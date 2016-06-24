from pathlib import PurePath

def fits_path(dateobs, telescope, propid, basename,
              source='mtn', # or "pipe"
              root='/data/noao'):
    """
    dateobs:: YYYY-MM-DD
    basename:: FITS base filename used in Archive (and Mass-Store)
    """
    return str(PurePath(root, source,
                    dateobs.replace('-',''), telescope, propid,
                    basename))

