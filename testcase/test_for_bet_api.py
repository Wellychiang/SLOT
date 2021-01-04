from . import allure
from . import cms
from . import log
from . import pytest
from . import sle
from . import time
from . import ROOT_ACCOUNT
from .bet_base import bet

bet_feature = 'Bet'


@allure.feature('Cms')
@pytest.mark.skip()
def test_cms():
    strftimes = (time.strftime('%Y-%m-%d') + ' 00:00:00', time.strftime('%Y-%m-%d') + ' 23:59:59')

    for strftime in strftimes:
        strptime = time.strptime(strftime, '%Y-%m-%d %H:%M:%S')
        if strftime == strftimes[0]:
            todays_start = time.mktime(strptime)
        else:
            todays_end = time.mktime(strptime)

    # print(int(todays_start*1000), int((todays_end+0.999)*1000))
    status_code, response = cms.bet_details(tm_start=int(todays_start * 1000), tm_end=int((todays_end + 0.999) * 1000))

    """Not done"""
    print(f'response: {len(response["data"])}')


@allure.feature(bet_feature)
@allure.step('')
@pytest.mark.Bet
def test_bet_for_rebate_packages(token, rebatePackages=(1980,
                                                        1979,
                                                        1981,
                                                        1769,
                                                        '1' * 20,
                                                        '####',
                                                        '我是中文',
                                                        '',
                                                        ' ',
                                                        'english'), ):
    for rebatePackage in rebatePackages:

        if rebatePackage in rebatePackages[1:4]:
            status_code, response = bet(rebatePackage=rebatePackage, token=token)

            pytest.assume(response['status'] == 400)
            pytest.assume(response['error'] == 'Bad Request')
            pytest.assume(response['message'] == 'Argument error-> argument name: rebate, message: invalid rebate')
            pytest.assume(response['errCode'] == 400)
            pytest.assume(response['code'] == 'param.txns[].rebate.invalid')
            pytest.assume(response['values'] == [])

        elif rebatePackage in rebatePackages[4:]:
            try:
                bet(rebatePackage=rebatePackage, token=token)
            except ValueError as e:
                log(f'I need three errors: {e}')
                pytest.assume(str(e) == 'Expecting value: line 1 column 1 (char 0)')
        else:
            status_code, response = bet(rebatePackage=rebatePackage, token=token)

            pytest.assume(status_code == 200)
            pytest.assume(len(response) == 1)
            pytest.assume([len(str(i)) for i in response] == [16])


@allure.feature(bet_feature)
@allure.step('')
@pytest.mark.Bet
def test_bet_for_game_id(token, gameIds=('NYSSC3F', 'nyssc3f', '####', '', '1' * 20, '我是中文', ' ', 'english')):
    for gameId in gameIds:
        if gameId not in gameIds[:4]:
            status_code, response = bet(gameId=gameId, token=token)

            pytest.assume(response['status'] == 400)
            pytest.assume(response['error'] == 'Bad Request')
            pytest.assume(response['message'] == 'Argument error-> argument name: gameid, message: invalid gameid')
            pytest.assume(response['errCode'] == 400)
            pytest.assume(response['code'] == 'param.gameid.invalid')
            pytest.assume(response['values'] == [])

        elif gameId in gameIds[1:4]:
            try:
                bet(gameId=gameId, token=token)
            except Exception as e:
                pytest.assume(str(e) == 'Expecting value: line 1 column 1 (char 0)')

        else:
            status_code, response = bet(gameId=gameId, token=token)

            pytest.assume(status_code == 200)
            pytest.assume(len(response) == 1)
            pytest.assume([len(str(i)) for i in response] == [16])


@allure.feature(bet_feature)
@allure.step('')
@pytest.mark.skip('Lower priority')
# Not done yet
def test_bet_for_game_platform(token, platforms=('1' * 20, 'Hi,im welly', '我是', '', ' ', '1' * 21)):
    for platform in platforms:
        if platform != platforms[5]:
            status_code, response = bet(platform=platform, token=token)

            pytest.assume(status_code == 200)
            pytest.assume(len(response) == 1)
            pytest.assume([len(str(i)) for i in response] == [16])

        else:
            try:
                bet(platform=platform, token=token)
            except Exception as e:

                pytest.assume(str(e) == 'Expecting value: line 1 column 1 (char 0)')


