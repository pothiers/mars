from django.db.models.signals import pre_save, post_save, m2m_changed 
from django.dispatch import receiver
from datetime import datetime, timezone, timedelta
import pdb

from djangocalendar.models import Event, Calendar
from schedule.models import Proposal

def optional_calendar(sender, **kwargs):
    event = kwargs.pop('instance')

    if not isinstance(event, Event):
        return True
    if not event.calendar:
        try:
            calendar = Calendar.objects.get(name='default')
        except Calendar.DoesNotExist:
            calendar = Calendar(name='default', slug='default')
            calendar.save()

        event.calendar = calendar
    return True

def update_slot(sender, **kwargs):
    import pdb; pdb.set_trace()
    return True
    if "schedule.models.Slot" not in str(sender):
        return True
    else:
        # create the calendar event
        slot = kwargs['instance']
        if slot.propid_list() is "":
            return True

        # problem: relational data doesn't exist yet
        # needs to be queried seperately
        props = Proposal.objects.filter(slot_id=slot.id)

        for prop in props:
            # check if this event is ongoing
            events = Event.objects.filter(title=prop)
            for item in events:
                # three possible conditions we care about
                # date adds to an existing timeframe i.e. +/- 1 day
                # date is within existing event timespan i.e. do nothing
                # date is neither the above two scenarios i.e. create a new calendar date
                obsdate = datetime(slot.obsdate.year, slot.obsdate.month, slot.obsdate.day)
                obsdate = obsdate.replace(tzinfo=item.start.tzinfo)
                if (obsdate-item.start) <= timedelta(days=1):
                    # change the calendar start
                    item.start = obsdate
                    item.save()
                elif (obsdate-item.end) <= timedelta(days=1):
                    item.end = obsdate
                    item.save()
                elif item.start <= obsdate and obsdate <= item.end: # do nothing
                    pass
                else:
                    # new item
                    event = Event()
                    event.title = prop
                    event.start = obsdate
                    event.end = event.start + timedelta(hours=1)
                    event.save()

    return True

m2m_changed.connect(update_slot)
pre_save.connect(optional_calendar)
