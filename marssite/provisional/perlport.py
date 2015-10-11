"Ported from perl: remove_fits_data_product.pl and DbToolLib.pm"

## WARNINGS:
## - Do as transaction.
## - Perl uses "prepare(multi_sqlstr)", "execute or bail", "finish", "commit"


def UNUSED_glean_fits_dp_info(cursor, file_id):
    sql = ("SELECT dtnsanam,dtpropid,reference "
           "FROM voi.siap "
           "WHERE fits_data_product_id=%(fits_file_id)s;".format(file_id))
    cursor.execute(sql, dict(fits_file_id=file_id))
    file_id = cursor.fetchone()[0]
    

def get_header_count(cursor, file_id):
    sql = ("SELECT count(*) FROM voi.siap "
           "WHERE fits_data_product_id=%(fits_file_id)s;".format(file_id))
    cursor.execute(sql, dict(fits_file_id=file_id))
    count = cursor.fetchone()[0]
    return count

def find_assoc_raw_headers(cursor, file_id):
    sql = ("SELECT fits_data_product_id, fits_header_id "
           "FROM edu_noao_nsa.fitsdataproduct_fitsheader_assoc "
           "WHERE fits_data_product_id = %(fits_id)s;")
    cursor.execute(sql, dict(fits_id=file_id))   
    return cursor.fetchall()
    

def create_drop_observation_sql_stmt(cursor, obs_id):
    'from DbToolLib.pm:create_drop_observation_sql_stmt(dbh,obs_id)'
    #raise Exception('UNIMPLEMENTED: perlport.create_drop_observation_sql_stmt')
    #
    
    sql = ''
    if obs_id > 0:
        # DbToolLib.pm:count_assoc
        sql0 = ("SELECT count(*) "
                "FROM edu_noao_nsa.observation_data_product_assoc "
                "WHERE observation_id = %(obs_id)s;")
        cursor.execute( sql0, dict(obs_id=obs_id) )
        count = cursor.fetchone()[0]
        if count < 2:
            # ONLY delete the observation IF this file is the last one
            # in assocation with it
            sql += ("DELETE FROM edu_noao_nsa.observation_proposal_assoc "
                    "WHERE observation_id = '{obs_id}';\n").format(obs_id=obs_id)
            sql += ("DELETE FROM edu_noao_nsa.observation "
                     "WHERE observation_id = '{obs_id}';\n").format(obs_id=obs_id)
            #!sql += ("SELECT count(*) "
            #!        "FROM edu_noao_nsa.observation_proposal_assoc "
            #!        "WHERE observation_id = %(obs_id)s;")
            #!sql += ("SELECT count(*) "
            #!        "FROM edu_noao_nsa.observation "
            #!         "WHERE observation_id =  %(obs_id)s;")
        
    return sql


# defined inline in: DbToolLib.pm:get_drop_file_sql()
def create_drop_header_sql_stmt(cursor, file_id):
    #raise Exception('UNIMPLEMENTED: perlport.create_drop_header_sql_stmt')
    #

    sql = ''
    if get_header_count(cursor, file_id) > 0:
        # build the sql for deleting assocated fits header structures
        for prod_id, header_id in find_assoc_raw_headers(cursor, file_id):
            #!print('DBG: header_id={}'.format(header_id))
            sql += ("DELETE FROM edu_noao_nsa.processed_fits_header "
                    "WHERE processed_fits_header_id = '{header_id}';\n"
                    "DELETE FROM edu_noao_nsa.fits_header "
                    "WHERE fits_header_id = '{header_id}';\n").format(header_id=header_id)
            #!sql += ("SELECT count(*) FROM edu_noao_nsa.processed_fits_header "
            #!        "WHERE processed_fits_header_id = '{header_id}';\n"
            #!        "SELECT count(*) FROM edu_noao_nsa.fits_header "
            #!        "WHERE fits_header_id = '{header_id}';\n").format(header_id=header_id)
            
            
    return sql

