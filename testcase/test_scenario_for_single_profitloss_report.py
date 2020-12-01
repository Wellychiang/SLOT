from testcase import cms, sle, time, log, Base, pytest, allure
# from testcase.test_try import bet
from testcase.test_scenario_for_search_member_with_classification_report import search_classification_report


@allure.feature('Scenario with scenario single profitloss report')
@allure.step('')
@pytest.mark.dd
def est_winning_bot(username=('autowelly001', 'clsreport01', 'clsreport04', 'yahoo'),
                      result='410112,317,058,233,205,05',
                      gameId='NYTHAIFFC',
                      playType='STANDALONE',
                      betStrings=('1dtop,1', '1dtop,2'),  # 需要用list或tuple, bet and draw funtion是用forloop展開
                      playId=90003,
                      playRateId=102332,
                      rebatePackage=1980,
                      stake=3,
                      times=1,
                      # report_start_month=now_month,
                      # report_start_day=now_day,
                      # report_end_month=now_month,
                      # report_end_day=now_day,
                      assert_gameName='泰国快乐彩',
                      assert_grp='1D头',
                      assert_pnl=13.2000,
                      assert_pnlRate=2.2000,
                      how_many_wins=2):
    search_classification_report()


