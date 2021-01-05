from . import allure
from . import Base
from . import cms
from . import log
from . import pytest
from . import sle
from . import time
from .bet_base import now_month
from .bet_base import now_day


@allure.feature(f"Scenario for bet chase number and verify basic chase report")
@allure.step('')
def test_bet_chase_number(gameId='NYK31F',
                          gameName='极速骰宝(官)',
                          playType='STANDALONE',
                          betString='s3sum|3',
                          playId='30001',
                          playRateId='14876',
                          rebatePackage=1980,
                          stake=1,
                          username='welly1',
                          drawCount=10,
                          betCategory='一般',
                          state='CREATED',
                          vendorId='MX2'
                          ):
    start, end = Base().start_and_end_time(now_month, now_day, now_month, now_day,)

    response = sle.active_and_previous_period(gameId)
    time.sleep(3) if response['current']['countdown'] <= 1000 else ''

    _, token = sle.get_launch_token(username)
    retrieved_draw = sle.retrieved_draw(gameId, token=token['token'], drawCount=drawCount)

    draw_list = []
    for draw in retrieved_draw:
        draw_list.append({'drawId': draw['drawId'], 'times': 1})
    sle.chase_bet(gameId=gameId,
                  playType=playType,
                  betString=betString,
                  playId=playId,
                  playRateId=playRateId,
                  rebatePackage=rebatePackage,
                  stake=stake,
                  drawId=draw_list,
                  token=token['token'])

    report = cms.chase_report(start=start, end=end)
    verify_chase_report(report,
                        betCategory,
                        betName=betString[-1],
                        betString=betString[-1],
                        firstDrawId=draw_list[0]['drawId'],
                        firstDrawIdString=str(retrieved_draw[0]['drawIdString']),
                        gameId=gameId,
                        gameName=gameName,
                        playType=playType,
                        state=state,
                        totalDrawCount=drawCount,
                        totalStake=stake * drawCount,
                        userId=f'SL3{username}',
                        vendorId=vendorId)


def verify_chase_report(report,
                        betCategory,
                        betName,
                        betString,
                        firstDrawId,
                        firstDrawIdString,
                        gameId,
                        gameName,
                        playType,
                        state,
                        totalDrawCount,
                        totalStake,
                        userId,
                        vendorId):
    report = report['data'][0]

    pytest.assume(report['betCategory'] == betCategory)
    pytest.assume(report['betName'] == betName)
    pytest.assume(report['betString'] == betString)
    pytest.assume(report['firstDrawId'] == firstDrawId)
    pytest.assume(report['firstDrawIdString'] == firstDrawIdString)
    pytest.assume(report['gameId'] == gameId)
    pytest.assume(report['gameName'] == gameName)
    pytest.assume(report['playType'] == playType)
    pytest.assume(report['state'] == state)
    pytest.assume(report['totalCanceledCount'] == 0)
    pytest.assume(report['totalCanceledStake'] == 0)
    pytest.assume(report['totalClearedCount'] == 0)
    pytest.assume(report['totalClearedStake'] == 0)
    pytest.assume(report['totalDrawCount'] == totalDrawCount)
    pytest.assume(report['totalStake'] == totalStake)
    pytest.assume(report['unit'] == 'DOLLAR')
    pytest.assume(report['userId'] == userId)
    assert report['vendorId'] == vendorId

