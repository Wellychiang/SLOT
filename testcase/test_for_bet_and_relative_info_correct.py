from testcase import allure
from testcase import Base
from testcase import cms
from testcase import log
from testcase import pytest
from testcase import sle
from testcase import time
from testcase.bet_base import bet
from testcase.bet_base import now_month
from testcase.bet_base import now_day
from testcase.bet_base import wait_for_bet_and_return_previous_or_current


@allure.feature()
@pytest.mark.skip()
def test_d(username='welly1',
           gameId='NYSSC1F',
           betString='s5vary1,1',
           playType='STANDALONE',
           count_down_second=15,
           playId=10009,
           playRateId=16476,
           rebatePackage=1940,
           stakes=(100, 1),
           create_txn_types='CREATE_TXN',
           cancel_txn_types='CANCEL_TXN'
           ):

    start, end = Base().start_and_end_time(now_month, now_day, now_month, now_day)
    bet_info = wait_for_bet_and_return_previous_or_current(gameId, count_down_second)
    _, get_token = sle.get_launch_token(username)
    sle_init_create_record = sle.transaction_record(token=get_token['token'],
                                                     start=start,
                                                     end=end,
                                                     types=create_txn_types)
    sle_init_cancel_record = sle.transaction_record(token=get_token['token'],
                                                    start=start,
                                                    end=end,
                                                    types=cancel_txn_types)
    bet_ids = []
    for stake in stakes:
        _, bet_i = bet(gameId=gameId,
                         playType=playType,
                         betString=betString,
                         playId=playId,
                         playRateId=playRateId,
                         rebatePackage=rebatePackage,
                         stake=stake,
                         token=get_token['token'],)
        time.sleep(1.5)
        bet_ids.append(bet_i)

    cancel_status_code, response = sle.cancel_bet(token=get_token['token'],
                                                   drawIdString=bet_info['current']['drawIdString'],
                                                   drawid=bet_info['current']['drawId'],
                                                   gameid=gameId,
                                                   txnid=bet_ids[1][0],)

    if cancel_status_code != 200 and response['total'] != 1:
        raise ValueError('Cancel bet failed')

    sle_search_for_bet_and_display_two(token=get_token['token'],
                                       start=start,
                                       end=end,
                                       types=create_txn_types,
                                       amount=100,
                                       init_total_record=sle_init_create_record['total'])

    sle_search_for_revoke_bet_and_display(token=get_token['token'],
                                          start=start,
                                          end=end,
                                          types=cancel_txn_types,
                                          amount=100,
                                          init_total_record=sle_init_cancel_record['total'])


def sle_search_for_bet_and_display_two(token, start, end, types, amount, init_total_record):
    record = sle.transaction_record(token=token,
                                    start=start,
                                    end=end,
                                    types=types)
    times = 0
    sleep = 5
    while record['total'] == init_total_record:
        time.sleep(sleep)
        times += 1
        if times > 12:
            raise ValueError(f'Too slow to grab info to report, spend time: {times * sleep}')

    data1 = record['data'][0]
    pytest.assume(data1['txnType'] == types)
    pytest.assume(data1['in'] == False)
    pytest.assume(data1['afterBalance'] == data1['beforeBalance'] - amount)

    data2 = record['data'][1]
    pytest.assume(data2['txnType'] == types)
    pytest.assume(data2['in'] == False)
    pytest.assume(data2['afterBalance'] == data2['beforeBalance'] - 1)

    assert init_total_record == record['total'] - 2


def sle_search_for_revoke_bet_and_display(token, start, end, types, amount, init_total_record):
    record = sle.transaction_record(token=token['token'],
                                    start=start,
                                    end=end,
                                    types=types)
    data1 = record['data'][0]
    pytest.assume(data1['txnType'] == types)
    pytest.assume(data1['in'] == False)
    pytest.assume(data1['afterBalance'] == data1['beforeBalance'] - amount)

    assert init_total_record == record['total'] - 1
