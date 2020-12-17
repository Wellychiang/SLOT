from testcase import allure
from testcase import Base
from testcase import cms
from testcase import pytest
from testcase import sle
from testcase import time
from testcase.bet_base import bet
from testcase.bet_base import now_month
from testcase.bet_base import now_day


@allure.feature('Scenario for transfer in and out check')
@pytest.mark.skip()
def test_for_transfer(username='welly1',
                      transfer_in='TRANSFER_IN',
                      tranfer_out='TRANSFER_OUT'):

    start, end = Base().start_and_end_time(now_month, now_day, now_month, now_day)

    _, profile = sle.profile(username)
    balance = profile['wallets'][0]['balance']

    response = transfer_in_and_out(username)

    ec_search_for_transfer_in_or_out_assert(token=response['token'],
                                             start=start,
                                             end=end,
                                             types=transfer_in,
                                             balance=balance)

    # TODO: Think about the mix and single type's with a interface verify



def transfer_in_and_out(username):
    _, response = sle.get_launch_token(username)
    sle.transfer_out(username)

    return response


def ec_search_for_transfer_in_or_out_assert(token, start, end, types, balance):

    record = sle.transaction_record(token=token,
                                    start=start,
                                    end=end,
                                    types=types)



    data = record['data'][0]
    pytest.assume(data['txnType'] == types)
    pytest.assume(int(data['txnAmt'] * 100) == int(balance * 100))


    if types == 'TRANSFER_IN':
        pytest.assume(data['in'] == True)
        pytest.assume(data['afterBalance'] == float(balance))

    elif types == 'TRANSFER_OUT':
        balance = str(balance)[:-2]

        pytest.assume(data['in'] == False)
        pytest(str(data['afterBalance']) == str(data['beforeBalance'] - float(balance))[:6])

    else:
        raise ValueError('Please input the right types')




def cms_search_for_transfer_in_and_out_assert(userId, start, end, types, balance):
    record = cms.transaction_record(userId=userId,
                                    start=start,
                                    end=end,
                                    types=types)
    data = record['data'][0]
    pytest.assume(data['txnType'] == types)
    pytest.assume(int(data['txnAmt'] * 100) == int(balance * 100))

    if types == 'TRANSFER_IN':
        pytest.assume(data['in'] == True)
        pytest.assume(data['afterBalance'] == float(balance))

    elif types == 'TRANSFER_OUT':
        balance = str(balance)[:-2]

        pytest.assume(data['in'] == False)
        pytest(str(data['afterBalance']) == str(data['beforeBalance'] - float(balance))[:6])

    else:
        raise ValueError('Please input the right types')