@allure.feature(bet_feature)
@allure.step('')
@pytest.mark.Bet
def test_bet_for_game_platType(token, playTypes=('SIMPLE', '1' * 20, '####', '我是中文', '', ' ', 'english'), ):
    for playType in playTypes:
        if playType != playTypes[0]:
            try:
                bet(playType=playType, token=token)
            except Exception as e:

                pytest.assume(str(e) == 'Expecting value: line 1 column 1 (char 0)')

        else:
            status_code, response = bet(playType=playType, token=token)

            pytest.assume(status_code == 200)
            pytest.assume(len(response) == 1)
            pytest.assume([len(str(i)) for i in response] == [16])


@allure.feature(bet_feature)
@allure.step('')
@pytest.mark.Bet
# sum|small = 16080, sum|big = 16790, sum|odd = 16792, sum|even = 16793
def test_bet_for_game_betString(token, betStrings=('sum,small', '', '1' * 20, '####', '我是中文', ' ', 'english')):
    for betString in betStrings:
        if betString not in betStrings[:2]:
            status_code, response = bet(betString=betString, token=token)

            pytest.assume(status_code == 400)
            pytest.assume(response['status'] == 400)
            pytest.assume(response['error'] == 'Bad Request')
            pytest.assume(response['message'] == 'Argument error-> argument name: txn, message: invalid')
            pytest.assume(response['errCode'] == 400)
            pytest.assume(response['code'] == 'param.txn.invalid')
            pytest.assume(response['values'] == [])

        elif betString == betStrings[1]:
            status_code, response = bet(betString=betString, token=token)

            pytest.assume(status_code == 400)
            pytest.assume(response['status'] == 400)
            pytest.assume(response['error'] == 'Bad Request')
            pytest.assume(response['message'] == 'Argument error-> argument name: betstring, message: invalid betstring' \
                                                 ':  for game:NYSSC3F')
            pytest.assume(response['errCode'] == 400)
            pytest.assume(response['code'] == 'param.txns[].betstring.invalid')
            pytest.assume(response['values'] == [])

        else:
            status_code, response = bet(betString=betString, token=token)

            pytest.assume(status_code == 200)
            pytest.assume(len(response) == 1)
            pytest.assume([len(str(i)) for i in response] == [16])


@allure.feature(bet_feature)
@allure.step('')
@pytest.mark.skip('Lower priority, comments can not see the different and even invalid input can input')
def test_bet_for_game_comment(token, comments=('1' * 99, '123', '#@$$%')):
    for comment in comments:
        bet(comment=comment, token=token)


@allure.feature(bet_feature)
@allure.step('')
@pytest.mark.Bet
def test_bet_for_game_playId(token,
                             playIdd=range(1, 50),
                             playIds=(17, '', '1' * 20, '####', '我是中文', ' ', 'english')):
    response = sle.active_and_previous_period('NYSSC3F')
    if response['current']['countdown'] <= 16000:
        wait_time = ((response['current']['countdown'] / 1000) + 5)

        log(f'\nCount down time is too short to verify, wait for the next lottery draw.\nCount down: {wait_time}')
        time.sleep(wait_time)

    for playId in playIds:

        if playId not in playIds[:2]:
            try:
                bet(playId=playId, token=token)
            except ValueError as e:

                pytest.assume(str(e) == 'Expecting value: line 1 column 1 (char 0)')

        elif playId == playIds[1]:

            status_code, response = bet(playId=playId, token=token)

            pytest.assume(status_code == 400)
            pytest.assume(response['status'] == 400)
            pytest.assume(response['error'] == 'Bad Request')
            pytest.assume(response['message'] == 'Argument error-> argument name: playid,' \
                                                 ' message: invalid playid: 0 for game:NYSSC3F')
            pytest.assume(response['errCode'] == 400)
            pytest.assume(response['code'] == 'param.txns[].playid.invalid')
            pytest.assume(response['values'] == [])

        else:
            status_code, response = bet(playId=playId, token=token)

            pytest.assume(status_code == 200)
            pytest.assume(len(response) == 1)
            pytest.assume([len(str(i)) for i in response] == [16])

    for playid in playIdd:

        if playid in range(18, 28):
            log(f'Play id in 18 ~ 27: {playid}')
            status_code, response = bet(playId=playid, token=token)

            pytest.assume(status_code == 400)
            pytest.assume(response['status'] == 400)
            pytest.assume(response['error'] == 'Bad Request')
            pytest.assume(response['message'] == 'Argument error-> argument name: playid, '
                                                 'message: playid not in playrate')
            pytest.assume(response['errCode'] == 400)
            pytest.assume(response['code'] == 'param.txns[].playid.invalid')
            pytest.assume(response['values'] == [])

        elif playid != 17:
            log(f'Play id: {playid}')
            status_code, response = bet(playId=playid, token=token)

            pytest.assume(status_code == 400)
            pytest.assume(response['status'] == 400)
            pytest.assume(response['error'] == 'Bad Request')
            pytest.assume(response['message'] == 'Argument error-> argument name: playid,'
                                                 f' message: invalid playid: {playid} for game:NYSSC3F')
            pytest.assume(response['errCode'] == 400)
            pytest.assume(response['code'] == 'param.txns[].playid.invalid')
            pytest.assume(response['values'] == [])

        else:
            log('Im play id 17, I should be success')
            status_code, response = bet(playId=playid, token=token)

            pytest.assume(status_code == 200)
            pytest.assume(len(response) == 1)
            pytest.assume([len(str(i)) for i in response] == [16])


