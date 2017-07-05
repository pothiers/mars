search_1 = '{"meta": {"dal_version": "0.1.6", "timestamp": "2017-07-05T11:13:26.844", "comment": "WARNING: Has not been tested much. Does not use IMAGE_FILTER.", "sql": "SELECT reference, ra, dec, prop_id, surveyid as survey_id, date_obs as obs_date, dtpi as pi, telescope, instrument, release_date, rawfile as flag_raw, proctype, filter, filesize, filename, dtacqnam as original_filename, md5sum, exposure, obstype as observation_type, obsmode as observation_mode, prodtype as product, proctype, seeing, depth FROM voi.siap WHERE (ra <= 186.368791666667) AND (ra >= 176.368791666667) AND (dec <= -40.5396111111111) AND (dec >= -50.5396111111111) AND (dtpi = \'Cypriano\') AND (dtpropid = \'noao\') AND (\'[2009-04-01,2009-04-03]\'::tsrange @> date_obs::timestamp) AND (dtacqnam = \'/ua84/mosaic/tflagana/3103/stdr1_012.fits\') AND ((telescope = \'ct4m\') OR (telescope = \'foobar\')) AND ((instrument = \'mosaic_2\')) AND (release_date = \'2010-10-01T00:00:00\') AND ((proctype = \'raw\') OR (proctype = \'InstCal\')) AND (exposure = \'15\') ORDER BY reference DESC LIMIT 100 OFFSET 0", "page_result_count": 4, "to_here_count": 4, "total_count": 4}, "resultset": [{"md5sum": null, "pi": "Cypriano", "original_filename": "/ua84/mosaic/tflagana/3103/stdr1_012.fits", "prop_id": "noao", "filesize": 14234056, "product": "png", "flag_raw": "stdr1_012", "release_date": "2010-10-01T00:00:00", "observation_type": "object", "telescope": "ct4m", "survey_id": null, "instrument": "mosaic_2", "observation_mode": "imaging", "filename": null, "depth": "23.04", "dec": "-45.5388055555556", "proctype": "InstCal", "filter": "R Harris c6004", "obs_date": "2009-04-01T01:23:27.900", "seeing": "0.9", "reference": "tu006122.fits.gz", "exposure": "15", "ra": "181.368083333333"}, {"md5sum": null, "pi": "Cypriano", "original_filename": "/ua84/mosaic/tflagana/3103/stdr1_012.fits", "prop_id": "noao", "filesize": 96811, "product": "dqmask", "flag_raw": "stdr1_012", "release_date": "2010-10-01T00:00:00", "observation_type": "object", "telescope": "ct4m", "survey_id": null, "instrument": "mosaic_2", "observation_mode": "imaging", "filename": null, "depth": "23.04", "dec": "-45.5388055555556", "proctype": "InstCal", "filter": "R Harris c6004", "obs_date": "2009-04-01T01:23:27.900", "seeing": "0.9", "reference": "tu006121.fits.gz", "exposure": "15", "ra": "181.368083333333"}, {"md5sum": null, "pi": "Cypriano", "original_filename": "/ua84/mosaic/tflagana/3103/stdr1_012.fits", "prop_id": "noao", "filesize": 222411172, "product": "image", "flag_raw": "stdr1_012", "release_date": "2010-10-01T00:00:00", "observation_type": "object", "telescope": "ct4m", "survey_id": null, "instrument": "mosaic_2", "observation_mode": "imaging", "filename": null, "depth": "23.04", "dec": "-45.5388055555556", "proctype": "InstCal", "filter": "R Harris c6004", "obs_date": "2009-04-01T01:23:27.900", "seeing": "0.9", "reference": "tu006120.fits.gz", "exposure": "15", "ra": "181.368083333333"}, {"md5sum": null, "pi": "Cypriano", "original_filename": "/ua84/mosaic/tflagana/3103/stdr1_012.fits", "prop_id": "noao", "filesize": 63471160, "product": null, "flag_raw": null, "release_date": "2010-10-01T00:00:00", "observation_type": "object", "telescope": "ct4m", "survey_id": null, "instrument": "mosaic_2", "observation_mode": "imaging", "filename": null, "depth": null, "dec": "-45.5320555555556", "proctype": "Raw", "filter": "R Harris c6004", "obs_date": "2009-04-01T01:23:27.900", "seeing": null, "reference": "ct1922390.fits.gz", "exposure": "15", "ra": "181.357875"}]}'
