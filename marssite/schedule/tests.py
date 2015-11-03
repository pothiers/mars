from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
#from rest_framework.test import APIRequestFactory

from .models import Slot, EmptySlot
import schedule.views



class ScheduleTest(TestCase):
    # Load (special test) DB with data
    fixtures = ['test.json']
    
    def setUp(self):
        self.factory = RequestFactory()

    def test_fixture(self):
        tele = 'kp4m'
        date = '2014-01-01'
        slot = Slot.objects.get(obsdate=date, telescope=tele)
        propid = slot.propid
        #print('DBG: db propid={}'.format(propid))
        expected = '2013B-0142'
        self.assertEqual(propid, expected)

    def test_getpropid(self):
        tele = 'kp4m'
        date = '2014-01-01'
        request = self.factory.get('/schedule/propid/{}/{}/'.format(tele, date))
        response = schedule.views.getpropid(request, tele, date)
        self.assertEqual(200, response.status_code)
        self.assertEqual('2013B-0142', response.content.decode())

    def test_upload(self):
        test_file = '/var/mars/small.xml'
        with open(test_file, 'rb') as fp:
            request = self.factory.post('/schedule/upload/',
                                        {'xmlfile': fp,
                                         'comment': 'for UNIT TEST'})
        response = schedule.views.upload_file(request)
        tele = 'ct4m'
        date = '2014-01-01'
        slot = Slot.objects.get(obsdate=date, telescope=tele)
        propid = slot.propid
        print('DBG: db propid={}'.format(propid))
        expected = '2012B-0001'
        #!self.assertRedirects(response, reverse('schedule:list'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(propid, expected)

    def test_list(self):
        request = self.factory.get(reverse('schedule:list'))
        response = schedule.views.list(request)
        self.assertEqual(200, response.status_code)
        self.assertContains(response,'2013B-0142')
