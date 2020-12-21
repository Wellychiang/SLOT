from . import allure
from . import Base
from . import cms
from . import log
from . import pytest
from . import sle
from .bet_base import now_month
from .bet_base import now_day


@allure.feature('Scenario for bet little game and game report')
@allure.step('')
def test_search_for_creator_and_player(creator=('gamerecord01', 'gamerecord02', 'gamerecord03'),
                                        player='gamerecord04',
                                        amount=20,
                                        bet_count=1,
                                        lose=0,
                                        validBet=18.82,
                                        gainLose=18.82,
                                        assert_pnl=18.82,
                                        prizeWon=38.82,
                                        winRate=100,
                                        player_pnl=-20,
                                        player_validBet=0,
                                        player_prizeWon=0,
                                        who_win='CREATOR',
                                        creator_choice="HI",
                                        player_choice='LO',
                                        gameId="HL",
                                        HL_commission=5.9,
                                        report_start_month=now_month,
                                        report_start_day=now_day,
                                        report_end_month=now_month,
                                        report_end_day=now_day,):
    # 轉成timestamp
    todays_start, todays_end = Base().start_and_end_time(report_start_month,
                                                         report_start_day,
                                                         report_end_month,
                                                         report_end_day)

    cms.little_game_get_or_patch(method='patch',
                                 HL_commission=HL_commission)
    plus_button = 0
    little_games_reports = cms.little_game_record(startTime=todays_start,
                                                  endTime=todays_end,
                                                  userId=f'SL3{creator[plus_button]}')
    while len(little_games_reports['dataList']) != 0:
        plus_button += 1
        try:
            little_games_reports = cms.little_game_record(startTime=todays_start,
                                                          endTime=todays_end,
                                                          userId=f'SL3{creator[plus_button]}')
        except Exception as e:
            if str(e) == 'tuple index out of range':
                raise ValueError('Three users is already used')
    log(f'Use user: {creator[plus_button]}')

    _, get_token = sle.get_launch_token(creator[plus_button])
    game_create = sle.little_game_create(token=get_token['token'],
                                         amount=amount,
                                         choice=creator_choice,
                                         gameId=gameId,)

    if game_create.get('status') != None:
        raise ValueError(f'Creator: {creator[plus_button]}')

    _, get_token = sle.get_launch_token(player)
    game_play_result = sle.little_game_play(token=get_token['token'],
                                            choice=player_choice,
                                            gameId=gameId,
                                            roomId=game_create['roomId'])

    log('Search with creator')
    assert_game_report(user_search=f'SL3{creator[plus_button]}',
                       creator=f'SL3{creator[plus_button]}',
                       player=f'SL3{player}',
                       recordType='CREATOR',
                       amount=amount,
                       assert_pnl=assert_pnl,
                       validBet=validBet,
                       prizeWon=prizeWon,
                       who_win=who_win,
                       gameId=gameId,
                       start=todays_start,
                       end=todays_end,)

    log('Search with player')
    assert_game_report(user_search=f'SL3{player}',
                       creator=f'SL3{creator[plus_button]}',
                       player=f'SL3{player}',
                       recordType='PLAYER',
                       amount=amount,
                       assert_pnl=player_pnl,
                       validBet=player_validBet,
                       prizeWon=player_prizeWon,
                       who_win=who_win,
                       gameId=gameId,
                       start=todays_start,
                       end=todays_end,)


def assert_game_report(user_search='xxx',
                       creator='xxxx',
                       player='gamerecord04',
                       recordType='PLAYER',
                       amount=20,
                       assert_pnl=-20,
                       validBet=0,
                       prizeWon=0,
                       who_win='CREATOR',
                       gameId="HL",
                       start='timestamp',
                       end='timestamp',):

    little_games_reports = cms.little_game_record(startTime=start,
                                                  endTime=end,
                                                  userId=user_search,)
    report = little_games_reports['dataList'][0]

    log(f'\n{report}')
    pytest.assume(report['recordType'] == recordType)
    pytest.assume(report['gameId'] == gameId)
    pytest.assume(report['creatorUserId'] == creator)
    pytest.assume(report['playerUserId'] == player)
    # pytest.assume(report['roomId'] == game_play_result)
    pytest.assume(report['amount'] == amount)
    pytest.assume(report['validBet'] == validBet)
    pytest.assume(report['prizeWon'] == prizeWon)
    pytest.assume(report['pnl'] == assert_pnl)
    assert report['status'] == f'{who_win}_WIN'




