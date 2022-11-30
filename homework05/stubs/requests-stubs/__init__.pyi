from .__version__ import __author__ as __author__
from .__version__ import __author_email__ as __author_email__
from .__version__ import __build__ as __build__
from .__version__ import __cake__ as __cake__
from .__version__ import __copyright__ as __copyright__
from .__version__ import __description__ as __description__
from .__version__ import __license__ as __license__
from .__version__ import __title__ as __title__
from .__version__ import __url__ as __url__
from .__version__ import __version__ as __version__
from .api import delete as delete
from .api import get as get
from .api import head as head
from .api import options as options
from .api import patch as patch
from .api import post as post
from .api import put as put
from .api import request as request
from .exceptions import ConnectionError as ConnectionError
from .exceptions import ConnectTimeout as ConnectTimeout
from .exceptions import FileModeWarning as FileModeWarning
from .exceptions import HTTPError as HTTPError
from .exceptions import JSONDecodeError as JSONDecodeError
from .exceptions import ReadTimeout as ReadTimeout
from .exceptions import RequestException as RequestException
from .exceptions import Timeout as Timeout
from .exceptions import TooManyRedirects as TooManyRedirects
from .exceptions import URLRequired as URLRequired
from .models import PreparedRequest as PreparedRequest
from .models import Request as Request
from .models import Response as Response
from .sessions import Session as Session
from .sessions import session as session
from .status_codes import codes as codes

def check_compatibility(
    urllib3_version: str, chardet_version: str | None, charset_normalizer_version: str | None
) -> None: ...
