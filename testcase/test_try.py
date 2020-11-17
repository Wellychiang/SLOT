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


@allure.feature('Bet')
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

        if rebatePackage == rebatePackages[2] or rebatePackage == rebatePackages[3]:
            status_code, response = bet(rebatePackage=rebatePackage, token=get_token['token'])

            assert response['status'] == 400
            assert response['error'] == 'Bad Request'
            assert response['message'] == 'Argument error-> argument name: rebate, message: invalid rebate'
            assert response['errCode'] == 400
            assert response['code'] == 'param.txns[].rebate.invalid'
            assert response['values'] == []

        elif rebatePackage in rebatePackages[4:]:
            try:
                bet(rebatePackage=rebatePackage, token=get_token['token'])
            except ValueError as e:
                log(f'I need three errors: {e}')
                assert str(e) == 'Expecting value: line 1 column 1 (char 0)'
        else:
            status_code, response = bet(rebatePackage=rebatePackage, token=get_token['token'])

            assert status_code == 200
            assert len(response) == 1
            assert [len(str(i)) for i in response] == [16]


@allure.feature('Bet')
@allure.step('')
@pytest.mark.Bet
def test_bet_for_game_id(gameIds=('NYSSC3F', 'nyssc3f', '1'*20, '####', '我是中文', '', ' ', 'english')):

    for gameId in gameIds:
        if gameId != gameIds[0] and gameId != gameIds[1]:
            status_code, response = bet(gameId=gameId, token=get_token['token'])

            assert response['status'] == 400
            assert response['error'] == 'Bad Request'
            assert response['message'] == 'Argument error-> argument name: gameid, message: invalid gameid'
            assert response['errCode'] == 400
            assert response['code'] == 'param.gameid.invalid'
            assert response['values'] == []

        elif gameId == gameIds[1]:
            try:
                bet(gameId=gameId, token=get_token['token'])
            except Exception as e:

                assert str(e) == 'Expecting value: line 1 column 1 (char 0)'

        else:
            status_code, response = bet(gameId=gameId, token=get_token['token'])

            assert status_code == 200
            assert len(response) == 1
            assert [len(str(i)) for i in response] == [16]


@allure.feature('Bet')
@allure.step('')
@pytest.mark.skip('Lower priority')
# Not done yet
def test_bet_for_game_platform(platforms=('1'*20, 'Hi,im welly', '我是', '', ' ', '1'*21)):

    for platform in platforms:
        if platform != platforms[5]:
            status_code, response = bet(platform=platform, token=get_token['token'])

            assert status_code == 200
            assert len(response) == 1
            assert [len(str(i)) for i in response] == [16]

        else:
            try:
                bet(platform=platform, token=get_token['token'])
            except Exception as e:

                assert str(e) == 'Expecting value: line 1 column 1 (char 0)'


@allure.feature('Bet')
@allure.step('')
@pytest.mark.Bet
def test_bet_for_game_platType(playTypes=('SIMPLE', '1'*20, '####', '我是中文', '', ' ', 'english'),):

    for playType in playTypes:
        if playType != playTypes[0]:
            try:
                bet(playType=playType, token=get_token['token'])
            except Exception as e:

                assert str(e) == 'Expecting value: line 1 column 1 (char 0)'

        else:
            status_code, response = bet(playType=playType, token=get_token['token'])

            assert status_code == 200
            assert len(response) == 1
            assert [len(str(i)) for i in response] == [16]


@allure.feature('Bet')
@allure.step('')
@pytest.mark.Bet
def test_bet_for_game_betString(betStrings=('sum|small', '', '1'*20, '####', '我是中文', ' ', 'english')):

    for betString in betStrings:
        if betString != betStrings[0] and betString != betStrings[1]:
            status_code, response = bet(betString=betString, token=get_token['token'])

            assert status_code == 400
            assert response['status'] == 400
            assert response['error'] == 'Bad Request'
            assert response['message'] == 'Argument error-> argument name: txn, message: invalid'
            assert response['errCode'] == 400
            assert response['code'] == 'param.txn.invalid'
            assert response['values'] == []

        elif betString == betStrings[1]:
            status_code, response = bet(betString=betString, token=get_token['token'])

            assert status_code == 400
            assert response['status'] == 400
            assert response['error'] == 'Bad Request'
            assert response['message'] == 'Argument error-> argument name: betstring, message: invalid betstring' \
                                          f':  for game:NYSSC3F'
            assert response['errCode'] == 400
            assert response['code'] == 'param.txns[].betstring.invalid'
            assert response['values'] == []

        else:
            status_code, response = bet(betString=betString, token=get_token['token'])

            assert status_code == 200
            assert len(response) == 1
            assert [len(str(i)) for i in response] == [16]


