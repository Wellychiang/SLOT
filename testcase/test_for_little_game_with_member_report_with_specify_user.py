from testcase import cms, sle, time, log, Base, pytest, allure
from testcase.bet_base import bet, wait_and_lottery_draw, for_loop_bet_and_verify, now_month, now_day


@allure.feature("Scenario for ")
@pytest.mark.d
def tes_aa(username=('memberreport', 'memberreport1', 'memberreport2'),
            amount="20",
            choice="HI",
            gameId="HL"):

    members_report = cms.little_game_members_report()

    change_button = 0
    if len(members_report['records']) != 0:

        _, get_token = sle.get_launch_token(username[0])
        sle.little_game_create(token='123',
                               amount=amount,
                               choice=choice,
                               gameId=gameId,)
