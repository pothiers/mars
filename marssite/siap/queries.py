from pathlib import PurePath
from django.db import connection

# WARNING: this is querying a materialized view.  It only gets
# "materialized" every so often.  There is a delay before changes in
# the underlying tables are reflected here. (4+ minutes)
def get_tada_references(limit=50):
    """RETURN: Archive filenames that include TADA tag"""
    sql = ("SELECT reference,dtacqnam "
           "FROM voi.siap  "
           #!"WHERE reference LIKE '%TADA%' OR dtacqnam LIKE '%pothier%' "
           #!"WHERE reference LIKE '%TADA%' "
           # hundredths of a second since 1/1/2015
           #!"WHERE reference ~ '.*_\d{{10}}\.fits' OR reference LIKE '%TADA%'"
           "WHERE reference LIKE '%TADA%'"
           "LIMIT {}"
           .format(limit))
    cursor = connection.cursor()
    # Force material view refresh
    cursor.execute('SELECT * FROM refresh_voi_material_views()')
    cursor.fetchall()
    #
    cursor.execute(sql)
    total = cursor.rowcount
    #print('TADA select found {} records'.format(total))
    images = cursor.fetchall()
    return images

def get_like_archfile(archfile_substr, refresh=False, limit=150):
    """RETURN: Archive filenames that contain ARCHFILE_SUBSTR"""
    cursor = connection.cursor()
    if refresh:
        #Force material view refresh
        cursor.execute('SELECT * FROM refresh_voi_material_views()')
        cursor.fetchall()
    sql = ("SELECT reference FROM voi.siap WHERE reference LIKE '%{}%'"
           "LIMIT {}").format(archfile_substr, limit)
    cursor.execute(sql)
    #total = cursor.rowcount
    #print('TADA select found {} records'.format(total))
    images = cursor.fetchall()
    return images

# Reference            | Character Varying           | 
# Ra                   | numeric                     | 
# dec                  | numeric                     | 
# instrument           | citext                      | 
# telescope            | citext                      | 
# date_obs             | timestamp without time zone | 
# dtacqnam             | citext                      | 
# dtpropid             | citext                      | 
# dtsite               | citext                      | 
# proctype             | citext                      | 
# prodtype             | citext                      | 
# start_date           | timestamp without time zone | 
# release_date         | timestamp without time zone | 
def get_from_siap(refresh=False, limit=999, **kwargs):
    """Return list of dictionaries matching column in KWARGS.
    Each dict represents one row (dict[column]=value).
    This is similar to django query aggregation and should be replaced by such.
    """
    cursor = connection.cursor()
    if refresh:
        #Force material view refresh
        cursor.execute('SELECT * FROM refresh_voi_material_views()')
        cursor.fetchall()

    where = list()
    # STB added 629 far future observations; all beyond 2080. Yr 193,036!!
    # http://www.halcyonmaps.com/constellations-throughout-the-ages/
    where.append("date_obs < '2050-01-01'")

    rangecols = ['ra', 'dec', 'date_obs', 'start_date', 'release_date']
    for k,v in kwargs.items():
        op = k[:4]
        if 'min:' == op and k[4:] in rangecols:
            where.append("{} >= '{}'".format(k[4:], v))
        elif 'max:' == op and k[4:] in rangecols:
            where.append("{} < '{}'".format(k[4:], v))
        elif k == 'reference':
            where.append("reference LIKE '%{}%'".format(v))
        else:
            where.append("{} = '{}'".format(k, v))

    whereclause = (' WHERE ' + ' AND '.join(where)) if len(where) > 0 else ''

    sql = ("SELECT count(*) FROM voi.siap {}".format(whereclause))
    cursor.execute(sql)
    total = cursor.fetchone()[0]

    sql = ("SELECT * FROM voi.siap {} LIMIT {}".format(whereclause, limit))
    print('Executing SQL: {}'.format(sql))
    cursor.execute(sql)
    cnt = cursor.rowcount
    columns = [col[0] for col in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return results, limit, cnt, total


# The field 'uri' In the table edu_noao_nsa.data_product contains the actual
# file location.
def get_fits_location(reference):
    """RETURN: absolute path to FITS file
    reference:: Archive basename of FITS file"""
    cursor = connection.cursor()
    sql = ("SELECT dp.uri FROM voi.siap as vs, edu_noao_nsa.data_product as dp"
           " WHERE dp.data_product_id = vs.fits_data_product_id"
           " AND vs.reference= '{}'").format(reference)
    print('sql={}'.format(sql))
    cursor.execute(sql)
    uri = cursor.fetchone()
    if uri != None:
        #return uri[0].replace('irods:///noao-tuc-z1','')
        ipath =  uri[0]
        return str(PurePath('/net/archive/',*PurePath(ipath).parts[2:]))
    return uri

        
    
