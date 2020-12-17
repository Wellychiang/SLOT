from testcase import allure
from testcase import Base
from testcase import cms
from testcase import pytest
from testcase import sle
from testcase import time
from testcase.bet_base import bet
from testcase.bet_base import now_month
from testcase.bet_base import now_day
from testcase.bet_base import wait_for_bet_and_return_previous_or_current


@allure.feature("Scenario for bet and check relative account changes info")
def test_for_bet_relative_info(username='welly1',
                               gameId='NYSSC1F',
                               betString='s5vary1,1',
                               result='1,0,9,2,3',
                               playType='STANDALONE',
                               count_down_second=15,
                               playId=10009,
                               playRateId=16476,
                               rebatePackage=1940,
                               rebate_amount=2,
                               win_prize=236.86,
                               stakes=(1, 100),
                               create_txn_types='CREATE_TXN',
                               cancel_txn_types='CANCEL_TXN',
                               self_rebate_types='SELF_REBATE',
                               win_prize_types='WIN_PRIZE'):
    start, end = Base().start_and_end_time(now_month, now_day, now_month, now_day)

    bet_info = wait_for_bet_and_return_previous_or_current(gameId, count_down_second)
    status_code = cms.lottery_draw(drawId=bet_info['current']['drawId'],
                                   gameId=gameId,
                                   result=result)
    if status_code != 200:
        raise ValueError('Lottery draw failed')

    _, get_token = sle.get_launch_token(username)
    sle_init = sle_init_record(token=get_token['token'],
                               start=start,
                               end=end,
                               create_types=create_txn_types,
                               cancel_types=cancel_txn_types,
                               rebate_types=self_rebate_types,
                               win_prize_types=win_prize_types)

    cms_init = cms_init_record(userId=f'SL3{username}',
                               start=start,
                               end=end,
                               create_types=create_txn_types,
                               cancel_types=cancel_txn_types,
                               rebate_types=self_rebate_types,
                               win_prize_types=win_prize_types)

    bet_ids = []
    for stake in stakes:
        _, bet_i = bet(gameId=gameId,
                       playType=playType,
                       betString=betString,
                       playId=playId,
                       playRateId=playRateId,
                       rebatePackage=rebatePackage,
                       stake=stake,
                       token=get_token['token'], )
        time.sleep(1.5)
        bet_ids.append(bet_i)

    cancel_status_code, response = sle.cancel_bet(token=get_token['token'],
                                                  drawIdString=bet_info['current']['drawIdString'],
                                                  drawid=bet_info['current']['drawId'],
                                                  gameid=gameId,
                                                  txnid=bet_ids[0][0], )

    if cancel_status_code != 200 and response['total'] != 1:
        raise ValueError('Cancel bet failed')

    sle_search_for_bet_and_assert_100_10(token=get_token['token'],
                                         start=start,
                                         end=end,
                                         types=create_txn_types,
                                         amount=stakes[1],
                                         init_total_record=sle_init["create_record"]["total"])
    sle_search_for_revoke_bet_and_assert_amount_equal_1(token=get_token['token'],
                                                        start=start,
                                                        end=end,
                                                        types=cancel_txn_types,
                                                        amount=stakes[0],
                                                        init_total_record=sle_init["cancel_record"]["total"])
    sle_search_for_rebate_and_assert_rebate_equal_2(token=get_token['token'],
                                                    start=start,
                                                    end=end,
                                                    types=self_rebate_types,
                                                    amount=rebate_amount,
                                                    init_total_record=sle_init["rebate_record"]["total"])
    sle_search_for_win_prize_and_assert_equal_236_dot_86(token=get_token['token'],
                                                         start=start,
                                                         end=end,
                                                         types=win_prize_types,
                                                         amount=win_prize,
                                                         init_total_record=sle_init["win_prize_record"]["total"])

    cms_search_for_bet_and_assert_100_10(userId=f'SL3{username}',
                                         start=start,
                                         end=end,
                                         types=create_txn_types,
                                         amount=stakes[1],
                                         init_total_record=cms_init["create_record"]["total"])
    cms_search_for_revoke_bet_and_assert_amount_equal_1(userId=f'SL3{username}',
                                                        start=start,
                                                        end=end,
                                                        types=cancel_txn_types,
                                                        amount=stakes[0],
                                                        init_total_record=cms_init["cancel_record"]["total"])
    cms_search_for_rebate_and_assert_rebate_equal_2(userId=f'SL3{username}',
                                                    start=start,
                                                    end=end,
                                                    types=self_rebate_types,
                                                    amount=rebate_amount,
                                                    init_total_record=cms_init["rebate_record"]["total"])
    cms_search_for_win_prize_and_assert_equal_236_dot_86(userId=f'SL3{username}',
                                                         start=start,
                                                         end=end,
                                                         types=win_prize_types,
                                                         amount=win_prize,
                                                         init_total_record=cms_init["win_prize_record"]["total"])


