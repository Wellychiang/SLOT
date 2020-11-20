from base.base_sle import Sle
import pytest

sle = Sle()


@pytest.fixture()
def token():
    _, get_token = sle.get_token()
    print('token')

    return get_token['token']
