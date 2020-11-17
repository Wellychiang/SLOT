from base.base import log, Base
from base.base_cms import Cms
from base.base_sle import Sle
import pytest
import allure
import time
import re

cms = Cms()
sle = Sle()
_, get_token = sle.get_token()

bet_feature = 'Bet'


@allure.feature('Cms')
@pytest.mark.skip
def test_cms():
    strftimes = (time.strftime('%Y-%m-%d') + ' 00:00:00', time.strftime('%Y-%m-%d') + ' 23:59:59')

    for strftime in strftimes:
        strptime = time.strptime(strftime, '%Y-%m-%d %H:%M:%S')
        if strftime == strftimes[0]:
            todays_start = time.mktime(strptime)
        else:
            todays_end = time.mktime(strptime)

    # print(int(todays_start*1000), int((todays_end+0.999)*1000))
    status_code, response = cms.txn_reports(tm_start=int(todays_start*1000), tm_end=int((todays_end+0.999)*1000))

    """Not done"""
    print(f'response: {len(response["data"])}')


def bet(drawId=int(time.strftime('%Y%m%d')+'00429'),
        gameId='NYSSC3F',  # NYSSC3F, NYSSC15F
        platform='Desktop',
        playType='SIMPLE',
        betString='sum|small',
        comment='',
        playId=17,
        playRateId=16080,
        rebatePackage=1980,
        stake=10,
        times=1,
        unit='DOLLAR',
        token=None):

    status_code, response = sle.bet(drawId,
                                    gameId,
                                    platform,
                                    playType,
                                    betString,
                                    comment,
                                    playId,
                                    playRateId,
                                    rebatePackage,
                                    stake,
                                    times,
                                    unit,
                                    token)
    # 先打一次錯誤的drawid, response會丟給我正確的, 再打
    drawid = re.findall('id (.*) !', response['message'])

    if 'Argument error-> argument name: drawid, message: Current draw id' in response['message']:
        draw = drawid[0]

        log(f'drawId: {drawId}')
        status_code, response = sle.bet(draw,
                                        gameId,
                                        platform,
                                        playType,
                                        betString,
                                        comment,
                                        playId,
                                        playRateId,
                                        rebatePackage,
                                        stake,
                                        times,
                                        unit,
                                        token)
    return status_code, response


@allure.feature(bet_feature)
@allure.step('')
@pytest.mark.Bet
def test_bet_for_rebate_packages(rebatePackages=(1980,
                                                 1800,
                                                 1981,
                                                 1799,
                                                 '1'*20,
                                                 '####',
                                                 '我是中文',
                                                 '',
                                                 ' ',
                                                 'english'),):

    for rebatePackage in rebatePackages:

        if rebatePackage in rebatePackages[2:4]:
            status_code, response = bet(rebatePackage=rebatePackage, token=get_token['token'])

            pytest.assume(response['status'] == 400)
            pytest.assume(response['error'] == 'Bad Request')
            pytest.assume(response['message'] == 'Argument error-> argument name: rebate, message: invalid rebate')
            pytest.assume(response['errCode'] == 400)
            pytest.assume(response['code'] == 'param.txns[].rebate.invalid')
            pytest.assume(response['values'] == [])

        elif rebatePackage in rebatePackages[4:]:
            try:
                bet(rebatePackage=rebatePackage, token=get_token['token'])
            except ValueError as e:
                log(f'I need three errors: {e}')
                pytest.assume(str(e) == 'Expecting value: line 1 column 1 (char 0)')
        else:
            status_code, response = bet(rebatePackage=rebatePackage, token=get_token['token'])

            pytest.assume(status_code == 200)
            pytest.assume(len(response) == 1)
            pytest.assume([len(str(i)) for i in response] == [16])


