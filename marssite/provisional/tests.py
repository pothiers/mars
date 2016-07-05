from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse

from .models import Fitsname
import provisional.views 

class ProvisionalTest(TestCase):
    # Load (special test) DB with data
    fixtures = ['test.json']

    def setUp(self):
        self.factory = RequestFactory()

    def test_fixture(self):
        fname = Fitsname.objects.get(pk='ksb_150709_044421_ori_TADATEST.fits')
        self.assertEqual(fname.source, "bok23m-90prime/d7212.0062.fits")

    def test_list(self):
        request = self.factory.get('/provisional/')
        response = provisional.views.index(request)
        self.assertTrue('Load from' in response.content.decode())


    def test_add(self):
        ref = 'foo.fits'
        src = 'foo.fz'
        url = reverse('provisional:add', kwargs={'reference': ref})
        request = self.factory.get(url+'/?source={src}'
                                   .format(src=src))
        response = provisional.views.add(request, ref)
        self.assertEqual(200, response.status_code)
        self.assertEqual(('Added provisional name (id=foo.fits, source={})'
                          .format(src)),
                         response.content.decode())

    ##
    ## CANNOT test ROLLBACK or STUFF because they affect live (unmanaged) DB.
    ## They are intended to delete/extract from the Archive DB!
    ##
    #!def test_rollback(self):
    #!    request = self.factory.get(reverse('provisional:rollback'))
    #!    response = provisional.views.rollback(request)
    #!    self.assertEqual(200, response.status_code)
    #!    self.assertEqual('FOOBAR ', response.content.decode())
    #!
    #!def test_stuff(self):
    #!    request = self.factory.get(reverse('provisional:stuff'))
    #!    response = provisional.views.stuff_with_tada(request)
    #!    self.assertEqual(200, response.status_code)
    #!    self.assertEqual('FOOBAR ', response.content.decode())
    
