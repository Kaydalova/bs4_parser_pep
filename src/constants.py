from pathlib import Path

BASE_DIR = Path(__file__).parent
LOG_DIR = 'logs'
LOG_FILE = 'parser.log'
MAIN_DOC_URL = 'https://docs.python.org/3/'
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
PEP_DOCS_URL = 'https://peps.python.org/'
OUTPUT_FILE = 'file'
OUTPUT_TABLE = 'pretty'
FILE_SAVING_FOLDER = 'results'
EXPECTED_STATUS = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active')}

STATUS_COUNT_DICT = {
    'Active': 0,
    'Deferred': 0,
    'Final': 0,
    'Provisional': 0,
    'Rejected': 0,
    'Superseded': 0,
    'Withdrawn': 0,
    'Draft': 0}
