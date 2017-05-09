from datetime import datetime
from schedule.models import Slot
from djangocalendar.models import Event

'''
  Sync will take data from the slots table and build a structure to be used
  in hydrating the calendar events table.

  The data structure to hold consecutive dates for propid:
  - each child array holds groups of days that are consecutive to
    infer a date range for the prop id to be displayed on the calendar
{
  propId1: [
    [date1, date2, date3],
    [date4, date5]
  ],
  propId2: [
    [date1, date2]
  ],
   ...
}
    .

'''
class Sync(object):

    def __init__(self):
        pass

    @classmethod
    def build_datastructure(self, slots):
        container = {}
        for s in slots:
            props = s.propids.split(", ")
            for pr in props:
                current = None
                injectTo = None
                # if not in list create a new group
                if pr not in container:
                    container[pr] = [[]]
                    injectTo = container[pr][0]
                else:
                    # used to check the dates below
                    lastSet = container[pr][-1]
                    current = lastSet[-1]

                if current is not None:
                    # check the dates
                    # if next slot is not consecutive (difference is more than a day and a second)
                    #  - create a new set and add it there
                    # else
                    #  - add it to the last set
                    delta = s.obsdate-current
                    if delta.total_seconds() > (24*60*60+1):
                        # new set - also happens to be the last set
                        container[pr].append([])

                    # the last set
                    injectTo = container[pr][-1]

                # add the new date 
                injectTo.append(s.obsdate)
        return container

    @classmethod
    def create_events(self, data):
        for prop in data:
            for sets in data[prop]:
                startDate = sets[0]
                endDate = sets[-1]

                e = Event()
                e.start = startDate
                e.end = endDate
                e.title = prop
                e.save()


    @classmethod
    def sync_slots(self):
        limit = 10000
        rounds = 0
        slots = Slot.objects.all()[:limit]
        while slots:
            rounds += 1
            propIdDates = self.build_datastructure(slots)

            self.create_events(propIdDates)
            slots = Slot.objects.all()[limit*rounds:limit*rounds+limit]

        return {'status':"Done"}
