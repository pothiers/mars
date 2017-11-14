from . import utils
######
#  Provides a library of calls made from external references i.e. not from a http request
#  Allows for interal access to dal functionality
######


def get_all_filenames_for_query(query):
    """
        Returns the list of filenames for a given query. Used in processing symlinks for 
        staging. 
    """
    # all results
    files = []
    # transform the query data into a query object we can process
    result = utils.process_query(query, 1, 50000, "+reference")
    resultset = result['resultset']
    for n in resultset:
        # check if file exists
        files.append(n['reference'])
    return files
