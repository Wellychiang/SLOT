from testcase import cms, sle, time, log, Base, pytest, allure
from testcase.bet_base import bet, wait_and_lottery_draw, for_loop_bet_and_verify, now_month, now_day
from testcase.bet_base import wait_for_bet_and_return_previous_or_current


@allure.feature("Scenario for check overwin's info correct or not")
def test_over_win_prize(username=('overwin01', 'overwin04', 'overwin03', 'yahoo'),
                        gameId='TXFFC',
                        playType='SIMPLE',
                        betString='sum,big',
                        betString2='sum,small',
                        playRateId=18449,
                        prizeLimit=500,
                        cancel_win_prize_types='CANCEL_WIN_PRIZE',
                        win_prize_type='WIN_PRIZE',
                        over_win_prize_type='OVER_WIN_PRIZE',
                        draw_null_types='REVOKED_NULL_RESULT'):
    start, end = Base().start_and_end_time(now_month, now_day, now_month, now_day)

    levelup_button = 0
    record = cms.transaction_record(userId=f"SL3{username[levelup_button]}", start=start, end=end, types=None)

    while record['total'] != 0:
        levelup_button += 1
        record = cms.transaction_record(userId=f"SL3{username[levelup_button]}", start=start, end=end, types=None)

    log(f"Use user: {username[levelup_button]}")
    _, token = sle.get_launch_token(username[levelup_button])

    cms.win_prize_limit(gameId=gameId,
                        playType=playType,
                        prizeLimit=prizeLimit, )

    # TODO: 下注藤信紛紛採 大, 小, 各500, 然後等到開獎
    current_bet = wait_for_bet_and_return_previous_or_current('TXFFC', 6)
    for i in range(2):
        bet(gameId='TXFFC',
            betString=betString,
            playId=17,
            playRateId=playRateId,
            rebatePackage=1980,
            stake=500,
            token=token['token'])
        betString = betString2
        playRateId += 1
        time.sleep(1)

    time.sleep(30)  # 太接近預設的開獎會失敗, so 睡30秒

    draw_record = cms.draw_management(gameId='TXFFC',
                                      startBefore=start,
                                      drawIdString=current_bet['current']['drawIdString'])
    cms.draw_null(period=draw_record['data'][0]['id'], action='MANUAL_GIVING_RESULTS', method=1)

    # TODO: Search EC斷言撤銷派彩, 中獎(Done)
    sle_cancel_win_prize_equal_zero(token, start, end, types=cancel_win_prize_types)
    sle_win_prize_search_and_display_500(token, start, end, types=win_prize_type, amount=prizeLimit)

    # TODO: cms勾選超額中獎扣除並提交, 和勾選彩票派獎並提交
    cms_over_win_minus(start, end, userId=None, types=over_win_prize_type)
    cms_win_prize_search_and_display_500(start, end, userId=f'SL3{username[levelup_button]}', types=win_prize_type,
                                         amount=prizeLimit)

    # TODO: cms 騰訊紛紛採 空開
    draw_record = cms.draw_management(gameId='TXFFC',
                                      startBefore=start,
                                      drawIdString=current_bet['current']['drawIdString'])
    cms.draw_null(period=draw_record['data'][0]['id'])

    time.sleep(3)
    # TODO: cms 勾選中獎返還並提交 (暫無資料)
    cms_over_win_minus(start, end, userId=None, types=over_win_prize_type)

    # TODO: cms 勾選撤銷派彩並提交(顯示500)
    cms_cancel_win_prize_search_equal_500(start, end, userId=f'SL3{username[levelup_button]}',
                                          types=cancel_win_prize_types, amount=prizeLimit)

    # TODO: cms 勾選空開撤單並提交(有兩筆, 顯示空開且500)
    cms_draw_null_search_two_equal_500(start, end, userId=f'SL3{username[levelup_button]}', types=draw_null_types,
                                       amount=prizeLimit)

    # TODO: ec 遊戲大廳 > 錢包紀錄, 撤銷派彩 -500, 兩筆空開掣單500
    sle_cancel_win_prize_equal_500(token, start, end, types=cancel_win_prize_types, amount=prizeLimit)
    sle_draw_null_search_two_bet_equal_500(token, start, end, types=draw_null_types, amount=prizeLimit)


def sle_cancel_win_prize_equal_zero(token, start, end, types):
    cancel_win_prize_record = sle.transaction_record(token=token['token'],
                                                     start=start,
                                                     end=end,
                                                     types=types)
    pytest.assume(cancel_win_prize_record['total'] == 0)


def sle_win_prize_search_and_display_500(token, start, end, types, amount):
    win_prize_record = sle.transaction_record(token['token'], start, end, types)
    data = win_prize_record['data'][0]

    pytest.assume(data['txnType'] == types)
    pytest.assume(data['in'] == True)
    pytest.assume(data['txnAmt'] == amount)
    pytest.assume(data['afterBalance'] == data['beforeBalance'] + amount)


def cms_over_win_minus(start, end, userId, types):
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
    record = sle.transaction_record(token=token['token'],
                                    start=start,
                                    end=end,
                                    types=types)
    data = record['data'][0]
    pytest.assume(data['in'] == False)
    pytest.assume(data['txnType'] == types)
    pytest.assume(data['txnAmt'] == amount)
    pytest.assume(data['afterBalance'] == data['beforeBalance'] - amount)


def sle_draw_null_search_two_bet_equal_500(token, start, end, types, amount):
    record = sle.transaction_record(token=token['token'],
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
