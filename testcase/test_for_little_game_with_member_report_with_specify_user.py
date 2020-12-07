from testcase import cms, sle, time, log, Base, pytest, allure
from testcase.bet_base import bet, wait_and_lottery_draw, for_loop_bet_and_verify, now_month, now_day


@allure.feature("Scenario for little game HL bet and member report")
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

    members_report = cms.little_game_members_report(userId=f'SL3{creator[0]}',
                                                    start=todays_start,
                                                    end=todays_end)

    little_games = cms.little_game_get_or_patch(method='get')

    log('\nVerify commission to equal 5.9%, if not, update to 5.9%')
    if HL_commission != little_games[2]['commission']:
        status_code = cms.little_game_get_or_patch(method='patch', HL_commission=HL_commission)
        if status_code != 204:
            raise ValueError(f'Commission is not 5.9% and patch failed')
        log('\nCommission update')
    else:
        log('\nCommission success')


    change_button = 0
    while len(members_report['records']) != 0:
        change_button += 1
        members_report = cms.little_game_members_report(userId=f'SL3{creator[change_button]}',
                                                        start=todays_start,
                                                        end=todays_end)
    log(f'\nCreator: {creator[change_button]}')

    _, get_token = sle.get_launch_token(creator[change_button])
    game_create = sle.little_game_create(token=get_token['token'],
                                         amount=amount,
                                         choice=creator_choice,
                                         gameId=gameId, )

    _, get_token = sle.get_launch_token(player)
    game_play_result = sle.little_game_play(token=get_token['token'],
                                            choice=player_choice,
                                            gameId=gameId,
                                            roomId=game_create['roomId'])

    pytest.assume(game_play_result['creatorPick'] == game_create['creatorPick'])
    pytest.assume(game_play_result['roomId'] == game_create['roomId'])
    pytest.assume(game_play_result['status'] == 'LOSE')
    pytest.assume(game_play_result['amountResult'] == -amount)

    members_report = cms.little_game_members_report(userId=f'SL3{creator[change_button]}',
                                                    start=todays_start,
                                                    end=todays_end)

    report = members_report['records'][0]

    pytest.assume(report['betCount'] == bet_count)
    pytest.assume(report['win'] == bet_count)
    pytest.assume(report['lose'] == lose)
    pytest.assume(report['betAmount'] == amount)
    pytest.assume(report['validBet'] == validBet)
    pytest.assume(report['prizeWon'] == prizeWon)
    pytest.assume(report['gainLose'] == gainLose)
    assert report['winRate'] == winRate
