# from testcase.test_try import bet, bet_feature, cms, sle, time
# from base import log, Base
# import pytest
# import allure

from testcase import cms, sle, time, log, Base, pytest, allure
from testcase.test_try import bet

now_month = time.strftime('%m')
now_day = time.strftime('%d')


@allure.feature('Scenario for bet and classification report')
@allure.step('')
def test_winning_both(username=('autowelly001', 'clsreport01', 'clsreport04', 'yahoo'),
                      result='410112,317,058,233,205,05',
                      gameId='NYTHAIFFC',
                      playType='STANDALONE',
                      betStrings=('1dtop,1', '1dtop,2'),  # 需要用list或tuple, bet and draw funtion是用forloop展開
                      playId=90003,
                      playRateId=102332,
                      rebatePackage=1980,
                      stake=3,
                      times=1,
                      report_start_month=now_month,
                      report_start_day=now_day,
                      report_end_month=now_month,
                      report_end_day=now_day,
                      assert_gameName='泰国快乐彩',
                      assert_grp='1D头',
                      assert_pnl=13.2000,
                      assert_pnlRate=2.2000,
                      how_many_wins=2):

    bet_search_and_verify_report(username=username,
                                 gameId=gameId,
                                 playType=playType,
                                 betStrings=betStrings,
                                 playId=playId,
                                 playRateId=playRateId,
                                 rebatePackage=rebatePackage,
                                 stake=stake,
                                 times=times,
                                 report_start_month=report_start_month,
                                 report_start_day=report_start_day,
                                 report_end_month=report_end_month,
                                 report_end_day=report_end_day,
                                 assert_gameName=assert_gameName,
                                 assert_grp=assert_grp,
                                 assert_pnl=assert_pnl,
                                 assert_pnlRate=assert_pnlRate,
                                 how_many_wins=how_many_wins)



@allure.feature('Scenario for bet and classification report')
@allure.step('')
def test_winning_one_draw(username=('autowelly002', 'clsreport02', 'clsreport05'),
                          result='410112,317,058,233,205,05',  # 自行開獎結果
                          gameId='NYTHAIFFC',
                          playType='STANDALONE',
                          betStrings=('1dtop,1', '1dtop,6'),  # 需要用list或tuple, bet and draw funtion是用forloop展開
                          playId=90003,
                          playRateId=102332,
                          rebatePackage=1980,
                          stake=3,
                          times=1,
                          report_start_month=now_month,
                          report_start_day=now_day,
                          report_end_month=now_month,
                          report_end_day=now_day,
                          assert_gameName='泰国快乐彩',
                          assert_grp='1D头',
                          assert_pnl=3.6000,
                          assert_pnlRate=0.6000,
                          how_many_wins=1):

    bet_search_and_verify_report(username=username,
                                 gameId=gameId,
                                 playType=playType,
                                 betStrings=betStrings,
                                 playId=playId,
                                 playRateId=playRateId,
                                 rebatePackage=rebatePackage,
                                 stake=stake,
                                 times=times,
                                 report_start_month=report_start_month,
                                 report_start_day=report_start_day,
                                 report_end_month=report_end_month,
                                 report_end_day=report_end_day,
                                 assert_gameName=assert_gameName,
                                 assert_grp=assert_grp,
                                 assert_pnl=assert_pnl,
                                 assert_pnlRate=assert_pnlRate,
                                 how_many_wins=how_many_wins)