def drop_file(cursor, reference):
    print('Remove file: {}'.format(reference))
    # relevent part of: DbToolLib::glean_file_info_by_reference()
    sql = ("SELECT fits_data_product_id FROM viewspace.fits_data_product "
            "WHERE reference='{}';".format(reference))
    cursor.execute(sql)
    res = cursor.fetchone()
    if res == None:
        return 0
    file_id = res[0]

    # relevent part of: DbToolLib::glean_file_obs_info($dbh, $fits_file_id)
    sql = ("SELECT observation_id "
           "FROM edu_noao_nsa.observation_data_product_assoc "
           "WHERE data_product_id = '{}';".format(file_id))
    cursor.execute(sql)
    obs_id = cursor.fetchone()[0]

    obs_sql = create_drop_observation_sql_stmt(cursor, obs_id)
    hdr_sql = create_drop_header_sql_stmt(cursor, file_id)

    sql = """
DELETE FROM edu_noao_nsa.observation_data_product_assoc WHERE data_product_id = %(fits_file_id)s; 
-- Observation
{obs_sql}
--
DELETE FROM edu_noao_nsa.fitsdataproduct_fitsheader_assoc WHERE fits_data_product_id = %(fits_file_id)s; 
-- Header
{hdr_sql}
--
DELETE FROM edu_noao_nsa.instcal_data_quality_mask_assoc WHERE instcal_id = %(fits_file_id)s or data_quality_mask_id = %(fits_file_id)s;
DELETE FROM edu_noao_nsa.instcal_mastercal_image_data_product_assoc WHERE instcal_image_data_product_id = %(fits_file_id)s or master_calibration_image_data_product_id = %(fits_file_id)s;
-- associations between FDP
DELETE FROM edu_noao_nsa.instcal_preview_assoc WHERE instcal_id = %(fits_file_id)s or preview_id = %(fits_file_id)s;
DELETE FROM edu_noao_nsa.master_calibration_preview_assoc WHERE master_calibration_id = %(fits_file_id)s or preview_id = %(fits_file_id)s;
DELETE FROM edu_noao_nsa.parent_data_product_child_assoc WHERE parent_data_product_id = %(fits_file_id)s or child_data_product_id = %(fits_file_id)s;
DELETE FROM edu_noao_nsa.resampled_data_quality_mask_assoc WHERE resampled_id = %(fits_file_id)s or data_quality_mask_id = %(fits_file_id)s;
DELETE FROM edu_noao_nsa.resampled_preview_assoc WHERE resampled_id = %(fits_file_id)s or preview_id = %(fits_file_id)s;
DELETE FROM edu_noao_nsa.stacked_data_quality_mask_assoc WHERE stacked_id = %(fits_file_id)s or data_quality_mask_id = %(fits_file_id)s;
DELETE FROM edu_noao_nsa.stacked_exposure_map_assoc WHERE stacked_id = %(fits_file_id)s or exposure_map_id = %(fits_file_id)s;
DELETE FROM edu_noao_nsa.stacked_preview_assoc WHERE stacked_id = %(fits_file_id)s or preview_id = %(fits_file_id)s;
DELETE FROM edu_noao_nsa.instcal_wtmap_assoc WHERE instcal_id = %(fits_file_id)s or wtmap_id = %(fits_file_id)s;
DELETE FROM edu_noao_nsa.resampled_wtmap_assoc WHERE resampled_id = %(fits_file_id)s or wtmap_id = %(fits_file_id)s;
DELETE FROM edu_noao_nsa.stacked_wtmap_assoc WHERE stacked_id = %(fits_file_id)s or wtmap_id = %(fits_file_id)s;
DELETE FROM edu_noao_nsa.mastercal_wtmap_assoc WHERE mastercal_id = %(fits_file_id)s or wtmap_id = %(fits_file_id)s;
-- sub-classes of FDP
DELETE FROM edu_noao_nsa.data_quality_mask_data_product WHERE data_quality_mask_data_product_id = %(fits_file_id)s;
DELETE FROM edu_noao_nsa.exposure_map_data_product WHERE exposure_map_data_product_id = %(fits_file_id)s;
DELETE FROM edu_noao_nsa.instcal_image_data_product WHERE instcal_image_data_product_id = %(fits_file_id)s;
DELETE FROM edu_noao_nsa.master_calibration_image_data_product WHERE master_calibration_image_data_product_id = %(fits_file_id)s;
DELETE FROM edu_noao_nsa.preview_image_data_product WHERE preview_image_data_product_id = %(fits_file_id)s;
DELETE FROM edu_noao_nsa.raw_image_data_product WHERE raw_image_data_product_id = %(fits_file_id)s;
DELETE FROM edu_noao_nsa.resampled_image_data_product WHERE resampled_image_data_product_id = %(fits_file_id)s;
DELETE FROM edu_noao_nsa.stacked_image_data_product WHERE stacked_image_data_product_id = %(fits_file_id)s;
DELETE FROM edu_noao_nsa.wtmap_data_product WHERE wtmap_data_product_id = %(fits_file_id)s;
-- FDP
DELETE FROM edu_noao_nsa.fits_data_product WHERE fits_data_product_id = %(fits_file_id)s;
DELETE FROM edu_noao_nsa.data_product WHERE data_product_id = %(fits_file_id)s;
""".format(obs_sql = obs_sql,  hdr_sql = hdr_sql)

    #!print('drop_file() EXECUTING SQL (fits_file_id = {}): {}'
    #!      .format(file_id,sql))

    results = []
    #!for sqlline in sql.split('\n'):
    #!    if sqlline.strip() == '':
    #!        continue
    #!    if sqlline.strip()[:2] == '--':
    #!        continue
    #!    cursor.execute( sqlline, dict(fits_file_id=file_id ))
    #!    results.append(str(cursor.fetchone()[0]))

    cursor.execute( sql, dict(fits_file_id=file_id ))
    results = cursor.rowcount

    return results
 
