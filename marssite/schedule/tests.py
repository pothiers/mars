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
        
