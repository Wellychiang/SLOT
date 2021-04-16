from . import allure
from . import Base
from . import cms
from . import log
from . import pytest
from . import sle
from .bet_base import now_month
from .bet_base import now_day


@allure.feature("Scenario for use lg's member report to search specify member")
@allure.step('')
def test_member_search_success_normally(creator=('memberreport1', 'memberreport2', 'memberreport3'),
                                        player='memberreport',
                                        amount=20,
                                        bet_count=1,
                                        lose=0,
                                        validBet=18.82,
                                        gainLose=18.82,
                                        prizeWon=38.82,
                                        winRate=100,
                                        creator_choice="HI",
                                        player_choice='LO',
                                        gameId="HL",
                                        HL_commission=5.9,
                                        report_start_month=now_month,
                                        report_start_day=now_day,
                                        report_end_month=now_month,
                                        report_end_day=now_day):
    # 轉成timestamp
    todays_start, todays_end = Base().start_and_end_time(report_start_month,
                                                         report_start_day,
                                                         report_end_month,
                                                         report_end_day)
    update_commission_to_5dot9(HL_commission)

    change_button = change_user_if_used(creator, todays_start, todays_end)

    game_create, game_play_result = game_create_and_play(creator[change_button],
                                                         player,
                                                         amount,
                                                         creator_choice,
                                                         player_choice,
                                                         gameId)

    assert_create_and_play_result(game_create, game_play_result, amount)

    assert_specify_member_info_in_little_game_report(f'SL3{creator[change_button]}',
                                                     todays_start,
                                                     todays_end,
                                                     bet_count,
                                                     lose,
                                                     amount,
                                                     validBet,
                                                     prizeWon,
                                                     gainLose,
                                                     winRate)


def update_commission_to_5dot9(HL_commission):
    little_games = cms.little_game_get_or_patch(method='get')

    log('\nVerify commission to equal 5.9%, if not, update to 5.9%')
    if HL_commission != little_games[2]['commission']:
        status_code = cms.little_game_get_or_patch(method='patch', HL_commission=HL_commission)
        if status_code != 204:
            raise ValueError(f'Commission is not 5.9% and patch failed')
        log('\nCommission update')
    else:
        log('\nCommission success')


def change_user_if_used(userId, start, end):
    members_report = cms.little_game_members_report(userId=f'SL3{userId[0]}',
                                                    start=start,
                                                    end=end)
    change_button = 0
    while len(members_report['records']) != 0:
        change_button += 1
        members_report = cms.little_game_members_report(userId=f'SL3{userId[change_button]}',
                                                        start=start,
                                                        end=end)
    log(f'\nCreator: {userId[change_button]}')

    return change_button


def game_create_and_play(creator, player, amount, creator_choice, player_choice, gameId):
    _, get_token = sle.get_launch_token(creator)
    game_create = sle.little_game_create(token=get_token['token'],
                                         amount=amount,
                                         choice=creator_choice,
                                         gameId=gameId, )

    _, get_token = sle.get_launch_token(player)
    game_play_result = sle.little_game_play(token=get_token['token'],
                                            choice=player_choice,
                                            gameId=gameId,
                                            roomId=game_create['roomId'])

    return game_create, game_play_result


def assert_create_and_play_result(game_create, game_play_result, amount):
    pytest.assume(game_play_result['creatorPick'] == game_create['creatorPick'])
    pytest.assume(game_play_result['roomId'] == game_create['roomId'])
    pytest.assume(game_play_result['status'] == 'LOSE')
    pytest.assume(game_play_result['amountResult'] == -amount)


def assert_specify_member_info_in_little_game_report(userId,
                                                     start,
                                                     end,
                                                     bet_count,
                                                     lose,
                                                     amount,
                                                     validBet,
                                                     prizeWon,
                                                     gainLose,
                                                     winRate):

    members_report = cms.little_game_members_report(userId=userId, start=start, end=end)
    report = members_report['records'][0]

    pytest.assume(report['betCount'] == bet_count)
    pytest.assume(report['win'] == bet_count)
    pytest.assume(report['lose'] == lose)
    pytest.assume(report['betAmount'] == amount)
    pytest.assume(report['validBet'] == validBet)
    pytest.assume(report['prizeWon'] == prizeWon)
    pytest.assume(report['gainLose'] == gainLose)
    assert report['winRate'] == winRate
