from .api import Client, API, LOGGER
from .exceptions import *

__version__ = "1.0.2"

import requests

if requests.__version__ < "2.0.0":
    msg = (
        "You are using requests version %s, which is older than "
        "getnet-py expects, please upgrade to 2.0.0 or later."
    )
    raise Warning(msg % requests.__version__)
