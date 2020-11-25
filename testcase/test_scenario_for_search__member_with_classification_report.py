# from testcase.test_try import bet, bet_feature, cms, sle, time
# from base import log, Base
# import pytest
# import allure

from testcase import cms, sle, time, log, Base, pytest
from testcase.test_try import bet, bet_feature



@pytest.mark.d
def test_get_together(username='yahoo',
                      result='410112,317,058,233,205,05',  # 自行開獎結果
                      gameId='NYTHAIFFC',
                      playType='STANDALONE',
                      betStrings=('1dtop,1', '1dtop,2'),
                      playId=90003,
                      playRateId=102332,
                      rebatePackage=1900,
                      stake=3,
                      times=1,
                      report_start_month=11,
                      report_start_day=24,
                      report_end_month=11,
                      report_end_day=24):
    # _, get_token = sle.get_token(username=username)
    #
    # response = bet_and_draw(token=get_token['token'],
    #                         result=result,
    #                         gameId=gameId,
    #                         playType=playType,
    #                         betStrings=betStrings,
    #                         playId=playId,
    #                         playRateId=playRateId,
    #                         rebatePackage=rebatePackage,
    #                         stake=stake,
    #                         times=times,)
    # log(response)

    todays_start, todays_end = Base().start_time_and_end_time(report_start_month,
                                                              report_start_day,
                                                              report_end_month,
                                                              report_end_day)

    infos = search_classification_report(gameId=gameId,
                                         end=todays_end,
                                         start=todays_start,
                                         userId=f'SL3{username}',
                                         username='wellyadmin')

    log(f'Infos length: {len(infos)}')

    for info_length in range(len(infos)):
        for info in infos[info_length]:
            print(info['gameName'])


    # for info in infos:
    #     pytest.assume(info['gameName'] == '泰国快乐彩')
    #     pytest.assume(betStrings[0][:2].title() in info['grp'])
    #     pytest.assume(betStrings[1][:2].title() in info['grp'])
    #     pytest.assume(info['betCount'] == len(betStrings))
    #     pytest.assume(info['stake'] == len(betStrings))
    #     pytest.assume(info['validBet'] == stake)
    #     pytest.assume(info['prizeWon'] == f'{stake * 3.2:.4f}')
    # for i in infos:
    #     print(i)
    # print(len(infos))


def search_classification_report(gameId, end, start, userId, username):
    response = cms.pnl_grp(end=end,
                           start=start,
                           userId=userId,
                           username=username)
    index = []
    for records in response['groupRecords']:
        for info in records['records']:
            if info['gameId'] == gameId:
                log(f'\nGame name:      {info["gameName"]}')
                log(f'Grp:              {info["grp"]}')
                log(f'Bet count:        {info["betCount"]}')
                log(f'Stake:            {info["stake"]}')
                log(f'Validate bet:     {info["validBet"]}')
                log(f'Won prize:        {info["prizeWon"]}\n')
            index.append(records['records'])
    return index


def reproduce_bet(token,
                gameId='NYTHAIFFC',
                playType='STANDALONE',
                betString='1dtop,1',
                playId=90003,
                playRateId=102332,
                rebatePackage=1900,
                stake=10,
                times=1):
    """
    Thaihappy:
        betString = playRateId
        3dtop|000 = 102328, 3d|roll = 102329,  playId = 90001
        2dtop|01 = 102330, 2d|bottom = 102331, playId = 90002
        1dtop|1 = 102332, 1d|bottom = 102333 playId = 90003
    """

    status_code, response = bet(gameId=gameId,
                                playType=playType,
                                betString=betString,
                                playId=playId,
                                playRateId=playRateId,
                                rebatePackage=rebatePackage,
                                stake=stake,
                                times=times,
                                token=token)


# 等到開獎倒數十秒, 就返回drawid等等, 小於十秒就等到下個round (十秒為預留給開獎的時間)
def wait_for_bet_and_return_previous_or_current(gameId):

    while True:
        response = sle.active_and_previous(gameId)
        count_down = response['current']['countdown']

        if count_down < 13000:
            time.sleep(13)
            log(f'Start to wait the new round')

        elif count_down >= 13000:
            start = time.time()
            log(f'Count down second: {int((count_down - 10000) / 1000)}')

            # sleep 到剩下5秒
            time.sleep(int((count_down-5000) / 1000))
            end = time.time()

            result = start - end

            log(f'Start: {start}\nEnd: {end}')
            log(f'Result: {result}')

            return response


def bet_and_draw(token,
                 result='410112,317,058,233,205,05',   # 自行開獎結果
                 gameId='NYTHAI3FC',
                 playType='STANDALONE',
                 betStrings=('3droll,012',),
                 playId=90001,
                 playRateId=102377,
                 rebatePackage=1870,
                 stake=3,
                 times=1):

    current_response = wait_for_bet_and_return_previous_or_current(gameId)

    log(f'Start bet')
    for betString in betStrings:
        _, response = bet(betString=betString,
                          gameId=gameId,
                          playType=playType,
                          playId=playId,
                          playRateId=playRateId,
                          rebatePackage=rebatePackage,
                          stake=stake,
                          times=times,
                          token=token)
        if len(response) != 1:
            raise ValueError('Bet failed')

    log('Start to draw the lottery')

    # Lottery draw
    status_code = cms.preset(drawId=current_response['current']['drawId'],
                             gameId=gameId,
                             result=result,)

    if status_code != 200:
        raise ValueError(f'Failed with lottery draw , put status code: {status_code}')

    return response








