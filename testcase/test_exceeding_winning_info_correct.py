from . import allure
from . import Base
from . import cms
from . import log
from . import pytest
from . import sle
from . import time
from .bet_base import bet
from .bet_base import now_month
from .bet_base import now_day
from .bet_base import wait_for_bet_and_return_previous_or_current


@allure.feature("Scenario for check overwin's info correct or not")
@allure.step('')
def test_over_win_prize(username=('overwin01', 'overwin04', 'overwin03', 'yahoo'),
                        gameId='TXFFC',
                        playType='SIMPLE',
                        betString='sum,big',
                        betString2='sum,small',
                        playRateId=18449,
                        prizeLimit=500,
                        stake=500,
                        playId=17,
                        rebatePackage=1980,
                        cancel_win_prize_types='CANCEL_WIN_PRIZE',
                        win_prize_type='WIN_PRIZE',
                        over_win_prize_type='OVER_WIN_PRIZE',
                        draw_null_types='REVOKED_NULL_RESULT'):
    start, end = Base().start_and_end_time(now_month, now_day, now_month, now_day)

    token, switch_button = continue_or_switch_user(username, start, end, types=None)

    cms.win_prize_limit(gameId=gameId,
                        playType=playType,
                        prizeLimit=prizeLimit, )

    current_bet = wait_for_bet_and_return_previous_or_current(gameId, sleep_time=6)
    for i in range(2):
        bet(gameId=gameId,
            betString=betString,
            playId=playId,
            playRateId=playRateId,
            rebatePackage=rebatePackage,
            stake=stake,
            token=token)
        betString = betString2
        playRateId += 1
        time.sleep(1)

    time.sleep(30)  # 太接近預設的開獎會失敗, so 睡30秒

    draw_lottery(gameId=gameId,
                 start=start,
                 drawIdString=current_bet['current']['drawIdString'],
                 action='MANUAL_GIVING_RESULTS',
                 result='1,2,3,4,5',
                 method=1)

    sle_cancel_win_prize_equal_zero(token, start, end, types=cancel_win_prize_types)
    sle_win_prize_search_and_display_500(token, start, end, types=win_prize_type, amount=prizeLimit)

    cms_over_win_prize_minus(start, end, userId=None, types=over_win_prize_type)
    cms_win_prize_search_and_display_500(start, end,
                                         userId=f'SL3{username[switch_button]}',
                                         types=win_prize_type,
                                         amount=prizeLimit)

    draw_lottery(gameId=gameId,
                 start=start,
                 drawIdString=current_bet['current']['drawIdString'],
                 action='OPEN_NULL',
                 result='1,2,3,4,5',
                 method='null')

    time.sleep(3)

    cms_over_win_prize_minus(start, end, userId=None, types=over_win_prize_type)

    cms_cancel_win_prize_search_equal_500(start,
                                          end,
                                          userId=f'SL3{username[switch_button]}',
                                          types=cancel_win_prize_types,
                                          amount=prizeLimit)

    cms_draw_null_search_two_equal_500(start,
                                       end,
                                       userId=f'SL3{username[switch_button]}',
                                       types=draw_null_types,
                                       amount=prizeLimit)

    sle_cancel_win_prize_equal_500(token, start, end, types=cancel_win_prize_types, amount=prizeLimit)
    sle_draw_null_search_two_bet_equal_500(token, start, end, types=draw_null_types, amount=prizeLimit)


def continue_or_switch_user(username, start, end, types):
    switch_button = 0
    record = cms.transaction_record(userId=f"SL3{username[switch_button]}", start=start, end=end, types=types)

    while record['total'] != 0:
        switch_button += 1
        record = cms.transaction_record(userId=f"SL3{username[switch_button]}", start=start, end=end, types=types)

    log(f"Use user: {username[switch_button]}")
    _, token = sle.get_launch_token(username[switch_button])

    return token['token'], switch_button


def draw_lottery(gameId, start, drawIdString, action, result, method):
    draw_record = cms.draw_management(gameId=gameId,
                                      startBefore=start,
                                      drawIdString=drawIdString)
    cms.draw_null(period=draw_record['data'][0]['id'], action=action, result=result, method=method)