def sle_init_record(token, start, end, create_types, cancel_types, rebate_types, win_prize_types):
    sle_init_create_record = sle.transaction_record(token=token,
                                                    start=start,
                                                    end=end,
                                                    types=create_types)
    sle_init_cancel_record = sle.transaction_record(token=token,
                                                    start=start,
                                                    end=end,
                                                    types=cancel_types)
    sle_init_rebate_record = sle.transaction_record(token=token,
                                                    start=start,
                                                    end=end,
                                                    types=rebate_types)
    sle_init_win_prize_record = sle.transaction_record(token=token,
                                                       start=start,
                                                       end=end,
                                                       types=win_prize_types)

    return {'create_record': sle_init_create_record,
            'cancel_record': sle_init_cancel_record,
            'rebate_record': sle_init_rebate_record,
            'win_prize_record': sle_init_win_prize_record}


def cms_init_record(userId, start, end, create_types, cancel_types, rebate_types, win_prize_types):
    cms_init_create_record = cms.transaction_record(userId=userId,
                                                    start=start,
                                                    end=end,
                                                    types=create_types)
    cms_init_cancel_record = cms.transaction_record(userId=userId,
                                                    start=start,
                                                    end=end,
                                                    types=cancel_types)
    cms_init_rebate_record = cms.transaction_record(userId=userId,
                                                    start=start,
                                                    end=end,
                                                    types=rebate_types)
    cms_init_win_prize_record = cms.transaction_record(userId=userId,
                                                       start=start,
                                                       end=end,
                                                       types=win_prize_types)

    return {'create_record': cms_init_create_record,
            'cancel_record': cms_init_cancel_record,
            'rebate_record': cms_init_rebate_record,
            'win_prize_record': cms_init_win_prize_record}


def sle_search_for_bet_and_assert_100_10(token, start, end, types, amount, init_total_record):
    record = sle.transaction_record(token=token,
                                    start=start,
                                    end=end,
                                    types=types)
    times = 0
    sleep = 5
    while record['total'] == init_total_record:
        time.sleep(sleep)
        times += 1
        record = sle.transaction_record(token=token,
                                        start=start,
                                        end=end,
                                        types=types)
        if times > 12:
            raise ValueError(f'Too slow to grab info to report, spend time: {times * sleep}')

    data1 = record['data'][0]
    pytest.assume(data1['txnType'] == types)
    pytest.assume(data1['in'] == False)
    pytest.assume(data1['afterBalance'] == data1['beforeBalance'] - amount)
    pytest.assume(data1['txnAmt'] == amount)

    data2 = record['data'][1]
    data2_amount = 1
    pytest.assume(data2['txnType'] == types)
    pytest.assume(data2['in'] == False)
    pytest.assume(data2['afterBalance'] == data2['beforeBalance'] - data2_amount)
    pytest.assume(data2['txnAmt'] == data2_amount)

    pytest.assume(init_total_record == record['total'] - 2)


def sle_search_for_revoke_bet_and_assert_amount_equal_1(token, start, end, types, amount, init_total_record):
    record = sle.transaction_record(token=token,
                                    start=start,
                                    end=end,
                                    types=types)
    data = record['data'][0]
    pytest.assume(data['txnType'] == types)
    pytest.assume(data['in'] == True)
    pytest.assume(data['afterBalance'] == data['beforeBalance'] + amount)
    pytest.assume(data['txnAmt'] == amount)

    pytest.assume(init_total_record == record['total'] - 1)


