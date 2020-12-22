from . import cms
from . import sle
from . import time
from . import log
from . import Base
from . import pytest
from . import allure


@pytest.fixture()
def token():
    _, get_token = sle.get_launch_token(username='welly1')

    return get_token['token']


@pytest.fixture()
def little_game_init_button():
    lg_get = cms.little_game_get_or_patch(method='get')
    for lg in lg_get:
        if lg['status'] != 'NORMAL':
            cms.little_game_get_or_patch(method='patch',
                                         SC_status='NORMAL',
                                         RPS_status='NORMAL',
                                         HL_status='NORMAL')
    yield

    cms.little_game_get_or_patch(SC_commission=5,
                                 method='patch',
                                 SC_status='NORMAL')

