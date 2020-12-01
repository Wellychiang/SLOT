from testcase import cms, sle, time, log, Base, pytest, allure
from testcase.bet_base import bet, wait_and_lottery_draw, for_loop_bet_and_verify


now_month = time.strftime('%m')
now_day = time.strftime('%d')


@allure.feature('Scenario for bet and single profitloss report')
def test_bet_search_and_verify_report(username='spreport01',
                                      result='000123,111,111,222,222,45',
                                      gameId='NYTHAIFFC',
                                      playType='STANDALONE',
                                      betStrings=('1dtop,0', '1dtop,1', '1dtop,2', '1dtop,3', '1dtop,4',
                                                  '1dtop,5', '1dtop,6', '1dtop,7', '1dtop,8', '1dtop,9'),
                                      playId=90003,
                                      playRateId=102332,
                                      rebatePackage=1980,
                                      stake=1,
                                      times=1,
                                      report_start_month=now_month,
                                      report_start_day=now_day,
                                      report_end_month=now_month,
                                      report_end_day=now_day,
                                      assert_gameName='泰国快乐彩',
                                      assert_pnl=-0.4000,
                                      assert_pnlRate=-0.0400,
                                      assert_bet_user_count=1,
                                      assert_prizeWon=9.6):
    # 轉成timestamp
    todays_start, todays_end = Base().start_time_and_end_time(report_start_month,
                                                              report_start_day,
                                                              report_end_month,
                                                              report_end_day)
    drawId_at_this_time = sle.active_and_previous(gameId)

    _, txn_reports = cms.txn_reports(username='wellyadmin',
                                     tm_end=todays_end,
                                     tm_start=todays_start,
                                     drawIdString=drawId_at_this_time['current']['drawIdString'])

    while len(txn_reports['data']) != 0:
        log(f'Current draw id is already exist, count down second: '
            f'{drawId_at_this_time["current"]["countdown"]/1000 + 3}')
        time.sleep(drawId_at_this_time['current']['countdown']/1000 + 3)

    # 流到剩下17秒後, 先開獎
    wait_and_lottery_draw(result=result, gameId=gameId, count_down_second=20)

    _, get_token = sle.get_token(username=username)

    # launch, 投注 及他們自己之間都需要間隔1秒或以上, 不然會觸發duplicate
    time.sleep(1.5)

    # 一個帳號投10筆
    for_loop_bet_and_verify(gameId=gameId,
                            playType=playType,
                            betStrings=betStrings,
                            playId=playId,
                            playRateId=playRateId,
                            rebatePackage=rebatePackage,
                            stake=stake,
                            times=times,
                            token=get_token['token'])
    # 目前15秒差不多可以更新到報表
    time.sleep(15)

    list_infos = search_single_profitloss_report(drawIdString='202012011082',
                                                  report_start_month=report_start_month,
                                                  report_start_day=report_start_day,
                                                  report_end_month=report_end_month,
                                                  report_end_day=report_end_day, )

    for info in list_infos:
        log('Success iterable')
        if len(info) != 0:
            log('Success to go on a assertion')
            pytest.assume(info['gameId'] == gameId)
            pytest.assume(info['gameName'] == assert_gameName)
            pytest.assume(info['pnl'] == assert_pnl)
            pytest.assume(info['pnlRate'] == assert_pnlRate)
            pytest.assume(info['betCount'] == len(betStrings))
            pytest.assume(info['betUserCount'] == assert_bet_user_count)
            pytest.assume(info['stake'] == stake * len(betStrings))
            pytest.assume(info['validBet'] == stake * len(betStrings))
            assert info['prizeWon'] == assert_prizeWon

        else:
            raise ValueError('Nothing in the single profitloss report')


def search_single_profitloss_report(gameId='NYTHAIFFC|STANDALONE',
                                    drawIdString='',
                                    report_start_month=now_month,
                                    report_start_day=now_day,
                                    report_end_month=now_month,
                                    report_end_day=now_day, ):

    todays_start, todays_end = Base().start_time_and_end_time(report_start_month,
                                                              report_start_day,
                                                              report_end_month,
                                                              report_end_day)
    infos = cms.pnl_draw(end=todays_end,
                         start=todays_start,
                         drawIdString=drawIdString,
                         gameId=gameId)

    index = []

    for info_list in infos['records']:
        if info_list['gameId'] == gameId[:9]:
            log(f"Game id:              {info_list['gameId']}")
            log(f"Game name:            {info_list['gameName']}")
            log(f"Bet user count:       {info_list['betUserCount']}")
            log(f"Pnl(盈虧):             {info_list['pnl']}")
            log(f"Pnl rate(利潤率):      {info_list['pnlRate']}")
            log(f"Bet count:            {info_list['betCount']}")
            log(f"Stake:                {info_list['stake']}")
            log(f"Valid bet:            {info_list['validBet']}")
            log(f"Prize won:            {info_list['prizeWon']}")
        else:
            raise ValueError('gameId is not correct')

        index.append(info_list)
        log(info_list)
    return index
