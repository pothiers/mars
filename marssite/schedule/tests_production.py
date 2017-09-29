# EXAMPLES:
# ./manage.py test --keepdb schedule.tests_production
# ./manage.py test 
# ./manage.py test schedule.tests_production.ScheduleTest.test_getpropid2 


from django.core.urlresolvers import reverse
from django.test import TestCase, Client, RequestFactory
from .models import Slot
import schedule.views

class ScheduleTest(TestCase):
    # Load (special test) DB with data
    #fixtures = ['schedule.yaml', 'dump.tada.yaml']
    fixtures = ['schedule.yaml', 'natica.yaml']

    def setUp(self):
        #self.factory = RequestFactory()
        #print('DBG: ScheduleTest.setUp()')
        self.client = Client()

    # Should test for:
    #   1. found in Slots
    #   2. not found in Slots, found in TAC
    #      - return propid from TAC
    #      - add to Slots
    #   3. Not found in Slots, not found in TAC, use DEFAULT
    #      - return propid from Defaults
    #      - no change to Slots
    #   4. Not found in Slots, not found in TAC, no DEFAULT found
    #      - return propid generated from tele,instrum ("NEED-DEFAULT.*")
    #      - no change to Slots
    
    
    def test_getpropid1(self):
        "Found in slots"
        tele = 'kp4m'
        instrum = 'kosmos'
        date = '2016-02-01'
        expected = '2015B-0313'
        response = self.client.get('/schedule/propid/{}/{}/{}/'
                                   .format(tele, instrum, date))
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, response.content.decode())

    # ./manage.py test --noinput schedule.tests_production.ScheduleTest.test_getpropid2
    def test_getpropid2(self):
        "Not found in Slots, found in TAC. (update Slots from TAC)"
        tele = 'kp4m'
        instrum = 'mosaic3'
        date = '2016-02-02'
        expected = '2016A-0453'
        #print('DBG: test_getpropid: instrum={}'.format(instrum))
        response = self.client.get('/schedule/propid/{}/{}/{}/'
                                   .format(tele, instrum, date))
        try:
            slot = Slot.objects.exists(obsdate=date,
                                       telescope=tele,
                                       instrument=instrum)
        except:
            pass
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, response.content.decode())

    def test_getpropid3(self):
        "Not found in Slots, not found in TAC, use DEFAULT. No SLOT change"
        tele = 'kp4m'
        instrum = 'kosmos'
        date = '1816-02-01'
        expected = '1816A-0247'
        response = self.client.get('/schedule/propid/{}/{}/{}/'
                                   .format(tele, instrum, date))
        try:
            slot = Slot.objects.exists(obsdate=date,
                                       telescope=tele,
                                       instrument=instrum)
        except:
            pass
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, response.content.decode())

        
    def test_getpropid4(self):
        "Not found in Slots, not found in TAC, no DEFAULT found. No SLOT change"
        tele = 'kp4m'
        instrum = 'no_instrument'
        date = '1816-02-01'
        expected = 'NEED-DEFAULT.{}.{}'.format(tele, instrum)
        response = self.client.get('/schedule/propid/{}/{}/{}/'
                                   .format(tele, instrum, date))
        try:
            slot = Slot.objects.exists(obsdate=date,
                                       telescope=tele,
                                       instrument=instrum)
        except:
            pass
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, response.content.decode())

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

    #############################################################
    ### dppropid: Determine what PROPID to use for DB.
    ###    Includes split-night handling behavior
    ###
    ### 1.   No Slot                                   => REJECT
    ### 2.   Slot with no propids (null list)          => REJECT
    ### 3.1  slot cnt <> 0, split=True, HdrPid not in Slot => REJECT
    ### 3.2  slot cnt <> 0, split=True, HdrPid in Slot => HdrPid

    ### 4.   slot cnt == 1, split=False                => slot[0]
    ### 5.   slot cnt >  1, split=False                => slot[0], WARN multipid


    
    def test_dbpropid_1(self):
        "No Slot                                   => REJECT"
        pass
    
    def test_dbpropid_2(self):
        "Slot with no propids (null list)          => REJECT"
        pass

    def test_dbpropid_3_1(self):
        "slot cnt <> 0, split=True, HdrPid not in Slot => REJECT"
        tele = 'kp4m'
        instrum = 'kosmos'
        date = '2015-09-03'
        hdrpid = 'foobar'
        expected = "Propid from hdr (foobar) not in scheduled list of Propids ['2015B-0267']; Telescope=kp4m, Instrument=kosmos, Date=2015-09-03\n"
        response = self.client.get('/schedule/dbpropid/{}/{}/{}/{}/'
                                   .format(tele, instrum, date, hdrpid))
        self.assertEqual(expected, response.content.decode())
        self.assertEqual(404, response.status_code)

    def test_dbpropid_3_2(self):
        "slot cnt <> 0, split=True, HdrPid in Slot => HdrPid"
        tele = 'kp4m'
        instrum = 'kosmos'
        date = '2015-09-03'
        hdrpid = '2015B-0267'
        expected = hdrpid
        response = self.client.get('/schedule/dbpropid/{}/{}/{}/{}/'
                                   .format(tele, instrum, date, hdrpid))
        self.assertEqual(expected, response.content.decode())
        self.assertEqual(200, response.status_code)

    def test_dbpropid_4(self):
        "slot cnt == 1, split=False                => slot[0]"
        tele = 'kp4m'
        instrum = 'kosmos'
        date = '2015-09-04'
        hdrpid = 'foobar'
        expected = '2015B-0267'
        response = self.client.get('/schedule/dbpropid/{}/{}/{}/{}/'
                                   .format(tele, instrum, date, hdrpid))
        self.assertEqual(expected, response.content.decode())
        self.assertEqual(200, response.status_code)
        
    def test_dbpropid_5(self):
        "slot cnt >  1, split=False                => slot[0], WARN multipid"
        tele = 'kp4m'
        instrum = 'kosmos'
        date = '2015-09-05'
        hdrpid = 'foobar'
        #expected = '2015B-0313'
        expected = '2015B-0267' # first of sorted list
        response = self.client.get('/schedule/dbpropid/{}/{}/{}/{}/'
                                   .format(tele, instrum, date, hdrpid))
        self.assertEqual(expected, response.content.decode())
        self.assertEqual(200, response.status_code)
