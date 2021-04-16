from . import allure
from . import Base
from . import cms
from . import log
from . import pytest
from . import sle
from . import ROOT_ACCOUNT
from . import time
from .bet_base import now_month
from .bet_base import now_day


@allure.feature("Scenario for check little game's profit loss report")
@allure.step('')
def test_little_game_profit_loss_report(amount=10,
                                         commission=3.3,
                                         creator='timesrecord',
                                         player='timesrecord01',
                                         gameId='SC',
                                         creator_choice='HEAD',
                                         player_choice='TAIL',
                                         odds=0.33,
                                         currency='CNY',
                                         report_start_month=now_month,
                                         report_start_day=now_day,
                                         report_end_month=now_month,
                                         report_end_day=now_day, ):
    todays_start, todays_end = Base().start_and_end_time(report_start_month,
                                                         report_start_day,
                                                         report_end_month,
                                                         report_end_day)

    log(f'\nVerify commission to equal {commission}%, if not , update to {commission}%')
    little_games = cms.little_game_get_or_patch(method='get')

    if commission != little_games[0]['commission']:
        status_code = cms.little_game_get_or_patch(method='patch', SC_commission=commission)
        if status_code != 204:
            raise ValueError(f'Commission is not {commission} and patch failed')
    else:
        log('\nCommission success')

    start = Base().return_now_start_time()

    _, get_token = sle.get_launch_token(creator)
    game_create = sle.little_game_create(token=get_token['token'],
                                         amount=amount,
                                         choice=creator_choice,
                                         gameId=gameId)

    _, get_token = sle.get_launch_token(player)
    game_play_result = sle.little_game_play(token=get_token['token'],
                                            choice=player_choice,
                                            gameId=gameId,
                                            roomId=game_create['roomId'])
    pytest.assume(game_play_result['roomId'] == game_create['roomId'])
    pytest.assume(game_play_result['status'] == 'LOSE')
    pytest.assume(game_play_result['creatorPick'] == 'HEAD')
    pytest.assume(game_play_result['amountResult'] == -amount)

    report = wait_and_verify_lg_profit_loss_report(start, end=todays_end, username=ROOT_ACCOUNT)

    assert_lg_profit_loss_info(report,
                               amount,
                               validBet=amount - odds,
                               prizeWon=amount + amount - odds,
                               pnl=odds,
                               accountCount=2,
                               recordCount=2,
                               currency=currency)


def wait_and_verify_lg_profit_loss_report(start, end, username):
    report = cms.lg_profit_loss_report(start, end, username=username)

    times = 0
    while report['dataList'][0]['amount'] == 0:
        log(f"Wait report updated")
        time.sleep(10)
        times += 1

        report = cms.lg_profit_loss_report(start, end, username=username)
        if times > 6:
            raise ValueError("It's too slow to load in little game profit loss report")

    return report


def assert_lg_profit_loss_info(report, amount, validBet, prizeWon, pnl, accountCount, recordCount, currency):
    data = report['dataList'][0]

    pytest.assume(data['amount'] == amount)
    pytest.assume(data['validBet'] == validBet)
    pytest.assume(data['prizeWon'] == prizeWon)
    pytest.assume(data['pnl'] == pnl)
    pytest.assume(data['accountCount'] == accountCount)
    pytest.assume(data['recordCount'] == recordCount)
    pytest.assume(data['currency'] == currency)

