from base.base_sle import Sle
from testcase import cms, Base, log
import pytest

sle = Sle()


@pytest.fixture()
def token():
    _, get_token = sle.get_token(username='welly1')

    return get_token['token']
