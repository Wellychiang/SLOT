from testcase import cms, sle, time, log, Base, pytest, allure
from testcase.bet_base import bet, wait_and_lottery_draw, for_loop_bet_and_verify, now_month, now_day


@allure.feature("Scenario with bet's relative info")
def test_EC_CMS_transaction_record(creator='relativeinfo',
                                   player='relativeinfo1',
                                   amount=150,
                                   pull_water=0.09,
                                   two_creators_choice='ROCK',
                                   player_choice1='PAPER',
                                   player_choice2='ROCK',
                                   gameId='RPS',
                                   pie_chiang_types='LITTLE_GAME_PRIZE',
                                   draw_return_bet='LITTLE_GAME_DRAW_RETURN_BET',
                                   bet='LITTLE_GAME_BET',
                                   start_month=now_month,
                                   end_month=now_month,
                                   start_day=now_day,
                                   end_day=now_day,):

    start, end = Base().start_and_end_time(start_month, start_day, end_month, end_day)
    cms.little_game_get_or_patch(method='patch',
                                 RPS_commission=pull_water * 100)
    _, token = sle.get_launch_token(player)

    # Take EC, CMS's init report
    pie_chiang_init_record =      sle.transaction_record(token['token'], start, end, pie_chiang_types)
    draw_return_bet_init_record = sle.transaction_record(token['token'], start, end, draw_return_bet)
    bet_init =                    sle.transaction_record(token['token'], start, end, bet)
    cms_pie_chiang_init =         cms.transaction_record(start=start, end=end, types=pie_chiang_types, userId=f'SL3{player}')
    cms_return_bet_init =         cms.transaction_record(start=start, end=end, types=draw_return_bet, userId=f'SL3{player}')
    cms_bet_init =                cms.transaction_record(start=start, end=end, types=bet, userId=f'SL3{player}')

    # Create two rooms and play
    creator_room1, creator_room2 = create_two_room_with_rock(creator, amount, two_creators_choice, gameId)

    gameplay1, gameplay2 = play_two_room_with_rock_and_scissors(token,
                                                                gameId,
                                                                player_choice1,
                                                                player_choice2,
                                                                creator_room1,
                                                                creator_room2)

    # Assert creator and players response
    assert_two_rooms_response(gameplay1, gameplay2, creator_room1, creator_room2, amount, pull_water)

    # Take EC, CMS's report
    total_pie_chiang =      assert_lg_pie_chiang_in_wallet(token, start, end, pie_chiang_types, amount, pull_water)
    total_return_bet =      assert_lg_draw_return_bet_in_wallet(token, start, end, draw_return_bet, amount)
    total_bet =             assert_lg_bet(token, start, end, bet, amount)
    cms_total_pie_chiang =  assert_cms_lg_pie_chiang(start, end, pie_chiang_types, f'SL3{player}', amount, pull_water)
    cms_total_return_bet =  assert_cms_lg_draw_return_bet_in_wallet(start, end, draw_return_bet, f'SL3{player}', amount)
    cms_total_bet =         assert_cms_lg_bet(start, end, bet, f'SL3{player}', amount)

    # Assert about init and right now's report's total
    pytest.assume(total_pie_chiang ==       pie_chiang_init_record['total'] + 1)
    pytest.assume(total_return_bet ==       draw_return_bet_init_record['total'] + 1)
    pytest.assume(total_bet ==              bet_init['total'] + 2)
    pytest.assume(cms_total_pie_chiang ==   cms_pie_chiang_init['total'] + 1)
    pytest.assume(cms_total_return_bet ==   cms_return_bet_init['total'] + 1)
    assert cms_total_bet ==                 cms_bet_init['total'] + 2


def create_two_room_with_rock(creator='relativeinfo',
                              amount=10,
                              two_creators_choice='ROCK',
                              gameId='RPS'):

    _, token = sle.get_launch_token(creator)
    creator_room1 = sle.little_game_create(token=token['token'],
                                           amount=amount,
                                           choice=two_creators_choice,
                                           gameId=gameId)
    time.sleep(1)
    _, token = sle.get_launch_token(creator)
    creator_room2 = sle.little_game_create(token=token['token'],
                                           amount=amount,
                                           choice=two_creators_choice,
                                           gameId=gameId)

    return creator_room1, creator_room2


def play_two_room_with_rock_and_scissors(token=None,
                                         gameId='RPS',
                                         player_choice1='SCISSORS',
                                         player_choice2='ROCK',
                                         creator_room1=None,
                                         creator_room2=None):

    gameplay1 = sle.little_game_play(token=token['token'],
                                     gameId=gameId,
                                     choice=player_choice1,
                                     roomId=creator_room1['roomId'])

    gameplay2 = sle.little_game_play(token=token['token'],
                                     gameId=gameId,
                                     choice=player_choice2,
                                     roomId=creator_room2['roomId'])

    return gameplay1, gameplay2


