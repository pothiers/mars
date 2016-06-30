from pathlib import PurePath

def fits_path(dateobs, telescope, propid, basename,
              relative=False,
              source='mtn', # or "pipe"
              root='/net/archive'):
    """
    dateobs:: YYYY-MM-DD
    basename:: FITS base filename used in Archive (and Mass-Store)
    """
    path = PurePath(dateobs.replace('-',''), telescope, propid, basename)

    if relative:
        return str(path)
    else:
        return str(PurePath(root,source, path))

