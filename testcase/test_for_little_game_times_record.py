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
from testcase.bet_base import wait_for_bet_and_return_previous_or_current


@allure.feature("Scenario for times record's three options")
@allure.step('')
def test_three_options_to_search(amount=10,
                                 commission=5,
                                 commissionAmount=0.5,
                                 creator='timesrecord',
                                 player='timesrecord01',
                                 gameId='SC',
                                 creator_choice='HEAD',
                                 player_choice='TAIL',
                                 status='CREATOR_WIN',
                                 report_start_month=now_month,
                                 report_start_day=now_day,
                                 report_end_month=now_month,
                                 report_end_day=now_day,):
    # 轉成timestamp
    todays_start, todays_end = Base().start_and_end_time(report_start_month,
                                                         report_start_day,
                                                         report_end_month,
                                                         report_end_day)

    log('\nVerify commission to equal 5%, if not , update to 5%')
    little_games = cms.little_game_get_or_patch(method='get')

    if 5 != little_games[0]['commission']:
        status_code = cms.little_game_get_or_patch(method='patch', SC_commission=5)
        if status_code != 204:
            raise ValueError('Commission is not 5 and patch failed')
    else:
        log('\nCommission success')


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


    assert_times_record_with_which_search(roomId=game_play_result['roomId'],
                                          start=todays_start,
                                          end=todays_end,
                                          gameId=gameId,
                                          creator_choice=creator_choice,
                                          player_choice=player_choice,
                                          amount=amount,
                                          status=status,
                                          commission=commission,
                                          commissionAmount=commissionAmount)

    assert_times_record_with_which_search(creatorName=f'SL3{creator}',
                                          start=todays_start,
                                          end=todays_end,
                                          gameId=gameId,
                                          creator_choice=creator_choice,
                                          player_choice=player_choice,
                                          amount=amount,
                                          status=status,
                                          commission=commission,
                                          commissionAmount=commissionAmount)

    assert_times_record_with_which_search(playerName=f'SL3{player}',
                                          start=todays_start,
                                          end=todays_end,
                                          gameId=gameId,
                                          creator_choice=creator_choice,
                                          player_choice=player_choice,
                                          amount=amount,
                                          status=status,
                                          commission=commission,
                                          commissionAmount=commissionAmount)

def assert_times_record_with_which_search(roomId=None,
                                          creatorName=None,
                                          playerName=None,
                                          start=None,
                                          end=None,
                                          gameId=None,
                                          creator_choice=None,
                                          player_choice=None,
                                          amount=None,
                                          status=None,
                                          commission=None,
                                          commissionAmount=None):

    records = cms.little_game_times_record(roomId=roomId,
                                           creatorName=creatorName,
                                           playerName=playerName,
                                           start=start,
                                           end=end)
    record = records['records'][-1]

    log(record)
    pytest.assume(record['gameId'] == gameId)
    pytest.assume(record['creatorName'] == 'SL3timesrecord')
    pytest.assume(record['creatorPick'] == creator_choice)
    pytest.assume(record['playerName'] == 'SL3timesrecord01')
    pytest.assume(record['playerPick'] == player_choice)
    pytest.assume(record['amount'] == amount)
    pytest.assume(record['status'] == status)
    pytest.assume(record['commission'] == commission)
    assert record['commissionAmount'] == commissionAmount