def sle_search_for_rebate_and_assert_rebate_equal_2(token, start, end, types, amount, init_total_record):
    record = sle.transaction_record(token=token, start=start, end=end, types=types)

    data = record['data'][0]
    pytest.assume(data['txnType'] == types)
    pytest.assume(data['in'] == True)
    pytest.assume(data['txnAmt'] == amount)
    pytest.assume(data['afterBalance'] == data['beforeBalance'] + amount)

    pytest.assume(init_total_record == record['total'] - 1)


def sle_search_for_win_prize_and_assert_equal_236_dot_86(token, start, end, types, amount, init_total_record):
    record = sle.transaction_record(token=token, start=start, end=end, types=types)

    data = record['data'][0]
    pytest.assume(data['txnType'] == types)
    pytest.assume(data['in'] == True)
    pytest.assume(data['txnAmt'] == amount)
    pytest.assume(data['afterBalance'] == float(f"{data['beforeBalance'] + amount:.4f}"))

    pytest.assume(init_total_record == record['total'] - 1)


def cms_search_for_bet_and_assert_100_10(userId, start, end, types, amount, init_total_record):
    record = cms.transaction_record(userId=userId, start=start, end=end, types=types)

    data1 = record['data'][0]
    pytest.assume(data1['txnType'] == types)
    pytest.assume(data1['in'] == False)
    pytest.assume(data1['afterBalance'] == data1['beforeBalance'] - amount)
    pytest.assume(data1['txnAmt'] == amount)
    pytest.assume(data1['userId'] == userId)
    pytest.assume(data1['createUser'] == userId)
    pytest.assume(data1['detailType'] == 'LOTTERY')

    data2 = record['data'][1]
    data2_amount = 1
    pytest.assume(data2['txnType'] == types)
    pytest.assume(data2['in'] == False)
    pytest.assume(data2['afterBalance'] == data2['beforeBalance'] - data2_amount)
    pytest.assume(data2['txnAmt'] == data2_amount)
    pytest.assume(data2['userId'] == userId)
    pytest.assume(data2['createUser'] == userId)
    pytest.assume(data2['detailType'] == 'LOTTERY')

    pytest.assume(init_total_record == record['total'] - 2)


def cms_search_for_revoke_bet_and_assert_amount_equal_1(userId, start, end, types, amount, init_total_record):
    record = cms.transaction_record(userId=userId, start=start, end=end, types=types)

    data = record['data'][0]
    pytest.assume(data['txnType'] == types)
    pytest.assume(data['in'] == True)
    pytest.assume(data['afterBalance'] == data['beforeBalance'] + amount)
    pytest.assume(data['txnAmt'] == amount)
    pytest.assume(data['userId'] == userId)
    pytest.assume(data['createUser'] == userId)
    pytest.assume(data['detailType'] == 'LOTTERY')

    pytest.assume(init_total_record == record['total'] - 1)


def cms_search_for_rebate_and_assert_rebate_equal_2(userId, start, end, types, amount, init_total_record):
    record = cms.transaction_record(userId=userId, start=start, end=end, types=types)

    data = record['data'][0]
    pytest.assume(data['txnType'] == types)
    pytest.assume(data['in'] == True)
    pytest.assume(data['txnAmt'] == amount)
    pytest.assume(data['afterBalance'] == data['beforeBalance'] + amount)
    pytest.assume(data['userId'] == userId)
    pytest.assume(data['createUser'] == 'SYSTEM')
    pytest.assume(data['detailType'] == 'LOTTERY')

    pytest.assume(init_total_record == record['total'] - 1)


def cms_search_for_win_prize_and_assert_equal_236_dot_86(userId, start, end, types, amount, init_total_record):
    record = cms.transaction_record(userId=userId, start=start, end=end, types=types)

    data = record['data'][0]
    pytest.assume(data['txnType'] == types)
    pytest.assume(data['in'] == True)
    pytest.assume(data['txnAmt'] == amount)
    pytest.assume(data['afterBalance'] == float(f"{data['beforeBalance'] + amount:.4f}"))
    pytest.assume(data['userId'] == userId)
    pytest.assume(data['createUser'] == 'SYSTEM')
    pytest.assume(data['detailType'] == 'LOTTERY')

    pytest.assume(init_total_record == record['total'] - 1)