@allure.feature(bet_feature)
@allure.step('')
@pytest.mark.Bet
def test_bet_for_game_id(gameIds=('NYSSC3F', 'nyssc3f', '1'*20, '####', '我是中文', '', ' ', 'english')):

    for gameId in gameIds:
        if gameId not in  gameIds[:2]:
            status_code, response = bet(gameId=gameId, token=get_token['token'])

            pytest.assume(response['status'] == 400)
            pytest.assume(response['error'] == 'Bad Request')
            pytest.assume(response['message'] == 'Argument error-> argument name: gameid, message: invalid gameid')
            pytest.assume(response['errCode'] == 400)
            pytest.assume(response['code'] == 'param.gameid.invalid')
            pytest.assume(response['values'] == [])

        elif gameId == gameIds[1]:
            try:
                bet(gameId=gameId, token=get_token['token'])
            except Exception as e:

                pytest.assume(str(e) == 'Expecting value: line 1 column 1 (char 0)')

        else:
            status_code, response = bet(gameId=gameId, token=get_token['token'])

            pytest.assume(status_code == 200)
            pytest.assume(len(response) == 1)
            pytest.assume([len(str(i)) for i in response] == [16])


@allure.feature(bet_feature)
@allure.step('')
@pytest.mark.skip('Lower priority')
# Not done yet
def test_bet_for_game_platform(platforms=('1'*20, 'Hi,im welly', '我是', '', ' ', '1'*21)):

    for platform in platforms:
        if platform != platforms[5]:
            status_code, response = bet(platform=platform, token=get_token['token'])

            pytest.assume(status_code == 200)
            pytest.assume(len(response) == 1)
            pytest.assume([len(str(i)) for i in response] == [16])

        else:
            try:
                bet(platform=platform, token=get_token['token'])
            except Exception as e:

                pytest.assume(str(e) == 'Expecting value: line 1 column 1 (char 0)')


@allure.feature(bet_feature)
@allure.step('')
@pytest.mark.Bet
def test_bet_for_game_platType(playTypes=('SIMPLE', '1'*20, '####', '我是中文', '', ' ', 'english'),):

    for playType in playTypes:
        if playType != playTypes[0]:
            try:
                bet(playType=playType, token=get_token['token'])
            except Exception as e:

                pytest.assume(str(e) == 'Expecting value: line 1 column 1 (char 0)')

        else:
            status_code, response = bet(playType=playType, token=get_token['token'])

            pytest.assume(status_code == 200)
            pytest.assume(len(response) == 1)
            pytest.assume([len(str(i)) for i in response] == [16])


@allure.feature(bet_feature)
@allure.step('')
@pytest.mark.Bet
# sum|small = 16080, sum|big = 16790, sum|odd = 16792, sum|even = 16793
def test_bet_for_game_betString(betStrings=('sum|small', '', '1'*20, '####', '我是中文', ' ', 'english')):

    for betString in betStrings:
        if betString not in betStrings[:2]:
            status_code, response = bet(betString=betString, token=get_token['token'])

            pytest.assume(status_code == 400)
            pytest.assume(response['status'] == 400)
            pytest.assume(response['error'] == 'Bad Request')
            pytest.assume(response['message'] == 'Argument error-> argument name: txn, message: invalid')
            pytest.assume(response['errCode'] == 400)
            pytest.assume(response['code'] == 'param.txn.invalid')
            pytest.assume(response['values'] == [])

        elif betString == betStrings[1]:
            status_code, response = bet(betString=betString, token=get_token['token'])

            pytest.assume(status_code == 400)
            pytest.assume(response['status'] == 400)
            pytest.assume(response['error'] == 'Bad Request')
            pytest.assume(response['message'] == 'Argument error-> argument name: betstring, message: invalid betstring' \
                                                 ':  for game:NYSSC3F')
            pytest.assume(response['errCode'] == 400)
            pytest.assume(response['code'] == 'param.txns[].betstring.invalid')
            pytest.assume(response['values'] == [])

        else:
            status_code, response = bet(betString=betString, token=get_token['token'])

            pytest.assume(status_code == 200)
            pytest.assume(len(response) == 1)
            pytest.assume([len(str(i)) for i in response] == [16])


