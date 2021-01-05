from . import allure
from . import Base
from . import cms
from . import log
from . import pytest
from . import sle
from . import time
from .bet_base import bet
from . import ROOT_ACCOUNT
from .bet_base import for_loop_bet_and_verify
from .bet_base import now_month
from .bet_base import now_day
from .bet_base import wait_and_lottery_draw
from .bet_base import wait_for_bet_and_return_previous_or_current


@allure.feature(f"Scenario for search game profit info with no manual input lottery draw's nums")
@allure.step('')
def test_game_profit_info_with_no_input_draw_nums(gameId='NYSC30S',  # 空戰風雲
                                                  sleep_time=5,
                                                  playType='SIMPLE',
                                                  username=('welly1',),
                                                  betStrings=('s1p1|big', 's1p1|small'),
                                                  playId=17,
                                                  playRateId=12301,
                                                  rebatePackage=1980,
                                                  stake=1,
                                                  vendorId='MX2',
                                                  gameName='空战风云',
                                                  notPresetPnl=-0.02,
                                                  pnl=-0.02,
                                                  pnlRate=-0.01,
                                                  odds=1.98,
                                                  isSelfOpen=True,
                                                  ):
    start, end = Base().start_and_end_time(now_month, now_day, now_month, now_day)
    original_report = cms.game_profit_report(start=start, end=end, gameId=f'{gameId}|{playType}')

    wait_for_bet_and_return_previous_or_current(gameId, sleep_time)

    _, launch = sle.get_launch_token(username[0])
    for betString in betStrings:
        bet(gameId=gameId,
            betString=betString,
            playId=playId,  # 信用玩法依順序為17, 18, 19 .....(泰國彩不適用)
            playRateId=playRateId,
            rebatePackage=rebatePackage,
            stake=stake,
            token=launch['token'],)
        playRateId = 12302

    now_start_time = Base().return_now_start_time()
    report = wait_for_the_game_profit_report(start, end, gameId, playType, original_report, now_start_time)

    assert_the_game_profit_report_with_air_fight(report,
                                                 gameId,
                                                 vendorId,
                                                 playType,
                                                 gameName,
                                                 betUserCount=len(username),
                                                 betCount=len(betStrings),
                                                 stake=stake*len(betStrings),
                                                 validBet=stake*len(betStrings),
                                                 prizeWon=stake*odds,
                                                 notPresetPnl=notPresetPnl,
                                                 pnl=pnl,
                                                 pnlRate=pnlRate,
                                                 isSelfOpen=isSelfOpen,
                                                 count=len(report['records']))


def wait_for_the_game_profit_report(start, end, gameId, playType, original_report, now_start_time):
    profit_report = cms.game_profit_report(start=start, end=end, gameId=f'{gameId}|{playType}')

    times = 0
    if len(original_report['records']) == 0:
        while len(profit_report['records']) == len(original_report['records']):
            log(f"Records info is update now, wait a second")
            times += 1
            time.sleep(10)
            profit_report = cms.game_profit_report(start=start, end=end, gameId=f'{gameId}|{playType}')
    else:
        while profit_report['records'][0]['betCount'] == original_report['records'][0]['betCount']:
            log(f'Records info is update now, wait a second')
            times += 1
            time.sleep(10)
            profit_report = cms.game_profit_report(start=start, end=end, gameId=f'{gameId}|{playType}')

    if times > 6:
        raise ValueError(f"It's too slow to load in the game profit report")

    profit_report = cms.game_profit_report(start=now_start_time, end=end, gameId=f'{gameId}|{playType}')

    return profit_report


def assert_the_game_profit_report_with_air_fight(report,
                                                 gameId,
                                                 vendorId,
                                                 playType,
                                                 gameName,
                                                 betUserCount,
                                                 betCount,
                                                 stake,
                                                 validBet,
                                                 prizeWon,
                                                 notPresetPnl,
                                                 pnl,
                                                 pnlRate,
                                                 isSelfOpen,
                                                 count):
    info = report['records'][0]
    total = report['totalSummary']

    pytest.assume(info['vendorId'] == vendorId)
    pytest.assume(info['gameId'] == gameId)
    pytest.assume(info['playType'] == playType)
    pytest.assume(info['gameName'] == gameName)
    pytest.assume(info['betUserCount'] == betUserCount)
    pytest.assume(info['betCount'] == betCount)
    pytest.assume(info['txnCount'] is None)
    pytest.assume(info['stake'] == stake)
    pytest.assume(info['validBet'] == validBet)
    pytest.assume(info['presetValidBet'] == 0)
    pytest.assume(info['prizeWon'] == prizeWon)
    pytest.assume(info['notPresetPnl'] == notPresetPnl)
    pytest.assume(info['pnl'] == pnl)
    pytest.assume(info['pnlRate'] == pnlRate)
    pytest.assume(info['isSelfOpen'] == isSelfOpen)

    pytest.assume(total['betCount'] == betCount)
    pytest.assume(total['stake'] == stake)
    pytest.assume(total['presetValidBet'] == 0)
    pytest.assume(total['validBet'] == validBet)
    pytest.assume(total['prizeWon'] == prizeWon)
    pytest.assume(total['notPresetPnl'] == notPresetPnl)
    pytest.assume(total['pnl'] == pnl)
    pytest.assume(total['pnlRate'] == pnlRate)
    assert total['count'] == count
