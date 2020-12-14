from testcase import cms, sle, time, log, Base, pytest, allure

now_month = time.strftime('%m')
now_day = time.strftime('%d')


def bet(gameId='NYSSC3F',
        platform='Desktop',
        playType='SIMPLE',
        betString='sum,small',
        comment='',
        playId=17,
        playRateId=16080,
        rebatePackage=1980,
        stake=10,
        times=1,
        unit='DOLLAR',
        token=None,
        more_data=None):

    response = sle.active_and_previous_period(gameId)
    if response['current']['countdown'] <= 1000:
        wait_time = ((response['current']['countdown'] / 1000) + 3)

        log(f'\nCount down time is too short to verify, wait for the next lottery draw.\nCount down: {wait_time}')
        time.sleep(wait_time)

    drawId = response['current']['drawId']
    status_code, response = sle.bet(drawId,
                                    gameId,
                                    platform,
                                    playType,
                                    betString,
                                    comment,
                                    playId,
                                    playRateId,
                                    rebatePackage,
                                    stake,
                                    times,
                                    unit,
                                    token,
                                    more_data)

    return status_code, response


# count down < 1, will wait 3 second till next round
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


def wait_and_lottery_draw(result='410112,317,058,233,205,05',  # 自行開獎結果
                          gameId='NYTHAI3FC',
                          count_down_second=5):
    current_response = wait_for_bet_and_return_previous_or_current(gameId, count_down_second)

    # Lottery draw
    status_code = cms.lottery_draw(drawId=current_response['current']['drawId'],
                                   gameId=gameId,
                                   result=result, )

    if status_code != 200:
        raise ValueError(f'Failed with lottery draw , put status code: {status_code}')


# 等到開獎倒數幾秒, 就返回drawid等等, 小於13秒就等到下個round (幾秒(10)為預留給開獎的時間)
def wait_for_bet_and_return_previous_or_current(gameId, sleep_time):
    while True:
        response = sle.active_and_previous_period(gameId)
        count_down = response['current']['countdown']

        if count_down < 20000:
            log(f'Start to wait a new round')
            time.sleep(13)

        elif count_down >= 20000:
            start = time.time()
            log(f'Count down second: {int((count_down - int(f"{sleep_time}000")) / 1000)}')

            # sleep 到剩下幾秒秒
            time.sleep(int((count_down - int(f'{sleep_time}000')) / 1000))
            end = time.time()

            result = start - end

            log(f'Correct spend time: {result}')

            return response



