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


@allure.feature('Scenario for search specify user game report')
@allure.step('')
def test_search_user_game_report(username=('gamereport01', 'gamereport02', 'gamereport03', 'gamereport04'),
                                 vendorId='MX2',
                                 result='000001|111|111|222|222|45',
                                 betStrings=('3dtop|001', '3dtop|002', '3dtop|003', '3dtop|004', '3dtop|005',
                                             '3dtop|006', '3dtop|007', '3dtop|008', '3dtop|009', '3dtop|010',),
                                 gameId='NYTHAIFFC',
                                 playType='STANDALONE',
                                 gameStatus='ACTIVE',
                                 playId=90001,
                                 playRateId=102328,
                                 rebatePackage=1980,
                                 stake=1,
                                 odds=920,):
    start, end = Base().start_and_end_time(now_month, now_day, now_month, now_day)

    cms.games_close_or_open(username=ROOT_ACCOUNT,
                            gameId=gameId,
                            playType=playType,
                            gameStatus=gameStatus, )

    switch_button = switch_user_if_user_used(start, end, username)

    wait_and_lottery_draw(result=result,
                          gameId=gameId,
                          count_down_second=20)

    _, token = sle.get_launch_token(username[switch_button])
    for_loop_bet_and_verify(token=token['token'],
                            gameId=gameId,
                            playType=playType,
                            betStrings=betStrings,
                            playId=playId,
                            playRateId=playRateId,
                            rebatePackage=rebatePackage,
                            stake=stake, )

    game_report = wait_for_the_game_report(start, end, username, switch_button)

    assert_game_report(game_report,
                       vendorId,
                       username,
                       betCount=len(betStrings),
                       stake=stake * len(betStrings),
                       validBet=stake * len(betStrings),
                       prizeWon=stake * odds,
                       pnl=(stake * odds) - len(betStrings),
                       pnlRate=int((stake * odds - len(betStrings)) / 10),
                       switch_button=switch_button)


def switch_user_if_user_used(start, end, username):
    game_report = cms.game_report(end=end,
                                  limit=5,
                                  start=start,
                                  userId=f'SL3{username[0]}', )

    switch_button = 0
    while len(game_report['records']) != 0:
        switch_button += 1
        game_report = cms.game_report(end=end,
                                      limit=5,
                                      start=start,
                                      userId=f'SL3{username[switch_button]}', )

    log(f"Use user: {username[switch_button]}")
    return switch_button


def wait_for_the_game_report(start, end, username, switch_button):
    game_report = cms.game_report(end=end,
                                  limit=5,
                                  start=start,
                                  userId=f'SL3{username[switch_button]}', )

    times = 0
    while game_report['records'] is None or len(game_report['records']) == 0:
        time.sleep(10)
        times += 1
        game_report = cms.game_report(end=end,
                                      limit=5,
                                      start=start,
                                      userId=f'SL3{username[switch_button]}', )
        if times > 6:
            raise ValueError(f'Too slow to load in report, it spend 60 seconds')

    return game_report


def assert_game_report(game_report,
                       vendorId,
                       username,
                       betCount,
                       stake,
                       validBet,
                       prizeWon,
                       pnl,
                       pnlRate,
                       switch_button):
    data = game_report['records'][0]

    assert data['vendorId'] == vendorId
    assert data['userId'] == f'SL3{username[switch_button]}'
    assert data['betUserCount'] is None
    assert data['betCount'] == betCount
    assert data['txnCount'] is None
    assert data['stake'] == stake
    assert data['validBet'] == validBet
    assert data['presetValidBet'] is None
    assert data['prizeWon'] == prizeWon
    assert data['notPresetPnl'] is None
    assert data['pnl'] == pnl
    assert data['pnlRate'] == pnlRate
