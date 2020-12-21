from . import allure
from . import pytest
from . import sle
from .bet_base import for_loop_bet_and_verify


@allure.feature()
@pytest.mark.skip("Too random to wait for the winning, because it's official's")
def test_d(username='welly1'):
    # cms.singled_out_setting()

    _, get_token = sle.get_launch_token(username)
    for_loop_bet_and_verify(token=get_token['token'],
                            gameId='TXFFC',
                            playType='STANDALONE',
                            betStrings=('dt1vs2,draw',),
                            playId=10901,
                            playRateId=79551,
                            rebatePackage=1980,
                            stake=3,
                            times=1)

