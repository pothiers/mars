from django.db import connection

# WARNING: this is querying a materialized view.  It only gets
# "materialized" every so often.  There is a delay before changes in
# the underlying tables are reflected here. (4+ minutes)
def get_tada_references(limit=50):
    sql=("SELECT reference,dtacqnam "
         "FROM voi.siap  "
         #!"WHERE reference LIKE '%TADA%' OR dtacqnam LIKE '%pothier%' "
         #!"WHERE reference LIKE '%TADA%' "
         # hundredths of a second since 1/1/2015
         "WHERE reference ~ '.*_\d{{10}}\.fits' OR reference LIKE '%TADA%'" 
         "LIMIT {}"
         .format(limit))
    cursor = connection.cursor()
    cursor.execute( sql )
    total = cursor.rowcount
    print('TADA select found {} records'.format(total))
    images = cursor.fetchall()
    return images
