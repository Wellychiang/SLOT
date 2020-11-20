from testcase.test_try import bet, bet_feature, cms, sle, time
from base import log
import pytest
import allure


# _, get_token = sle.get_token()


@pytest.mark.d
def test_sss(token,
             gameId='NYTHAIFFC',
            playType='STANDALONE',
            betString='3dtop|000',
            playId=90001,
            playRateId=102328,
            rebatePackage=1900,
            stake=10,
            times=1,
            ):

    bet(gameId='NYTHAIFFC',
        playType='STANDALONE',
        betString='3dtop|000',
        playId=90001,
        playRateId=102328,
        rebatePackage=1900,
        stake=10,
        times=1,
        token=token)


@allure.feature(bet_feature)
@allure.step('')
@pytest.mark.dd
def test_bet_for_Thai_happy(token,
                            gameId='NYTHAIFFC',
                            playType='STANDALONE',
                            betString='3dtop|000',
                            playId=90001,
                            playRateId=102328,
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


@pytest.mark.dd
def cms_lottery_draw_management(gameId='NYTHAIFFC',
                                startBefore=int(float(time.time())*1000),   # 開獎日期
                                drawIdString=202011181092,                  # 獎號 (可以為None, 會變成查詢所有開獎)
                                username='wellyadmin'):

    status_code, response = cms.MX2(gameId=gameId,
                                    startBefore=startBefore,
                                    drawIdString=drawIdString,
                                    username=username,)

    return response


@pytest.mark.dd
def test_for_scenario(token,
                      result='1|2|3|4|5',   # 自行開獎結果
                      gameId='NYSSC3F',
                      playType='SIMPLE',
                      betString='sum|small',
                      playId=17,
                      playRateId=16791,   # 28 = top, 29 = roll
                      rebatePackage=1900,
                      stake=10,
                      times=1):

    current_response = wait_for_bet_and_return_previous_or_current(gameId)

    log(f'Start bet')
    _, response = bet(betString=betString,
                      gameId=gameId,
                      playType=playType,
                      playId=playId,
                      playRateId=playRateId,
                      rebatePackage=rebatePackage,
                      stake=stake,
                      times=times,
                      token=token)

    log('Start to draw the lottery')

    cms.preset(drawId=current_response['current']['drawId'],
               gameId=gameId,
               result=result,)

    response = cms_lottery_draw_management(gameId=gameId,
                                           startBefore=int(float(time.time()) * 1000),
                                           drawIdString=current_response['current']['drawIdString'],
                                           username='wellyadmin')

    log(f'Show management response: {response["data"]}')


# 等到開獎倒數十秒, 並返回drawid等等, 小於十秒就等到下個round
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


@pytest.mark.dd
def lottery_draw(drawId=None,
                 gameId="NYSSC3F",
                 result="1|2|3|4|5"):

    response = sle.active_and_previous(gameId)

    print(response['current']['drawId'])
    cms.preset(drawId,
               gameId,
               result)