@allure.feature('Scenario for bet and classification report')
@allure.step('')
def test_lose_both_draw(username=('autowelly003', 'clsreport03', 'clsreport06'),
                        result='410112,317,058,233,205,05',
                           gameId='NYTHAIFFC',
                           playType='STANDALONE',
                           betStrings=('1dtop,6', '1dtop,7'),  # 需要用list或tuple, bet and draw funtion是用forloop展開
                           playId=90003,
                           playRateId=102332,
                           rebatePackage=1980,
                           stake=3,
                           times=1,
                           report_start_month=now_month,
                           report_start_day=now_day,
                           report_end_month=now_month,
                           report_end_day=now_day,
                           assert_gameName='泰国快乐彩',
                           assert_grp='1D头',
                           assert_pnl=-6.0000,
                           assert_pnlRate=-1.0000,
                           how_many_wins=0):

    bet_search_and_verify_report(username=username,
                                 gameId=gameId,
                                 playType=playType,
                                 betStrings=betStrings,
                                 playId=playId,
                                 playRateId=playRateId,
                                 rebatePackage=rebatePackage,
                                 stake=stake,
                                 times=times,
                                 report_start_month=report_start_month,
                                 report_start_day=report_start_day,
                                 report_end_month=report_end_month,
                                 report_end_day=report_end_day,
                                 assert_gameName=assert_gameName,
                                 assert_grp=assert_grp,
                                 assert_pnl=assert_pnl,
                                 assert_pnlRate=assert_pnlRate,
                                 how_many_wins=how_many_wins)


def bet_search_and_verify_report(username: list = ('autowelly004', 'clsreport01', 'clsreport02', 'clsreport03'),
                                  result='410112,317,058,233,205,05',
                                  gameId='NYTHAIFFC',
                                  playType='STANDALONE',
                                  betStrings=('1dtop,1', '1dtop,6'),  # 需要用list或tuple, bet and draw funtion是用forloop展開
                                  playId=90003,
                                  playRateId=102332,
                                  rebatePackage=1980,
                                  stake=3,
                                  times=1,
                                  report_start_month=now_month,
                                  report_start_day=now_day,
                                  report_end_month=now_month,
                                  report_end_day=now_day,
                                  assert_gameName='泰国快乐彩',
                                  assert_grp='1D头',
                                  assert_pnl=13.2000,
                                  assert_pnlRate=2.2000,
                                  how_many_wins=2):

    list_infos = search_classification_report(gameId=gameId,
                                              userId=f'SL3{username[0]}',
                                              report_start_month=report_start_month,
                                              report_start_day=report_start_day,
                                              report_end_month=report_end_month,
                                              report_end_day=report_end_day, )

    # 從拿到的分類報表檢查, 若是有資料便換個帳號, 直到找到帳號資料為0的, 才好判斷
    change_button = 0
    while len(list_infos) != 0:
        change_button += 1
        list_infos = search_classification_report(gameId=gameId,
                                                  userId=f'SL3{username[change_button]}',
                                                  report_start_month=report_start_month,
                                                  report_start_day=report_start_day,
                                                  report_end_month=report_end_month,
                                                  report_end_day=report_end_day, )

    log(f'Use user: {username[change_button]}')

    # 流到剩下八秒後, 先開獎
    wait_and_lottery_draw(result=result, gameId=gameId, count_down_second=8)

    _, get_token = sle.get_token(username=username[change_button])

    # launch, 投注 及他們自己之間都需要間隔1秒或以上, 不然會觸發duplicate
    time.sleep(1.5)

    # 一個帳號投兩筆
    for_loop_bet_and_verify(gameId=gameId,
                            playType=playType,
                            betStrings=betStrings,
                            playId=playId,
                            playRateId=playRateId,
                            rebatePackage=rebatePackage,
                            stake=stake,
                            times=times,
                            token=get_token['token'])
    # 目前15秒差不多可以更新到分類報表
    time.sleep(15)
    # 分類報表
    list_infos = search_classification_report(gameId=gameId,
                                              userId=f'SL3{username[change_button]}',
                                              report_start_month=report_start_month,
                                              report_start_day=report_start_day,
                                              report_end_month=report_end_month,
                                              report_end_day=report_end_day, )

    for info in list_infos:
        log('Success iterable')
        if len(info) != 0:
            log('im a normal assertion')
            pytest.assume(info['gameId'] == gameId)
            pytest.assume(info['gameName'] == assert_gameName)
            pytest.assume(info['grp'] == assert_grp)
            pytest.assume(info['pnl'] == assert_pnl)
            pytest.assume(info['pnlRate'] == assert_pnlRate)
            pytest.assume(info['betCount'] == len(betStrings))
            pytest.assume(info['stake'] == stake * len(betStrings))
            pytest.assume(info['validBet'] == stake * len(betStrings))
            if how_many_wins == 2:
                log('I won both')
                win_bet = 2
                pytest.assume(str(info['prizeWon']) in f'{stake * win_bet * 3.2:.4f}')
            elif how_many_wins == 1:
                log('I won one')
                win_bet = 1
                pytest.assume(str(info['prizeWon']) in f'{stake * win_bet * 3.2:.4f}')
            elif how_many_wins == 0:
                win_bet = 0
                pytest.assume(str(info['prizeWon']) in f'{stake * win_bet * 3.2:.4f}')
                log('Im loose both')

        else:
            raise ValueError('Nothing in the clsreport')