@allure.feature(bet_feature)
@allure.step('')
@pytest.mark.skip('Lower priority, comments can not see the different and even invalid input can input')
def test_bet_for_game_comment(comments=('1'*99, '123', '#@$$%')):

    for comment in comments:
        bet(comment=comment, token=get_token['token'])


@allure.feature(bet_feature)
@allure.step('')
@pytest.mark.Bet
def test_bet_for_game_playId(playIdd=range(1, 50),
                             playIds=(17, '', '1'*20, '####', '我是中文', ' ', 'english')):

    for playId in playIds:

        if playId not in playIds[:2]:
            try:
                bet(playId=playId, token=get_token['token'])
            except ValueError as e:

                pytest.assume(str(e) == 'Expecting value: line 1 column 1 (char 0)')

        elif playId == playIds[1]:

            status_code, response = bet(playId=playId, token=get_token['token'])

            pytest.assume(status_code == 400)
            pytest.assume(response['status'] == 400)
            pytest.assume(response['error'] == 'Bad Request')
            pytest.assume(response['message'] == 'Argument error-> argument name: playid,' \
                                          ' message: invalid playid: 0 for game:NYSSC3F')
            pytest.assume(response['errCode'] == 400)
            pytest.assume(response['code'] == 'param.txns[].playid.invalid')
            pytest.assume(response['values'] == [])

        else:
            status_code, response = bet(playId=playId, token=get_token['token'])

            pytest.assume(status_code == 200)
            pytest.assume(len(response) == 1)
            pytest.assume([len(str(i)) for i in response] == [16])

    for playid in playIdd:

        if playid in range(18, 23):
            status_code, response = bet(playId=playid, token=get_token['token'])

            pytest.assume(status_code == 400)
            pytest.assume(response['status'] == 400)
            pytest.assume(response['error'] == 'Bad Request')
            pytest.assume(response['message'] == 'Argument error-> argument name: playid, '
                                                 'message: playid not in playrate')
            pytest.assume(response['errCode'] == 400)
            pytest.assume(response['code'] == 'param.txns[].playid.invalid')
            pytest.assume(response['values'] == [])

        elif playid != 17:
            status_code, response = bet(playId=playid, token=get_token['token'])

            pytest.assume(status_code == 400)
            pytest.assume(response['status'] == 400)
            pytest.assume(response['error'] == 'Bad Request')
            pytest.assume(response['message'] == 'Argument error-> argument name: playid,'
                                                 f' message: invalid playid: {playid} for game:NYSSC3F')
            pytest.assume(response['errCode'] == 400)
            pytest.assume(response['code'] == 'param.txns[].playid.invalid')
            pytest.assume(response['values'] == [])

        else:
            status_code, response = bet(playId=playid, token=get_token['token'])

            pytest.assume(status_code == 200)
            pytest.assume(len(response) == 1)
            pytest.assume([len(str(i)) for i in response] == [16])


@allure.feature(bet_feature)
@allure.step('')
@pytest.mark.Bet
def test_bet_for_game_playRateId(playRateIds=range(16080, 16090),
                                 playRateIdd=('', '1'*20, '####', '我是中文', ' ', 'english')):

    for playRateId in playRateIds:
        if playRateId != playRateIds[0]:

            status_code, response = bet(playRateId=playRateId, token=get_token['token'])

            pytest.assume(status_code == 400)
            pytest.assume(response['status'] == 400)
            pytest.assume(response['error'] == 'Bad Request')
            pytest.assume(response['message'] == 'Argument error-> argument name: txn, '
                                                 'message: invalid')
            pytest.assume(response['errCode'] == 400)
            pytest.assume(response['code'] == 'param.txn.invalid')
            pytest.assume(response['values'] == [])

        else:
            status_code, response = bet(playRateId=playRateId, token=get_token['token'])

            pytest.assume(status_code == 200)
            pytest.assume(len(response) == 1)
            pytest.assume([len(str(i)) for i in response] == [16])

    for playrateid in playRateIdd:
        try:
            bet(playRateId=playrateid, token=get_token['token'])

        except ValueError as e:
            pytest.assume(str(e) == 'Expecting value: line 1 column 1 (char 0)')


