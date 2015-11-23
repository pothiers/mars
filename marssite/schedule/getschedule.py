#! /usr/bin/env python3
'''Get schedules in XML format for a bunch of dates and telescopes.'''

# EXAMPLES:
#   getschedule.py foo.xml --begindate=2015-10-09 --enddate=2015-10-11
#   getschedule.py all.2014.2016.xml --begindate=2014-01-01 --enddate=2016-07-01

import sys
import argparse
import logging
import subprocess
from datetime import date, datetime, timedelta as td
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

def getxml(outxml, begindate, enddate):
    '''begin/enddate :: DATE object'''

    telescope_list = ('ct09m,ct13m,ct15m,ct1m,ct4m,gem_n,gem_s,het,'
                      'keckI,keckII,kp09m,kp13m,kp21m,kp4m,kpcf,'
                      'magI,magII,mmt,soar,wiyn').split(',')

    # getschedulexml.pl -tel=wiyn -date=2015-09-01 >wiyn.2015-09-01.schedule.xml
    cmdstr = '/home/pothiers/sandbox/mars/marssite/schedule/getschedulexml.pl -tel={telescope} -date={date}'
    #cmd = cmdstr.split()

    delta = enddate - begindate
    ns = dict(noao="http://www.noao.edu/proposal/noao/", )
    with open(outxml, 'w') as f:
        print('<all created="{}" begindate="{}" enddate="{}">'
              .format(date.today().isoformat(),
                      begindate.isoformat(),
                      enddate.isoformat() ),
              file=f, flush=True)
        for i in range(delta.days + 1):
            obsdate = begindate + td(days=i)
            for tele in telescope_list:
                out = subprocess.check_output(cmdstr.format(telescope=tele,
                                                            date=obsdate),
                                              shell=True)
                #!print(out, file=f)
                if len(out) < 3:
                    continue
                logging.debug('XML from {}: {}'
                              .format(cmdstr.format(telescope=tele, date=obsdate), out))
                root = ET.fromstring(out)
                prop_el = root.find('.//proposal')
                if prop_el == None:
                    continue
                title = prop_el.findtext('title',default='')
                pif = prop_el.findtext(
                    'investigators[1]/investigator/name/first',
                    default='')
                pil = prop_el.findtext(
                    'investigators[1]/investigator/name/last',
                    default='')
                piname = pif + ' ' + pil
                affil = prop_el.findtext(
                    'investigators[1]/investigator/affiliation',
                    default='')
                
                tele_el = root.find('.//parameter[@name="telescope"]')
                date_el = root.find('.//parameter[@name="date"]')
                print('tele={}, date={} -> propid={}'
                      .format(tele_el.text,
                              date_el.text,
                              prop_el.get('{{{noao}}}id'.format(**ns)),
                      ))
                print('<proposal telescope="{}" date="{}" propid="{}"> \n'
                      '  <title>{}</title> \n'
                      '  <piname>{}</piname> \n'
                      '  <affiliation>{}</affiliation> \n'
                      '</proposal>'
                      .format(tele_el.text,
                              date_el.text,
                              prop_el.get('{{{noao}}}id'.format(**ns)),
                              escape(title), escape(piname), escape(affil) ),
                      file=f
                )
        print('</all>', file=f)                



##############################################################################

def main():
    "Parse command line arguments and do the work."
    #!print('EXECUTING: %s\n\n' % (' '.join(sys.argv)))
    parser = argparse.ArgumentParser(
        description='My shiny new python program',
        epilog='EXAMPLE: %(prog)s a b"'
        )
    parser.add_argument('--version', action='version', version='1.0.1')
    parser.add_argument('outxml', type=argparse.FileType('w'),
                        help='Output XML file')
    
    parser.add_argument('--begindate',
                        help='First date (YYYY-MM-DD) for returned schedule [default=today]')
    parser.add_argument('--enddate', 
                        help='Last date for returned schedule. [default=begindate]')


    parser.add_argument('--loglevel',
                        help='Kind of diagnostic output',
                        choices=['CRTICAL', 'ERROR', 'WARNING',
                                 'INFO', 'DEBUG'],
                        default='WARNING')
    args = parser.parse_args()
    args.outxml.close()
    args.outxml = args.outxml.name


    log_level = getattr(logging, args.loglevel.upper(), None)
    if not isinstance(log_level, int):
        parser.error('Invalid log level: %s' % args.loglevel)
    logging.basicConfig(level=log_level,
                        format='%(levelname)s %(message)s',
                        datefmt='%m-%d %H:%M')
    logging.debug('Debug output is enabled in %s !!!', sys.argv[0])

    if args.begindate == None:
        bdate = date.today()
    else:
        bdate = datetime.strptime(args.begindate,'%Y-%m-%d').date()

    if args.enddate == None:
        edate = bdate
    else:
        edate = datetime.strptime(args.enddate,'%Y-%m-%d').date()
        
    getxml(args.outxml, bdate, edate)

if __name__ == '__main__':
    main()

        
