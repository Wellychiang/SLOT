from base.base import log, Base
from base.base_cms import Cms
from base.base_sle import Sle
import pytest
import time
import re

cms = Cms()
sle = Sle()


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

    print(f'response: {len(response["data"])}')


def test_bet_for_rebate_packages(username='welly1',
                                 drawId=int(time.strftime('%Y%m%d')+'00429'),
                                 gameId='NYSSC3F',  # NYSSC3F, NYSSC15F
                                 platform='Desktop',
                                 playType='SIMPLE',
                                 betString='sum|small',
                                 comment='',
                                 playId=17,
                                 playRateId=16080,
                                 rebatePackages=(1980, 1800, 1981, 1799, '1'*20, '####', '我是中文'),
                                 stake=10,
                                 times=1,
                                 unit='DOLLAR'):
    invalid_rebate = 0
    wrong_message = 0
    for rebatePackage in rebatePackages:
        try:
            status_code, response = sle.bet(username,
                                            drawId,
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
                                            unit)
            # 先打一次錯誤的drawid, response會丟給我正確的, 之後再打
            drawid = re.findall('id (.*) !', response['message'])
            draw = drawid[0]

            print(f'drawId: {drawId}')
            status_code, response = sle.bet(username,
                                            draw,
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
                                            unit)
            if 'message' in response:
                if 'invalid rebate' in response['message']:
                    invalid_rebate += 1
            else:
                pass

        except ValueError as e:
            wrong_message += 1
            log(f'Im a error: {e}')
            assert str(e) == 'Expecting value: line 1 column 1 (char 0)'

    log(f'Invalid rebate: {invalid_rebate}\n '
        f'wrong message with json: {wrong_message}')
    assert invalid_rebate == 2
    assert wrong_message == 3


def test_bet_for_game_id(username='welly1',
                         drawId=int(time.strftime('%Y%m%d')+'00429'),
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
                         unit='DOLLAR'):

        status_code, response = sle.bet(username,
                                        drawId,
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
                                        unit)
        # 先打一次錯誤的drawid, response會丟給我正確的, 之後再打
        drawid = re.findall('id (.*) !', response['message'])
        draw = drawid[0]

        print(f'drawId: {drawId}')
        status_code, response = sle.bet(username,
                                        draw,
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
                                        unit)