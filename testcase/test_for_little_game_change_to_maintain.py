from testcase import allure
from testcase import Base
from testcase import cms
from testcase import log
from testcase import pytest
from testcase import sle
from testcase.bet_base import now_month
from testcase.bet_base import now_day


@allure.feature('Little game CMS change to maintain, check info correct')
def test_verify_info_with_setting_maintain(little_game_init_button,
                                            creator='lgmaintain01',
                                            amount=100,
                                            creator_choice='HEAD',
                                            gameId='SC',
                                            report_start_month=now_month,
                                            report_start_day=now_day,
                                            report_end_month=now_month,
                                            report_end_day=now_day):

    """
    目前是一天的第一次關閉或第一次維護遊戲,
    前端不會顯示關閉且可以繼續創建房間(限於開啟的第一個帳號, 明天可以用 edge 多開一個帳號試),
    且不會在關閉或維護時進行結算, 一樣多開一個帳號試, 且再確定是不是只有第一次關閉迴護才會
    可以一次開三個小遊戲, 然後開完房直接都進入維護
    """
    # Change to timestamp
    todays_start, todays_end = Base().start_and_end_time(report_start_month,
                                                         report_start_day,
                                                         report_end_month,
                                                         report_end_day)
    # Grab how much data init
    cms_record = cms.transaction_record(userId=f'SL3{creator}',
                                        start=todays_start,
                                        end=todays_end,
                                        types='LITTLE_GAME_CLOSE_RETURN_BET')

    _, get_token = sle.get_launch_token(creator)
    sle_record = sle.transaction_record(token=get_token['token'],
                                        types='LITTLE_GAME_CLOSE_RETURN_BET',
                                        start=todays_start,
                                        end=todays_end)

    cms_total_init = cms_record['total']
    sle_total_init = sle_record['total']
    log(f'CMS:{cms_total_init}\nSLE: {sle_total_init}')


    # Create a room and use maintain to close the room
    sle.little_game_create(token=get_token['token'],
                           amount=amount,
                           choice=creator_choice,
                           gameId=gameId,)

    cms.little_game_get_or_patch(SC_commission=5,
                                 method='patch',
                                 SC_status='MAINTAIN')



    # CMS  report
    cms_record = cms.transaction_record(userId=f'SL3{creator}',
                                        start=todays_start,
                                        end=todays_end,
                                        types='LITTLE_GAME_CLOSE_RETURN_BET')
    cms_total = cms_record['total']
    cms_record = cms_record['data'][0]

    pytest.assume(cms_record['afterBalance'] == cms_record['beforeBalance'] + amount)
    pytest.assume(cms_record['txnAmt'] == amount)
    pytest.assume(cms_record['userId'] == f'SL3{creator}')
    pytest.assume(cms_record['in'] is True)


    sle_record = sle.transaction_record(token=get_token['token'],
                                        start=todays_start,
                                        end=todays_end,
                                        types='LITTLE_GAME_CLOSE_RETURN_BET')
    sle_total = sle_record['total']
    sle_record = sle_record['data'][0]

    pytest.assume(cms_total == cms_total_init + 1)
    pytest.assume(sle_total == sle_total_init + 1)
    pytest.assume(cms_total == sle_total)

    pytest.assume(sle_record['afterBalance'] == sle_record['beforeBalance'] + amount)
    pytest.assume(sle_record['txnType'] == 'LITTLE_GAME_CLOSE_RETURN_BET')
    pytest.assume(sle_record['afterBalance'] == cms_record['afterBalance'])
    pytest.assume(sle_record['beforeBalance'] == cms_record['beforeBalance'])
    pytest.assume(sle_record['in'] == cms_record['in'] == True)
    pytest.assume(sle_record['txnAmt'] == cms_record['txnAmt'])