def assert_two_rooms_response(gameplay1, gameplay2, creator_room1, creator_room2, amount, pull_water):

    pytest.assume(gameplay1['roomId'] == creator_room1['roomId'])
    pytest.assume(gameplay1['status'] == 'WIN')
    pytest.assume(gameplay1['creatorPick'] == creator_room1['creatorPick'])
    pytest.assume(gameplay1['amountResult'] == creator_room1['amount'] - (creator_room1['amount'] * pull_water))

    pytest.assume(gameplay2['roomId'] == creator_room2['roomId'])
    pytest.assume(gameplay2['status'] == 'DRAW')
    pytest.assume(gameplay2['creatorPick'] == creator_room2['creatorPick'])
    pytest.assume(gameplay2['amountResult'] == creator_room2['amount'] - amount)


def assert_lg_pie_chiang_in_wallet(token, start, end, types, amount, pull_water):
    record = sle.transaction_record(token['token'], start, end, types)
    
    pie_chiang = amount + (amount - (amount * pull_water))
    pytest.assume(record['data'][0]['txnType'] == 'LITTLE_GAME_PRIZE')
    pytest.assume(record['data'][0]['afterBalance'] == record['data'][0]['beforeBalance'] + pie_chiang)
    pytest.assume(record['data'][0]['txnAmt'] == pie_chiang)

    return record['total']


def assert_lg_draw_return_bet_in_wallet(token, start, end, types, amount):
    record = sle.transaction_record(token['token'], start, end, types)

    pytest.assume(record['data'][0]['in'] == True)
    pytest.assume(record['data'][0]['afterBalance'] == record['data'][0]['beforeBalance'] + amount)
    pytest.assume(record['data'][0]['txnAmt'] == amount)
    pytest.assume(record['data'][0]['txnType'] == 'LITTLE_GAME_DRAW_RETURN_BET')

    return record['total']


def assert_lg_bet(token, start, end, types, amount):
    record = sle.transaction_record(token['token'], start, end, types)

    pytest.assume(record['data'][0]['txnType'] == 'LITTLE_GAME_BET')
    pytest.assume(record['data'][0]['in'] == False)
    pytest.assume(record['data'][0]['txnAmt'] == amount)
    pytest.assume(record['data'][0]['afterBalance'] == record['data'][0]['beforeBalance'] - amount)

    return record['total']


def assert_cms_lg_pie_chiang(start, end, types, userId, amount, pull_water, username='wellyadmin'):
    record = cms.transaction_record(username=username, start=start, end=end, types=types, userId=userId)

    pie_chiang = amount + (amount - (amount * pull_water))
    pytest.assume(record['data'][0]['afterBalance'] == record['data'][0]['beforeBalance'] + pie_chiang)
    pytest.assume(record['data'][0]['in'] == True)
    pytest.assume(record['data'][0]['txnType'] == 'LITTLE_GAME_PRIZE')
    pytest.assume(record['data'][0]['txnAmt'] == pie_chiang)

    return record['total']


def assert_cms_lg_draw_return_bet_in_wallet(start, end, types, userId, amount, username='wellyadmin'):
    record = cms.transaction_record(username=username, start=start, end=end, types=types, userId=userId)

    pytest.assume(record['data'][0]['in'] == True)
    pytest.assume(record['data'][0]['afterBalance'] == record['data'][0]['beforeBalance'] + amount)
    pytest.assume(record['data'][0]['txnAmt'] == amount)
    pytest.assume(record['data'][0]['txnType'] == 'LITTLE_GAME_DRAW_RETURN_BET')
    pytest.assume(record['data'][0]['userId'] == userId)
    pytest.assume(record['data'][0]['detailType'] == 'MINI_GAME')

    return record['total']


def assert_cms_lg_bet(start, end, types, userId, amount, username='wellyadmin'):
    record = cms.transaction_record(username=username, start=start, end=end, types=types, userId=userId)

    pytest.assume(record['data'][0]['in'] == False)
    pytest.assume(record['data'][0]['afterBalance'] == record['data'][0]['beforeBalance'] - amount)
    pytest.assume(record['data'][0]['txnAmt'] == amount)
    pytest.assume(record['data'][0]['txnType'] == 'LITTLE_GAME_BET')
    pytest.assume(record['data'][0]['userId'] == userId)
    pytest.assume(record['data'][0]['detailType'] == 'MINI_GAME')

    return record['total']
