from builtins import bytes as bytes
from builtins import str as str
from collections import OrderedDict as OrderedDict
from urllib.parse import quote as quote
from urllib.parse import quote_plus as quote_plus
from urllib.parse import unquote as unquote
from urllib.parse import unquote_plus as unquote_plus
from urllib.parse import urldefrag as urldefrag
from urllib.parse import urlencode as urlencode
from urllib.parse import urljoin as urljoin
from urllib.parse import urlparse as urlparse
from urllib.parse import urlsplit as urlsplit
from urllib.parse import urlunparse as urlunparse
from urllib.request import getproxies as getproxies
from urllib.request import parse_http_list as parse_http_list
from urllib.request import proxy_bypass as proxy_bypass

from typing_extensions import Literal, TypeAlias

is_py2: Literal[False]
is_py3: Literal[True]
has_simplejson: bool

builtin_str: TypeAlias = str  # noqa: Y042
basestring: tuple[type, ...]
numeric_types: tuple[type, ...]
integer_types: tuple[type, ...]
