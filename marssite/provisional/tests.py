from django.test import TestCase, RequestFactory


from .models import Slot, EmptySlot
import provisional.views 

class ProvisionalTest(TestCase):
    # Load (special test) DB with data
    fixtures = ['test.json']

    def setUp(self):
        self.factory = RequestFactory()

    def test_fixture(self):
        pass

    def test_list(self):
        request = self.factory.get('/provisional/')
        response = provisional.views.index(request)
        self.assertTrue('Load from' in response.content.decode())

    def test_add(self):        
        request = self.factory.get('/provisional/add/{archfile}/?source={src}'
                                   .format(archfile='foo.fits', src='myfoo.fz'))        response = provisional.views.add(request)
        self.assertTrue('foobar' in response.content.decode())        
        
    
