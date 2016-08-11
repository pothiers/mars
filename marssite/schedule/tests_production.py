from django.core.urlresolvers import reverse
from django.test import TestCase, Client, RequestFactory
#from rest_framework.test import APIRequestFactory

from .models import Slot
import schedule.views

class ScheduleTest(TestCase):
    # Load (special test) DB with data
    fixtures = ['schedule.yaml']
    

    def setUp(self):
        #self.factory = RequestFactory()
        self.client = Client()

    # Should test for:
    #   1. found in Slots
    #   2. not found in Slots, found in TAC
    #      - return propid from TAC
    #      - add to Slots
    #   3. Not found in Slots, not found in TAC
    #      - return propid from Defaults
    #      - no change to Slots
    def test_getpropid1(self):
        "Found in slots"
        tele = 'kp4m'
        instrum = 'kosmos'
        date = '2016-02-01'
        response = self.client.get('/schedule/propid/{}/{}/{}/'
                                   .format(tele, instrum, date))
        self.assertEqual(200, response.status_code)
        expected = '2015B-0313'
        self.assertEqual(expected, response.content.decode())

    #!def test_getpropid2(self):
    #!    tele = 'kp4m'
    #!    instrum = 'kosmos'
    #!    date = '2015-09-04'
    #!    #!request = self.factory.get('/schedule/propid/{}/{}/{}/'
    #!    #!                           .format(tele, instrum, date))
    #!    #!response = schedule.views.getpropid(request, tele, instrum, date)
    #!    response = self.client.get('/schedule/propid/{}/{}/{}/'
    #!                               .format(tele, instrum, date))
    #!    self.assertEqual(200, response.status_code)
    #!    expected = '2015B-0267'
    #!    self.assertEqual(expected, response.content.decode())


    # needed after Dave's schedule gets updated when we've already
    # cached a value in the mars schedule
    def test_update_date(self):
        response = self.client.get('/schedule/update/2015-09-04/')
        #print('response={}'.format(response.content))
        self.assertEqual(200, response.status_code)

    def test_update_semester(self):
        response = self.client.get('/schedule/update/2015B/')
        #print('response={}'.format(response.content))
        self.assertEqual(200, response.status_code)

        
    #!def test_upload(self):
    #!    test_file = '/var/mars/small.xml'
    #!    with open(test_file, 'rb') as fp:
    #!        request = self.factory.post('/schedule/upload/',
    #!                                    {'xmlfile': fp,
    #!                                     'comment': 'for UNIT TEST'})
    #!    response = schedule.views.upload_file(request)
    #!    tele = 'ct4m'
    #!    date = '2014-01-01'
    #!    slot = Slot.objects.get(obsdate=date, telescope=tele)
    #!    propid = slot.propid
    #!    expected = '2012B-0001'
    #!    #!self.assertRedirects(response, reverse('schedule:list'))
    #!    self.assertEqual(response.status_code, 302)
    #!    self.assertEqual(propid, expected)
    
    #!def test_list(self):
    #!    request = self.factory.get('/schedule/list/')
    #!    response = schedule.views.SlotList.as_view()(request)
    #!    self.assertEqual(200, response.status_code)
    #!    self.assertContains(response,'2013B-0142')