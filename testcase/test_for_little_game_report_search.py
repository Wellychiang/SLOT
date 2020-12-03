from testcase import cms, sle, time, log, Base, pytest, allure
from testcase.bet_base import bet, wait_and_lottery_draw, for_loop_bet_and_verify, now_month, now_day


@allure.feature('Scenario for ')
@allure.step('')
@pytest.mark.dd
def tes_tt(token):




    # Response: {'roomId': 1272084216604354, 'status': 'LOSE', 'creatorPick': 'HEAD', 'amountResult': -10.0}
    # Response: {'roomId': 1272087638083305, 'status': 'WIN', 'creatorPick': 'HEAD', 'amountResult': 9.5}


    little_games_reports = cms.little_game_record()

    print((little_games_report['roomId'] for little_games_report in little_games_reports['dataList']))

    assert 1271981426123892 in (little_games_report['roomId'] for little_games_report in little_games_reports['dataList'])


