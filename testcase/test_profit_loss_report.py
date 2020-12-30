from . import allure
from . import Base
from . import cms
from . import sle
from . import time
from . import pytest
from . import log
from .bet_base import bet
from . import ROOT_ACCOUNT
from .bet_base import for_loop_bet_and_verify
from .bet_base import now_month
from .bet_base import now_day
from .bet_base import wait_and_lottery_draw


@allure.feature(f"Scenario for search game profit loss report after bet")
def test_game_profit_loss_report(username=('welly1',),
                                 result='000001|111|111|222|222|45',
                                 vendorId='MX2',
                                 gameName='泰国快乐彩',
                                 notPresetPnl=0,
                                 odds=920,
                                 isSelfOpen=True,
                                 betStrings=('3dtop|001', '3dtop|002', '3dtop|003', '3dtop|004', '3dtop|005',
                                             '3dtop|006', '3dtop|007', '3dtop|008', '3dtop|009', '3dtop|010',),
                                 gameId='NYTHAIFFC',
                                 playType='STANDALONE',
                                 playId=90001,
                                 playRateId=102328,
                                 rebatePackage=1980,
                                 stake=1, ):
    start, end = Base().start_and_end_time(now_month, now_day, now_month, now_day)

    origin_report = cms.game_profit_report(start=start, end=end, gameId=f'{gameId}|{playType}')

    wait_and_lottery_draw(result=result,
                          gameId=gameId,
                          count_down_second=22)

    _, token = sle.get_launch_token(username[0])
    for_loop_bet_and_verify(token=token['token'],
                            gameId=gameId,
                            playType=playType,
                            betStrings=betStrings,
                            playId=playId,
                            playRateId=playRateId,
                            rebatePackage=rebatePackage,
                            stake=stake, )

    now_start_time = Base().return_now_start_time()
    report = wait_for_game_profit_report_info_update(start, end, gameId, playType, origin_report, now_start_time)

    assert_the_game_profit_report_with_thai(report,
                                            gameId,
                                            vendorId,
                                            playType,
                                            gameName,
                                            betUserCount=len(username),
                                            betCount=len(betStrings),
                                            stake=stake * len(betStrings),
                                            validBet=stake*len(betStrings),
                                            prizeWon=stake*odds,
                                            notPresetPnl=notPresetPnl,
                                            pnl=(stake*odds)-len(betStrings),
                                            pnlRate=((stake*odds)-len(betStrings)) / 10,
                                            isSelfOpen=isSelfOpen,
                                            count=len(report['records']))


def wait_for_game_profit_report_info_update(start, end, gameId, playType, origin_report, now_start_time):
    report = cms.game_profit_report(start=start, end=end, gameId=f'{gameId}|{playType}')
    times = 0
    while report['records'][0]['betCount'] == origin_report['records'][0]['betCount']:
        log(f'Record update now, wait a minute')
        times += 1
        time.sleep(10)
        report = cms.game_profit_report(start=start, end=end, gameId=f'{gameId}|{playType}')

        if times > 6:
            raise ValueError(f"It's too slow too load in the game profit report")

    report = cms.game_profit_report(start=now_start_time, end=end, gameId=f'{gameId}|{playType}')

    return report






def assert_the_game_profit_report_with_thai(report,
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
    pytest.assume(info['presetValidBet'] == validBet)
    pytest.assume(info['prizeWon'] == prizeWon)
    pytest.assume(info['notPresetPnl'] == notPresetPnl)
    pytest.assume(info['pnl'] == pnl)
    pytest.assume(info['pnlRate'] == pnlRate)
    pytest.assume(info['isSelfOpen'] == isSelfOpen)

    pytest.assume(total['betCount'] == betCount)
    pytest.assume(total['stake'] == stake)
    pytest.assume(total['presetValidBet'] == validBet)
    pytest.assume(total['validBet'] == validBet)
    pytest.assume(total['prizeWon'] == prizeWon)
    pytest.assume(total['notPresetPnl'] == notPresetPnl)
    pytest.assume(total['pnl'] == pnl)
    pytest.assume(total['pnlRate'] == pnlRate)
    assert total['count'] == count
