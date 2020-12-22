from . import allure
from . import Base
from . import cms
from . import log
from . import pytest
from . import sle
from . import time
from .bet_base import bet
from .bet_base import now_month
from .bet_base import now_day
from .bet_base import for_loop_bet_and_verify
from .bet_base import wait_and_lottery_draw


@allure.feature("Scenario with check info correct after bet in bet detail report")
def test_info_correct_after_bet(username='welly1',
                                gameId='NYTHAIFFC',
                                playType='STANDALONE',
                                result='000001|111|111|222|222|45',
                                betStrings=('3dtop|001', '3dtop|004'),
                                playId=90001,
                                playRateId=102328,
                                rebatePackage=1980,
                                betCount=1,
                                currency='CNY',
                                stake=1,
                                validBet=1,
                                cancellable=False,
                                odds=920,
                                betCategory='3D',
                                prizeRebate=0,
                                lose_stateStr='LOST',
                                win_stateStr='WON',
                                lose_prizeWon=0,
                                win_prizeWon=920,
                                lose_pl=-1,
                                win_pl=919,
                                ):
    # TODO: 需增加 程式開獎的測試 case(單獨一個 case)
    start, end = Base().start_and_end_time(now_month, now_day, now_month, now_day)

    setup_prize_limit(gameId, playType)

    wait_and_lottery_draw(result=result, gameId=gameId, count_down_second=22)

    _, get_token = sle.get_launch_token(username)
    response = for_loop_bet_and_verify(gameId=gameId,
                                       playType=playType,
                                       betStrings=betStrings,
                                       playId=playId,
                                       playRateId=playRateId,
                                       rebatePackage=rebatePackage,
                                       stake=stake,
                                       token=get_token['token'])

    bet_data = wait_for_the_bet_details_report_update(gameId, start, end, betStrings, txnId=response[0])
    assert_info_in_details_report(bet_data,
                                  playType,
                                  playId,
                                  playRateId,
                                  result,
                                  betCount,
                                  currency,
                                  stake,
                                  validBet,
                                  cancellable,
                                  odds,
                                  betCategory,
                                  prizeRebate,
                                  lose_stateStr,
                                  win_stateStr,
                                  lose_prizeWon,
                                  win_prizeWon,
                                  lose_pl,
                                  win_pl)


def setup_prize_limit(gameId, playType):
    prize_limit_status = cms.win_prize_limit(gameId=gameId, playType=playType, prizeLimit=20000)
    assert prize_limit_status == 204


def wait_for_the_bet_details_report_update(gameId, start, end, betStrings, txnId):
    times = 0
    _, bet_details = cms.bet_details(tm_start=start, tm_end=end, limit=2)
    if bet_details['data'][0]['gameId'] == gameId and bet_details['data'][1]['gameId'] == gameId \
            and bet_details['data'][0]['betString'] == betStrings[1][6:] \
            and bet_details['data'][1]['betString'] == betStrings[0][6:] \
            and bet_details['data'][0]['txnId'] == txnId:
        while bet_details['data'][0]['pl'] == 0 and bet_details['data'][1]['pl'] == 0:
            time.sleep(15)
            times += 1
            _, bet_details = cms.bet_details(tm_start=start, tm_end=end, limit=2)
            if times > 4:
                raise ValueError('Too slow to load')
    else:
        raise ValueError("The first two bet's info is not mine")

    return bet_details['data']


def assert_info_in_details_report(bet_data,
                                  playType,
                                  playId,
                                  playRateId,
                                  result,
                                  betCount,
                                  currency,
                                  stake,
                                  validBet,
                                  cancellable,
                                  odds,
                                  betCategory,
                                  prizeRebate,
                                  lose_stateStr,
                                  win_stateStr,
                                  lose_prizeWon,
                                  win_prizeWon,
                                  lose_pl,
                                  win_pl
                                  ):
    lose_dt = bet_data[0]
    win_dt = bet_data[1]

    assert lose_dt['playType'] == playType
    assert lose_dt['playId'] == playId
    assert lose_dt['playRateId'] == playRateId
    assert lose_dt['result'] == result
    assert lose_dt['betCount'] == betCount
    assert lose_dt['currency'] == currency
    assert lose_dt['stake'] == stake
    assert lose_dt['validBet'] == validBet
    assert lose_dt['cancellable'] == cancellable
    assert lose_dt['prize'][0] == odds
    assert lose_dt['odds'][0] == odds
    assert betCategory in lose_dt['betCategory']
    assert lose_dt['prizeRebate'] == prizeRebate
    assert lose_dt['stateStr'] == lose_stateStr
    assert lose_dt['prizeWon'] == lose_prizeWon
    assert lose_dt['pl'] == lose_pl

    assert win_dt['playType'] == playType
    assert win_dt['playId'] == playId
    assert win_dt['playRateId'] == playRateId
    assert win_dt['result'] == result
    assert win_dt['betCount'] == betCount
    assert win_dt['currency'] == currency
    assert win_dt['stake'] == stake
    assert win_dt['validBet'] == validBet
    assert win_dt['cancellable'] == cancellable
    assert win_dt['prize'][0] == odds
    assert win_dt['odds'][0] == odds
    assert betCategory in win_dt['betCategory']
    assert win_dt['prizeRebate'] == prizeRebate
    assert win_dt['stateStr'] == win_stateStr
    assert win_dt['prizeWon'] == win_prizeWon
    assert win_dt['pl'] == win_pl
