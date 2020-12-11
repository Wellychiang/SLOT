from testcase import cms, sle, time, log, Base, pytest, allure
from testcase.bet_base import bet, wait_and_lottery_draw, for_loop_bet_and_verify, now_month, now_day


@allure.feature()
@pytest.mark.skip()
def test_d(username='welly1',
           gameId='TXFFC',
           playType='SIMPLE',
           prizeLimit=500,
           cancel_win_prize_types='CANCEL_WIN_PRIZE',
           win_prize_type='WIN_PRIZE',
           over_win_prize_type='OVER_WIN_PRIZE'):

    start, end = Base().start_and_end_time(now_month, now_day, now_month, now_day)

    _, token = sle.get_launch_token(username)

    # TODO: 需要對比最初的 total 跟新增過後是否確實有加, 且加 1
    # init_sle_trans = sle.transaction_record(token['token'], start, end, types=win_prize_type)
    # init_cms_trans = cms.transaction_record(userId=f'SL3{username}', start=start, end=end, types=win_prize_type)

    # cms.win_prize_limit(gameId=gameId,
    #                     playType=playType,
    #                     prizeLimit=prizeLimit,)

    # TODO: 下注藤信紛紛採 大, 小, 各500, 然後等到開獎

    # TODO: 斷言撤銷派彩, 中獎(Done)
    # sle_cancel_win_prize_equal_zero(token, start, end, types=cancel_win_prize_types)
    # sle_win_prize_search_and_display_500(token, start, end, types=win_prize_type, amount=prizeLimit)

    # TODO: 勾選超額中獎扣除並提交, 和勾選彩票派獎並提交
    # cms_over_win_minus(start, end, userId=None, types=over_win_prize_type)
    # cms_win_prize_search_and_display_500(start, end, userId=f'SL3{username}', types=win_prize_type, amount=prizeLimit)

    # TODO: 騰訊紛紛採 空開

    # TODO: 勾選中獎返還並提交 (暫無資料)

    # TODO: 勾選撤銷派彩並提交(顯示500)

    # TODO: 勾選空開撤單並提交(有兩筆, 顯示空開且500)

    # TODO:


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


