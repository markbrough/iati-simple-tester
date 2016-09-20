import os.path


REGISTRY_API_BASE_URL = "https://iatiregistry.org/api/3/action"
CACHE_TIMEOUT = 86400  # 24 hours
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
DIR_FOR_TESTING = os.path.join(CURRENT_PATH, "uploads")
TESTS_FILE = os.path.join(CURRENT_PATH, "tests.csv")
FILTERS_FILE = os.path.join(CURRENT_PATH, "filters.csv")
DEFAULT_FILTER = None
DEFAULT_TEST = None
PER_PAGE = 20

from IATISimpleTester import codelists
LISTS = codelists.CODELISTS
LISTS["Agriculture"] = ["23070", "31110", "31120", "31130", "31140", "31150", "31161", "31162", "31163", "31164", "31165", "31166", "31181", "31182", "31191", "31192", "31193", "31194", "31195", "31210", "31220", "31261", "31281", "31282", "31291", "31310", "31320", "31381", "31382", "31391", "72040", "12240", "43040", "52010",]


######## Legacy command line config ########

# SUPPLY THE NAME OF THE PACKAGEGROUP (WILL LOOK FOR ALL .XML FILES BEGINNING
# WITH THIS)
PACKAGEGROUP_NAME = "dfid"

# SUPPLY THE CURRENT TEST EXPRESSION (WILL BE OUTPUT AS A COLUMN WITH PASS/FAIL)
CURRENT_TEST = "activity-date[@type='end-planned']/@iso-date or activity-date[@type='end-planned']/text() or activity-date[@type='end-actual']/@iso-date or activity-date[@type='end-actual']/text() or transaction-date/@iso-date (for any transaction[transaction-type/@code='D']|transaction[transaction-type/@code='E']) is less than 13 months ago?"

# SUPPLY THE TEST EXPRESSION(S) AS A DICT ('expression', 'name') WITHIN AN ARRAY
TESTS = [{'expression': "conditions or document-link/category[@code='A04'] exists (if activity-status/@code is at least 2 and conditions/@attached is not 0)?",
        'name': "Conditions"}]