def search_classification_report(gameId='NYTHAIFFC',
                                 userId='SL3autowelly004',
                                 report_start_month=11,
                                 report_start_day=27,
                                 report_end_month=11,
                                 report_end_day=27, ):
    todays_start, todays_end = Base().start_time_and_end_time(report_start_month,
                                                              report_start_day,
                                                              report_end_month,
                                                              report_end_day)
    response = cms.pnl_grp(end=todays_end,
                           start=todays_start,
                           userId=userId)

    index = []
    for records_list in response['groupRecords']:
        for record_list in records_list['records']:
            if record_list['gameId'] == gameId:
                log(f"Game id:              {record_list['gameId']}")
                log(f"Game name:            {record_list['gameName']}")
                log(f"Grp(玩法):             {record_list['grp']}")
                log(f"Pnl(盈虧):             {record_list['pnl']}")
                log(f"Pnl rate(利潤率):      {record_list['pnlRate']}")
                log(f"Bet account:          {record_list['betCount']}")
                log(f"Stake:                {record_list['stake']}")
                log(f"Valid bet:            {record_list['validBet']}")
                log(f"Prize won:            {record_list['prizeWon']}")

                index.append(record_list)
    return index


def for_loop_bet_and_verify(token,
                            gameId='NYTHAI3FC',
                            playType='STANDALONE',
                            betStrings=('3droll,012',),
                            playId=90001,
                            playRateId=102377,
                            rebatePackage=1870,
                            stake=3,
                            times=1):
    """
    Thaihappy:
        betString = playRateId
        3dtop|000 = 102328, 3d|roll = 102329,  playId = 90001
        2dtop|01 = 102330, 2d|bottom = 102331, playId = 90002
        1dtop|1 = 102332, 1d|bottom = 102333 playId = 90003
    """

    log(f'Start bet')
    for betString in betStrings:

        _, response = bet(betString=betString,
                          gameId=gameId,
                          playType=playType,
                          playId=playId,
                          playRateId=playRateId,
                          rebatePackage=rebatePackage,
                          stake=stake,
                          times=times,
                          token=token)
        start = time.time()
        time.sleep(1.5)
        end = time.time()
        log(f'Spend time: {start-end}')
        if len(response) != 1:
            raise ValueError('Bet failed')

    return response


# 等到開獎倒數幾秒, 就返回drawid等等, 小於13秒就等到下個round (十秒為預留給開獎的時間)
def wait_for_bet_and_return_previous_or_current(gameId, sleep_time):
    while True:
        response = sle.active_and_previous(gameId)
        count_down = response['current']['countdown']

        if count_down < 13000:
            time.sleep(13)
            log(f'Start to wait the new round')

        elif count_down >= 13000:
            start = time.time()
            log(f'Count down second: {int((count_down - int(f"{sleep_time}000")) / 1000)}')

            # sleep 到剩下幾秒秒
            time.sleep(int((count_down - int(f'{sleep_time}000')) / 1000))
            end = time.time()

            result = start - end

            log(f'Start: {start}\nEnd: {end}')
            log(f'Result: {result}')

            return response


def wait_and_lottery_draw(result='410112,317,058,233,205,05',  # 自行開獎結果
                          gameId='NYTHAI3FC',
                          count_down_second=5):
    current_response = wait_for_bet_and_return_previous_or_current(gameId, count_down_second)

    # Lottery draw
    status_code = cms.preset(drawId=current_response['current']['drawId'],
                             gameId=gameId,
                             result=result, )

    if status_code != 200:
        raise ValueError(f'Failed with lottery draw , put status code: {status_code}')
