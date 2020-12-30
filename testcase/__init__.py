from base.base import log
from base.base import Base
from base.base_cms import Cms
from base.base_sle import Sle
from base.base_ae import Ae

import pytest
import allure
import time
import re
import os
from pprint import pprint

cms = Cms()
sle = Sle()
ae = Ae()

ROOT_ACCOUNT = os.getenv('ROOT_ACCOUNT')