@allure.feature('Bet')
@allure.step('')
@pytest.mark.skip('Lower priority')
def test_bet_for_game_comment(comments=('', '123', 'gnetl')):

    for comment in comments:
        bet(comment=comment, token=get_token['token'])


@allure.feature('Bet')
@allure.step('')
@pytest.mark.Bet
def test_bet_for_game_playId(playIdd=range(1, 50),
                             playIds=(17, '', '1'*20, '####', '我是中文', ' ', 'english')):

    for playId in playIds:

        if playId != playIds[0] and playId != playIds[1]:
            try:
                bet(playId=playId, token=get_token['token'])
            except ValueError as e:

                assert str(e) == 'Expecting value: line 1 column 1 (char 0)'

        elif playId == playIds[1]:

            status_code, response = bet(playId=playId, token=get_token['token'])

            assert status_code == 400
            assert response['status'] == 400
            assert response['error'] == 'Bad Request'
            assert response['message'] == 'Argument error-> argument name: playid,' \
                                          ' message: invalid playid: 0 for game:NYSSC3F'
            assert response['errCode'] == 400
            assert response['code'] == 'param.txns[].playid.invalid'
            assert response['values'] == []

        else:
            status_code, response = bet(playId=playId, token=get_token['token'])

            assert status_code == 200
            assert len(response) == 1
            assert [len(str(i)) for i in response] == [16]

    for playid in playIdd:

        if playid in range(18, 23):
            status_code, response = bet(playId=playid, token=get_token['token'])

            assert status_code == 400
            assert response['status'] == 400
            assert response['error'] == 'Bad Request'
            assert response['message'] == 'Argument error-> argument name: playid, ' \
                                          'message: playid not in playrate'
            assert response['errCode'] == 400
            assert response['code'] == 'param.txns[].playid.invalid'
            assert response['values'] == []

        elif playid != 17:
            status_code, response = bet(playId=playid, token=get_token['token'])

            assert status_code == 400
            assert response['status'] == 400
            assert response['error'] == 'Bad Request'
            assert response['message'] == 'Argument error-> argument name: playid,' \
                                          f' message: invalid playid: {playid} for game:NYSSC3F'
            assert response['errCode'] == 400
            assert response['code'] == 'param.txns[].playid.invalid'
            assert response['values'] == []

        else:
            pass


@allure.feature('Bet')
@allure.step('')
@pytest.mark.Bet
def test_bet_for_game_playRateId(playRateIds=range(16080, 16090),
                                 playRateIdd=('', '1'*20, '####', '我是中文', ' ', 'english'),
                                 rebatePackage=1980,
                                 stake=10,
                                 times=1,
                                 unit='DOLLAR'):

    for playRateId in playRateIds:
        if playRateId != playRateIds[0]:

            status_code, response = bet(playRateId=playRateId, token=get_token['token'])

            assert status_code == 400
            assert response['status'] == 400
            assert response['error'] == 'Bad Request'
            assert response['message'] == 'Argument error-> argument name: txn, ' \
                                          'message: invalid'
            assert response['errCode'] == 400
            assert response['code'] == 'param.txn.invalid'
            assert response['values'] == []

        else:
            status_code, response = bet(playRateId=playRateId, token=get_token['token'])

            assert status_code == 200
            assert len(response) == 1
            assert [len(str(i)) for i in response] == [16]

    for playrateid in playRateIdd:
        try:
            bet(playRateId=playrateid, token=get_token['token'])

        except ValueError as e:
            assert str(e) == 'Expecting value: line 1 column 1 (char 0)'


@allure.feature('Bet')
@allure.step('')
@pytest.mark.Bet
def test_bet_for_game_stake(stakes=('10', '', '1'*20, '####', '我是中文', ' ', 'english'),
                            times=1,
                            unit='DOLLAR'):

    for stake in stakes:
        log(stake)
        if stake == stakes[2]:

            status_code, response = bet(stake=stake, token=get_token['token'])

            assert status_code == 400
            assert response['status'] == 400
            assert response['error'] == 'Bad Request'
            assert response['message'] == 'Argument error-> argument name: risk, ' \
                                          'message: not pass risk validation'
            assert response['errCode'] == 400
            assert response['code'] == 'risk.exceed.by.player.total.stake'
            assert response['values'] == [50000]

        elif stake != stakes[0] and stake != stakes[2]:
            try:
                bet(stake=stake, token=get_token['token'])
            except ValueError as e:
                log(str(e))
                assert str(e) == 'Expecting value: line 1 column 1 (char 0)'

        else:
            status_code, response = bet(stake=stake, token=get_token['token'])

            assert status_code == 200
            assert len(response) == 1
            assert [len(str(i)) for i in response] == [16]






