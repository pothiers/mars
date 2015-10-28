from django.test import TestCase, Client


class GetpropidTestCase(TestCase):


    #!def test_upload(self):
    #!    c = Client()
    #!    with open('/home/pothiers/sandbox/mars/marssite/schedule/small.xml') as fp:
    #!        #print('DBG: xmlstr="{}"'.format(xmlstr))
    #!        c.post('/schedule/upload/',data={'xmlfile': fp})
    #!    return True

    def test_list(self):
        c = Client()
        with open('/home/pothiers/sandbox/mars/marssite/schedule/small.xml') as fp:
            #print('DBG: xmlstr="{}"'.format(xmlstr))
            c.post('/schedule/upload/',data={'xmlfile': fp})

        response = c.get('/schedule/')
        #expected='all my goodies'
        expected='2013B-0621'
        print('DBG: content={}'.format(response.content.decode()))
        self.assertTrue(expected in response.content.decode())
        
    def test_getpropid(self):
        c = Client()
        response = c.get('/schedule/propid/kp21m/2014-01-01/')
        expected='2013B-0621'
        self.assertEqual(expected, response.content)
        
