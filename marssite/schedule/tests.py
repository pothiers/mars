from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
#from rest_framework.test import APIRequestFactory

from .models import Slot, EmptySlot
import schedule.views

class ScheduleTest(TestCase):
    # Load (special test) DB with data
    fixtures = ['schedule.yaml']
    
    def setUp(self):
        self.factory = RequestFactory()

    def test_fixture(self):
        tele = 'kp4m'
        instrum = 'y4kcam'
        date = '2016-01-01'
        slot = Slot.objects.get(obsdate=date,
                                telescope=tele,
                                instrument=instrum)
        propids = slot.propids.split(', ')
        #!print('DBG: db propids={}'.format(propids))
        expected = '2015B-0254'
        self.assertIn(expected, propids)
    
    def test_getpropid(self):
        tele = 'kp4m'
        instrum = 'y4kcam'
        date = '2016-01-01'
        request = self.factory.get('/schedule/propid/{}/{}/{}/'
                                   .format(tele, instrum, date))
        response = schedule.views.getpropid(request, tele, instrum, date)
        self.assertEqual(200, response.status_code)
        expected = '2015B-0254'
        self.assertEqual(expected, response.content.decode())
    
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
    #!    print('DBG: db propid={}'.format(propid))
    #!    expected = '2012B-0001'
    #!    #!self.assertRedirects(response, reverse('schedule:list'))
    #!    self.assertEqual(response.status_code, 302)
    #!    self.assertEqual(propid, expected)
    
    #!def test_list(self):
    #!    request = self.factory.get('/schedule/list/')
    #!    response = schedule.views.SlotList.as_view()(request)
    #!    self.assertEqual(200, response.status_code)
    #!    print('DBG: response.content={}'.format(response.content.decode()))
    #!    self.assertContains(response,'2013B-0142')