@allure.feature(bet_feature)
@allure.step('')
@pytest.mark.Bet
def test_bet_for_game_playRateId(token,
                                 playRateIds=range(16080, 16090),
                                 playRateIdd=('', '1' * 20, '####', '我是中文', ' ', 'english')):
    for playRateId in playRateIds:
        if playRateId != playRateIds[0]:

            status_code, response = bet(playRateId=playRateId, token=token)

            pytest.assume(status_code == 400)
            pytest.assume(response['status'] == 400)
            pytest.assume(response['error'] == 'Bad Request')
            pytest.assume(response['message'] == 'Argument error-> argument name: txn, '
                                                 'message: invalid')
            pytest.assume(response['errCode'] == 400)
            pytest.assume(response['code'] == 'param.txn.invalid')
            pytest.assume(response['values'] == [])

        else:
            status_code, response = bet(playRateId=playRateId, token=token)

            pytest.assume(status_code == 200)
            pytest.assume(len(response) == 1)
            pytest.assume([len(str(i)) for i in response] == [16])

    for playrateid in playRateIdd:
        try:
            bet(playRateId=playrateid, token=token)

        except ValueError as e:
            pytest.assume(str(e) == 'Expecting value: line 1 column 1 (char 0)')


@allure.feature(bet_feature)
@allure.step('')
@pytest.mark.skip('Wait for the new module done')
def test_bet_for_game_stake(token,
                            stakes=('10', '1' * 20, '0.2999', '', '####', '我是中文', ' ', 'english')):
    """
    CMS 彩票設置 > 封鎖限額限制(新增玩家單注最低), 影響到了這 function, 會導致可以輸入0.2這樣的數字
    """
    for stake in stakes:
        if stake == stakes[1] or stake == stakes[2]:

            status_code, response = bet(stake=stake, token=token)

            log(f'Stake: {stake}')
            pytest.assume(status_code == 400)
            pytest.assume(response['status'] == 400)
            pytest.assume(response['error'] == 'Bad Request')
            pytest.assume(response['message'] == 'Argument error-> argument name: risk, '
                                                 'message: not pass risk validation')
            pytest.assume(response['errCode'] == 400)
            pytest.assume(response['code'] == 'risk.exceed.by.player.single.stake')
            pytest.assume(50000 in response['values'])

        elif stake not in stakes[:3]:

            log(f'Stake: {stake}')
            try:
                bet(stake=stake, token=token)
            except ValueError as e:
                pytest.assume(str(e) == 'Expecting value: line 1 column 1 (char 0)')

        else:
            log(f'Stake: {stake}')
            status_code, response = bet(stake=stake, token=token)

            pytest.assume(status_code == 200)
            pytest.assume(len(response) == 1)
            pytest.assume([len(str(i)) for i in response] == [16])


