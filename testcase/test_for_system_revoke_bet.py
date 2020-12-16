from testcase import allure
from testcase import Base
from testcase import cms
from testcase import log
from testcase import pytest
from testcase import sle
from testcase import time
from testcase.bet_base import bet
from testcase.bet_base import now_month
from testcase.bet_base import now_day
import os

ROOT_ACCOUNT = os.getenv('ROOT_ACCOUNT')


@allure.feature('Scenario for system revoke bet when game closed')
def test_system_step_backs_info(games_close_or_open_init,
                                gameId='TXFFC',
                                cms_username=ROOT_ACCOUNT,
                                sle_username='welly1',
                                gameStatus='INACTIVE',
                                playType='STANDALONE' or 'SIMPLE',
                                betString='f3vary1,5',
                                playId=10310,
                                playRateId=18639,
                                stake=1,
                                times=5,
                                types='SYS_CANCELLED'):

    start, end = Base().start_and_end_time(now_month, now_day, now_month, now_day)

    cms_init_record = cms.transaction_record(userId=f"SL3{sle_username}",
                                             end=end,
                                             start=start,
                                             types=types,)

    _, get_token = sle.get_launch_token(sle_username)
    sle_init_record = sle.transaction_record(token=get_token['token'],
                                             start=start,
                                             end=end,
                                             types=types)
    bet(gameId=gameId,
        playType=playType,
        betString=betString,
        playId=playId,
        playRateId=playRateId,
        stake=stake,
        times=times,
        token=get_token['token'],)

    cms.games_close_or_open(username=cms_username,
                            gameId=gameId,
                            gameStatus=gameStatus,
                            playType=playType)

    cms_record = cms.transaction_record(userId=f"SL3{sle_username}",
                                        end=end,
                                        start=start,
                                        types=types,)

    timess = 0
    log(f"Wait for the record update, it will spend about 30 second")
    while cms_record['total'] == cms_init_record['total']:
        time.sleep(5)
        timess += 1
        cms_record = cms.transaction_record(userId=f"SL3{sle_username}",
                                            end=end,
                                            start=start,
                                            types=types,)
        if timess > 12:
            raise ValueError("It spend more then 1 minute, the original update time is about 30 second")


    sle_record = sle.transaction_record(token=get_token['token'],
                                        start=start,
                                        end=end,
                                        types=types)
    sle_data = sle_record['data'][0]
    pytest.assume(sle_data['txnAmt'] == stake * times)
    pytest.assume(sle_data['txnType'] == types)
    pytest.assume(sle_data['in'] == True)
    pytest.assume(sle_data['afterBalance'] == sle_data['beforeBalance'] + (stake * times))

    cms_data = cms_record['data'][0]
    pytest.assume(cms_data['txnAmt'] == stake * times)
    pytest.assume(cms_data['txnType'] == types)
    pytest.assume(cms_data['in'] == True)
    pytest.assume(cms_data['afterBalance'] == cms_data['beforeBalance'] + (stake * times))
    pytest.assume(cms_data['userId'] == f"SL3{sle_username}")
    pytest.assume(cms_data['detailType'] == 'LOTTERY')

    pytest.assume(sle_init_record['total'] == sle_record['total'] - 1)
    assert cms_init_record['total'] == cms_record['total'] - 1


@pytest.fixture()
def games_close_or_open_init(gameId='TXFFC',
                             cms_username=ROOT_ACCOUNT,
                             playType='STANDALONE',
                             gameStatus='ACTIVE',):
    status_code = cms.games_close_or_open(username=cms_username,
                                            gameId=gameId,
                                            gameStatus=gameStatus,
                                            playType=playType)
    if status_code != 204:
        raise ValueError('Init failed')
    yield

    cms.games_close_or_open(username=cms_username,
                            gameId=gameId,
                            gameStatus=gameStatus,
                            playType=playType)
    if status_code != 204:
        raise ValueError('Teardown failed')