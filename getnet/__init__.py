import logging

from .api import API
from .exceptions import APIException

__version__ = "0.1.2"

import requests

if requests.__version__ < "2.0.0":
    msg = (
        "You are using requests version %s, which is older than "
        "getnet-py expects, please upgrade to 2.0.0 or later."
    )
    raise Warning(msg % requests.__version__)

logging.getLogger("getnet-py").addHandler(logging.NullHandler())
