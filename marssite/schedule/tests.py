from django.test import TestCase, RequestFactory
#from rest_framework.test import APIRequestFactory

from .models import Slot, EmptySlot
import schedule.views



class ScheduleTest(TestCase):
    # Load (special test) DB with data
    fixtures = ['test.json']
    
    def setUp(self):
        self.factory = RequestFactory()

        
    def test_list(self):
        request = self.factory.get('/schedule/')
        response = schedule.views.list(request)
        self.assertTrue('2013B-0142' in response.content.decode())

    def test_getpropid(self):
        request = self.factory.get('/schedule/propid/kp4m/2014-01-01/')
        response = schedule.views.getpropid(request,'kp4m', '2014-01-01')
        expected='2013B-0142'
        self.assertEqual(expected, response.content.decode())

    # UNDER CONSTRUCTION!!!
    def test_upload(self):
        test_file = '/var/mars/small.xml'
        with open(test_file, 'rb') as fp:
            request = self.factory.post('/schedule/upload/',
                                         {'xmlfile': fp},
            )

        response = schedule.views.upload_file(request)
        tele='ct4m'
        date='2014-01-01'
        slot = Slot.objects.get(obsdate=date,telescope=tele)
        propid = slot.propid
        print('DBG: db propid={}'.format(propid))
        expected='2012B-0001'
        self.assertEqual(response.status_code, 200)
        self.assertEqual(propid,expected)
