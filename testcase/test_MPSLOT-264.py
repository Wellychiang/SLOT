from . import allure
from . import Base
from . import cms
from . import log
from . import pytest
from . import sle
from . import time
from . import ROOT_ACCOUNT
from .bet_base import bet
from .bet_base import now_month
from .bet_base import now_day
import os


@allure.feature('Scenario for system revoke bet when game closed')
@allure.step('')
def test_system_revoke_bet_info(games_close_or_open_init,
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
    game_bet_and_close(gameId=gameId,
                       playType=playType,
                       betString=betString,
                       playId=playId,
                       playRateId=playRateId,
                       stake=stake,
                       times=times,
                       token=get_token['token'],
                       username=cms_username,
                       gameStatus=gameStatus)

    cms_search_for_revoke_bet_and_equal_5(userId=f"SL3{sle_username}",
                                          start=start,
                                          end=end,
                                          types=types,
                                          cms_init_total_record=cms_init_record['total'],
                                          stake=stake,
                                          times=times)

    ec_search_for_revoke_bet_and_equal_5(token=get_token['token'],
                                         start=start,
                                         end=end,
                                         types=types,
                                         sle_init_total_record=sle_init_record['total'],
                                         stake=stake,
                                         times=times)


def game_bet_and_close(gameId, playType, betString, playId, playRateId, stake, times, token, username, gameStatus):
    bet(gameId=gameId,
        playType=playType,
        betString=betString,
        playId=playId,
        playRateId=playRateId,
        stake=stake,
        times=times,
        token=token)

    cms.games_close_or_open(username=username,
                            gameId=gameId,
                            gameStatus=gameStatus,
                            playType=playType)
    
    
def cms_search_for_revoke_bet_and_equal_5(userId, start, end, types, cms_init_total_record, stake, times, ):
    record = cms.transaction_record(userId=userId,
                                        end=end,
                                        start=start,
                                        types=types,)

    timess = 0
    log(f"Wait for the record update, it will spend about 30 second")
    while record['total'] == cms_init_total_record:
        time.sleep(5)
        timess += 1
        record = cms.transaction_record(userId=userId,
                                        end=end,
                                        start=start,
                                        types=types,)
        if timess > 12:
            raise ValueError("It spend more then 1 minute, the original update time is about 30 second")

    data = record['data'][0]
    pytest.assume(data['txnAmt'] == stake * times)
    pytest.assume(data['txnType'] == types)
    pytest.assume(data['in'] == True)
    pytest.assume(data['afterBalance'] == data['beforeBalance'] + (stake * times))
    pytest.assume(data['userId'] == userId)
    pytest.assume(data['detailType'] == 'LOTTERY')

    pytest.assume(cms_init_total_record == record['total'] - 1)


def ec_search_for_revoke_bet_and_equal_5(token, start, end, types, sle_init_total_record, stake, times,):
    record = sle.transaction_record(token=token,
                                    start=start,
                                    end=end,
                                    types=types)
    sle_data = record['data'][0]
    pytest.assume(sle_data['txnAmt'] == stake * times)
    pytest.assume(sle_data['txnType'] == types)
    pytest.assume(sle_data['in'] == True)
    pytest.assume(sle_data['afterBalance'] == sle_data['beforeBalance'] + (stake * times))

    pytest.assume(sle_init_total_record == record['total'] - 1)


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