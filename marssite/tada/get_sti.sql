

SELECT tada_site.name AS "Site", tada_telescope.name AS "Tele", tada_instrument.name AS "Inst", tada_fileprefix.prefix as "Pfx"  FROM tada_fileprefix, tada_instrument, tada_telescope, tada_site WHERE tada_site.id = tada_fileprefix.site_id and tada_telescope.id = tada_fileprefix.telescope_id and tada_instrument.id = tada_fileprefix.instrument_id;

select * from tada_fileprefix;
select * from tada_instrument;