@allure.feature(bet_feature)
@allure.step('')
@pytest.mark.Bet
def test_bet_for_game_times(token,
                            timeses=(3, '', ' ', '1' * 20, '####', '我是中文', 'english')):
    """if bet slip amount = 10, times = 3,  it will be 30 at last(10*3)"""
    for times in timeses:
        if times in timeses[3:]:
            try:
                bet(times=times, token=token)

            except ValueError as e:

                pytest.assume(str(e) == 'Expecting value: line 1 column 1 (char 0)')

        elif times in timeses[1:3]:
            status_code, response = bet(times=times, token=token)

            pytest.assume(status_code == 400)
            pytest.assume(response['status'] == 400)
            pytest.assume(response['error'] == 'Bad Request')
            pytest.assume(response['message'] == 'Argument error-> argument name: times, message: invalid times')
            pytest.assume(response['errCode'] == 400)
            pytest.assume(response['code'] == 'param.txns[].times.invalid')
            pytest.assume(response['values'] == [])

        else:
            status_code, response = bet(times=times, token=token)

            pytest.assume(status_code == 200)
            pytest.assume(len(response) == 1)
            pytest.assume([len(str(i)) for i in response] == [16])


@allure.feature(bet_feature)
@allure.step('')
@pytest.mark.Bet
def test_bet_for_game_unit(token, units=('DOLLAR', '', ' ', '1' * 20, '####', '刀惹', 'english'.upper())):
    for unit in units:
        if unit != units[0]:
            try:
                bet(unit=unit, token=token)

            except ValueError as e:
                print(str(e))

                pytest.assume(str(e) == 'Expecting value: line 1 column 1 (char 0)')
        else:
            status_code, response = bet(unit=unit, token=token)

            pytest.assume(status_code == 200)
            pytest.assume(len(response) == 1)
            pytest.assume([len(str(i)) for i in response] == [16])


@allure.feature(bet_feature)
@allure.step('')
@pytest.mark.Bet
def bet_for_two_bet_slit(token,
                         gameId='NYSSC3F',
                         playType='SIMPLE',
                         betString='sum,small',
                         playId=17,
                         playRateId=16791,
                         rebatePackage=1900,
                         stake=10,
                         times=1):
    """
    Use two txn arguments in request body to post in one interface, and get two bet slip.
    """
    more_data = {
        'betString': 'sum,big',
        'gameId': gameId,
        'playType': playType,
        'playId': playId,
        'playRateId': '16790',
        'rebatePackage': rebatePackage,
        'stake': stake,
        'times': times,
        'unit': 'DOLLAR'
    }

    # for betString in betStrings:
    bet(betString=betString,
        gameId=gameId,
        playType=playType,
        playId=playId,
        playRateId=playRateId,
        rebatePackage=rebatePackage,
        stake=stake,
        times=times,
        token=token,
        more_data=more_data)



@allure.feature(f"Scenario for betString's multi content")
@allure.step
@pytest.mark.Bet
def test_betString_multi_content(token,
                                 gameId=('NYK31F', 'NYSSC15F', 'HKHSIL', 'SUPERYK'),
                                 playType='STANDALONE',
                                 betString=('s3redblack|1,2:3|1,2:3|1,2:3', 'dt2vs5|draw|draw|draw', '1dtop|0|2|4|0',
                                            '3dtop|090|121|332|090'),
                                 playId=(30101, 10907, 100003, 80001),
                                 playRateId=(14903, 78737, 101867, 102616),
                                 rebatePackage=1980,
                                 stake=1,
                                 vendor='MX2'):
    for i in range(4):
        setting_status = cms.games_close_or_open(username=ROOT_ACCOUNT,
                                                 gameId=gameId[i],
                                                 gameStatus='ACTIVE',
                                                 playType=playType,
                                                 vendorId=vendor)
        if setting_status != 204:
            raise ValueError('Init game failed')
        status_code, response = bet(gameId=gameId[i],
                                    playType=playType,
                                    betString=betString[i],
                                    playId=playId[i],
                                    playRateId=playRateId[i],
                                    rebatePackage=rebatePackage,
                                    stake=stake,
                                    token=token,
                                    vendor=vendor)

        pytest.assume(status_code == 400)
        pytest.assume(response['message'] == 'Argument error-> argument name: betstring, message: invalid betstring:'
                                             f' multi content for game:{gameId[i]}')


if __name__ == '__main__':
    pass