@allure.feature(bet_feature)
@allure.step('')
@pytest.mark.Bet
def test_bet_for_game_stake(stakes=('10', '1'*20,  '', '####', '我是中文', ' ', 'english')):

    for stake in stakes:
        if stake == stakes[1]:

            status_code, response = bet(stake=stake, token=get_token['token'])

            pytest.assume(status_code == 400)
            pytest.assume(response['status'] == 400)
            pytest.assume(response['error'] == 'Bad Request')
            pytest.assume(response['message'] == 'Argument error-> argument name: risk, '
                                                 'message: not pass risk validation')
            pytest.assume(response['errCode'] == 400)
            pytest.assume(response['code'] == 'risk.exceed.by.player.total.stake')
            pytest.assume(response['values'] == [50000])

        elif stake not in stakes[:2]:
            try:
                bet(stake=stake, token=get_token['token'])
            except ValueError as e:
                pytest.assume(str(e) == 'Expecting value: line 1 column 1 (char 0)')

        else:
            status_code, response = bet(stake=stake, token=get_token['token'])

            pytest.assume(status_code == 200)
            pytest.assume(len(response) == 1)
            pytest.assume([len(str(i)) for i in response] == [16])


@allure.feature(bet_feature)
@allure.step('')
@pytest.mark.Bet
def test_bet_for_game_times(timeses=(3, '', ' ', '1'*20, '####', '我是中文', 'english')):

    for times in timeses:
        if times in timeses[3:]:
            try:
                bet(times=times, token=get_token['token'])

            except ValueError as e:

                pytest.assume(str(e) == 'Expecting value: line 1 column 1 (char 0)')

        elif times in timeses[1:3]:
            status_code, response = bet(times=times, token=get_token['token'])

            pytest.assume(status_code == 400)
            pytest.assume(response['status'] == 400)
            pytest.assume(response['error'] == 'Bad Request')
            pytest.assume(response['message'] == 'Argument error-> argument name: times, message: invalid times')
            pytest.assume(response['errCode'] == 400)
            pytest.assume(response['code'] == 'param.txns[].times.invalid')
            pytest.assume(response['values'] == [])

        else:
            status_code, response = bet(times=times, token=get_token['token'])

            pytest.assume(status_code == 200)
            pytest.assume(len(response) == 1)
            pytest.assume([len(str(i)) for i in response] == [16])


@allure.feature(bet_feature)
@allure.step('')
@pytest.mark.Bet
def test_bet_for_game_unit(units=('DOLLAR', '', ' ', '1'*20, '####', '刀惹', 'english'.upper())):

    for unit in units:
        if unit != units[0]:
            try:
                bet(unit=unit, token=get_token['token'])

            except ValueError as e:
                print(str(e))

                pytest.assume(str(e) == 'Expecting value: line 1 column 1 (char 0)')
        else:
            status_code, response = bet(unit=unit, token=get_token['token'])

            pytest.assume(status_code == 200)
            pytest.assume(len(response) == 1)
            pytest.assume([len(str(i)) for i in response] == [16])


@allure.feature(bet_feature)
@allure.step('')
@pytest.mark.dd
def test_bet_for_thai(gameId='NYTHAIFFC',
                      playType='STANDALONE',
                      betStrings=('3dtop|000', '3droll|000'),
                      playId=90001,
                      playRateId=102328,   # 28 = top, 29 = roll
                      rebatePackage=1900,
                      stake=10,
                      times=1):
    """
    betString:
    3dtop|000 = 102328, 3d|small = 102329,  playId = 90001
    2dtop|01 = 102330, 2d|bottom = 102331, playId = 90002
    1dtop|1 = 102332, 1d|bottom = 102333 playId = 90003
    """
    for betString in betStrings:
        bet(betString=betString,
            gameId=gameId,
            playType=playType,
            playId=playId,
            playRateId=playRateId,
            rebatePackage=rebatePackage,
            stake=stake,
            times=times,
            token=get_token['token'])



