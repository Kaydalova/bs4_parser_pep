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
    'A': 0,
    'D': 0,
    'F': 0,
    'P': 0,
    'R': 0,
    'S': 0,
    'W': 0,
    '': 0}