def sle_cancel_win_prize_equal_zero(token, start, end, types):
    cancel_win_prize_record = sle.transaction_record(token=token,
                                                     start=start,
                                                     end=end,
                                                     types=types)
    pytest.assume(cancel_win_prize_record['total'] == 0)


def sle_win_prize_search_and_display_500(token, start, end, types, amount):
    win_prize_record = sle.transaction_record(token, start, end, types)
    data = win_prize_record['data'][0]

    pytest.assume(data['txnType'] == types)
    pytest.assume(data['in'] == True)
    pytest.assume(data['txnAmt'] == amount)
    pytest.assume(data['afterBalance'] == data['beforeBalance'] + amount)


def cms_over_win_prize_minus(start, end, userId, types):
    record = cms.transaction_record(userId=userId, start=start, end=end, types=types)

    pytest.assume(record['total'] == 0)


def cms_win_prize_search_and_display_500(start, end, userId, types, amount):
    record = cms.transaction_record(userId=userId, start=start, end=end, types=types)
    data = record['data'][0]

    pytest.assume(data['txnType'] == types)
    pytest.assume(data['in'] == True)
    pytest.assume(data['userId'] == userId)
    pytest.assume(data['txnAmt'] == amount)
    pytest.assume(data['afterBalance'] == data['beforeBalance'] + amount)
    pytest.assume(data['detailType'] == 'LOTTERY')


def cms_cancel_win_prize_search_equal_500(start, end, userId, types, amount):
    record = cms.transaction_record(userId=userId, start=start, end=end, types=types)
    data = record['data'][0]

    pytest.assume(data['txnType'] == types)
    pytest.assume(data['in'] == False)
    pytest.assume(data['userId'] == userId)
    pytest.assume(data['txnAmt'] == amount)
    pytest.assume(data['afterBalance'] == data['beforeBalance'] - 500)


def cms_draw_null_search_two_equal_500(start, end, userId, types, amount):
    record = cms.transaction_record(userId=userId, start=start, end=end, types=types)
    times = 0
    sleep_second = 5
    while len(record['data']) == 0:
        times += 1
        time.sleep(sleep_second)
        record = cms.transaction_record(userId=userId, start=start, end=end, types=types)
        if times > 8:
            raise ValueError(f"CMS's transaction record not found, spend time: {times} times * {sleep_second} second")

    data1 = record['data'][0]
    data2 = record['data'][1]

    pytest.assume(data1['txnType'] == types)
    pytest.assume(data1['in'] == True)
    pytest.assume(data1['userId'] == userId)
    pytest.assume(data1['txnAmt'] == amount)
    pytest.assume(data1['afterBalance'] == data1['beforeBalance'] + 500)

    pytest.assume(data2['txnType'] == types)
    pytest.assume(data2['in'] == True)
    pytest.assume(data2['userId'] == userId)
    pytest.assume(data2['txnAmt'] == amount)
    pytest.assume(data2['afterBalance'] == data2['beforeBalance'] + 500)


def sle_cancel_win_prize_equal_500(token, start, end, types, amount):
    record = sle.transaction_record(token=token,
                                    start=start,
                                    end=end,
                                    types=types)
    data = record['data'][0]
    pytest.assume(data['in'] == False)
    pytest.assume(data['txnType'] == types)
    pytest.assume(data['txnAmt'] == amount)
    pytest.assume(data['afterBalance'] == data['beforeBalance'] - amount)


def sle_draw_null_search_two_bet_equal_500(token, start, end, types, amount):
    record = sle.transaction_record(token=token,
                                    start=start,
                                    end=end,
                                    types=types)
    data1 = record['data'][0]
    data2 = record['data'][1]

    pytest.assume(data1['txnType'] == types)
    pytest.assume(data1['in'] == True)
    pytest.assume(data1['txnAmt'] == amount)
    pytest.assume(data1['afterBalance'] == data1['beforeBalance'] + 500)

    pytest.assume(data2['txnType'] == types)
    pytest.assume(data2['in'] == True)
    pytest.assume(data2['txnAmt'] == amount)
    pytest.assume(data2['afterBalance'] == data2['beforeBalance'] + 500)
