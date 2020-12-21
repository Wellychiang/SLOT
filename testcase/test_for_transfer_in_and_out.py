from . import allure
from . import Base
from . import cms
from . import pytest
from . import sle
from .bet_base import now_month
from .bet_base import now_day


@allure.feature('Scenario for transfer in and out check')
def test_for_transfer(username='welly1',
                      transfer_in_n_out_type='TRANSFER_IN,TRANSFER_OUT',
                      transfer_out_type='TRANSFER_OUT',
                      transfer_in_type='TRANSFER_IN',):
    start, end = Base().start_and_end_time(now_month, now_day, now_month, now_day)

    _, profile = sle.profile(username)
    balance = profile['wallets'][0]['balance']

    response = transfer_in_and_out(username)
    in_total = ec_search_for_transfer_in_assert(token=response['token'],
                                                start=start,
                                                end=end,
                                                types=transfer_in_type,
                                                balance=balance)

    out_total = ec_search_for_transfer_out_assert(token=response['token'],
                                                  start=start,
                                                  end=end,
                                                  types=transfer_out_type,
                                                  balance=balance)

    in_and_out_total = ec_search_for_transfer_in_and_out_assert(token=response['token'],
                                                                start=start,
                                                                end=end,
                                                                types=transfer_in_n_out_type,
                                                                balance=balance)

    pytest.assume(in_total == out_total)
    pytest.assume(in_and_out_total == (in_total + out_total))

    total = in_total
    transfer_type = transfer_in_type
    for i in range(2):
        cms_search_for_transfer_in_and_out_assert(userId=f'SL3{username}',
                                                  start=start,
                                                  end=end,
                                                  types=transfer_type,
                                                  balance=balance,
                                                  sle_total=total)
        total = out_total
        transfer_type = transfer_out_type


def transfer_in_and_out(username):
    _, response = sle.get_launch_token(username)
    sle.transfer_out(username)

    return response


def ec_search_for_transfer_in_assert(token, start, end, types, balance):
    record = sle.transaction_record(token=token,
                                    start=start,
                                    end=end,
                                    types=types)

    data = record['data'][0]
    pytest.assume(int(data['txnAmt'] * 100) == int(balance * 100))

    pytest.assume(data['txnType'] == types)
    pytest.assume(data['in'] == True)
    pytest.assume(data['afterBalance'] == float(balance))

    return record['total']


def ec_search_for_transfer_out_assert(token, start, end, types, balance):
    record = sle.transaction_record(token=token,
                                    start=start,
                                    end=end,
                                    types=types)

    data = record['data'][0]
    pytest.assume(int(data['txnAmt'] * 100) == int(balance * 100))

    balance = str(balance)[:-2]

    pytest.assume(data['txnType'] == types)
    pytest.assume(data['in'] == False)
    pytest.assume(str(data['afterBalance']) == str(data['beforeBalance'] - float(balance))[:6])

    return record['total']


def ec_search_for_transfer_in_and_out_assert(token, start, end, types, balance):
    record = sle.transaction_record(token=token,
                                    start=start,
                                    end=end,
                                    types=types)

    data_out = record['data'][0]
    data_in = record['data'][1]

    pytest.assume(data_in['txnType'] == types[:11])
    pytest.assume(data_in['in'] == True)
    pytest.assume(int(data_in['txnAmt'] * 100) == int(balance * 100))
    pytest.assume(data_in['afterBalance'] == float(balance))

    balance = str(balance)[:-2]
    pytest.assume(data_out['txnType'] == types[12:])
    pytest.assume(data_out['in'] == False)
    assert (str(data_out['afterBalance']) == str(data_out['beforeBalance'] - float(balance))[:6])

    return record['total']


def cms_search_for_transfer_in_and_out_assert(userId, start, end, types, balance, sle_total):
    record = cms.transaction_record(userId=userId,
                                    start=start,
                                    end=end,
                                    types=types)
    data = record['data'][0]
    pytest.assume(data['txnType'] == types)
    pytest.assume(int(data['txnAmt'] * 100) == int(balance * 100))
    pytest.assume(data['userId'] == userId)
    pytest.assume(data['createUser'] == 'SYSTEM')

    if types == 'TRANSFER_IN':
        pytest.assume(data['txnType'] == types)
        pytest.assume(data['in'] == True)
        pytest.assume(data['afterBalance'] == float(balance))
        pytest.assume(record['total'] == sle_total)

    elif types == 'TRANSFER_OUT':
        balance = str(balance)[:-2]

        pytest.assume(data['txnType'] == types)
        pytest.assume(data['in'] == False)
        pytest.assume(str(data['afterBalance']) == str(data['beforeBalance'] - float(balance))[:6])
        pytest.assume(record['total'] == sle_total)

    else:
        raise ValueError('Please input the right types')
