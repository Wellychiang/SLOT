from . import allure
from . import Base
from . import cms
from . import sle
from . import ae
from . import time
from . import pytest
from . import log
from .bet_base import bet
from . import ROOT_ACCOUNT
from .bet_base import now_month
from .bet_base import now_day


@allure.feature(f"Scenario for verify two vendor's bet in profit loss report.")
@allure.step('')
def test_profit_loss_report(username=ROOT_ACCOUNT,
                            user=('welly1',),
                            gameId='NYSSC30S',
                            betString=('sum,big',),
                            playId=17,
                            playRateId=16553,
                            rebatePackage=1980,
                            vendor1='ISAPI',
                            vendor2='MX2',
                            ISAPI_stake=3,
                            MX2_stake=4,
                            odds=0.96,
                            currency='CNY',):
    start, end = Base().start_and_end_time(now_month,
                                           now_day,
                                           now_month,
                                           now_day)

    start = Base().return_now_start_time()

    get_token = ae.get_launch_token(username=user[0])
    if get_token.get('msg') == 'launch game fail':
        raise ValueError('AE get launch token failed')
    bet(gameId=gameId,
        betString=betString[0],
        playId=playId,
        playRateId=playRateId,
        rebatePackage=rebatePackage,
        stake=ISAPI_stake,
        token=get_token['token'],
        vendor=vendor1)

    _, get_token = sle.get_launch_token(username=user[0])
    if get_token.get('msg') == 'launch game fail':
        raise ValueError('Get games launch failed')
    bet(gameId=gameId,
        betString=betString[0],
        playId=playId,
        playRateId=playRateId,
        rebatePackage=rebatePackage,
        stake=MX2_stake,
        token=get_token['token'],
        vendor=vendor2)

    report = wait_for_reports_info_updated(username, start, end)
    assert_MX2_with_profit_loss_report(report,
                                       betUserCount=len(user),
                                       betCount=len(betString),
                                       txnCount=len(betString),
                                       stake=MX2_stake,
                                       validBet=MX2_stake,
                                       prizeWon=MX2_stake + (MX2_stake * odds),
                                       pnl=MX2_stake * odds,
                                       pnlRate=odds,
                                       currency=currency)

    assert_ISAPI_with_profit_loss_report(report,
                                         betUserCount=len(user),
                                         betCount=len(betString),
                                         txnCount=len(betString),
                                         stake=ISAPI_stake,
                                         validBet=ISAPI_stake,
                                         prizeWon=ISAPI_stake + (ISAPI_stake * odds),
                                         pnl=ISAPI_stake * odds,
                                         pnlRate=odds,
                                         currency=currency)


def assert_ISAPI_with_profit_loss_report(report,
                                         betUserCount,
                                         betCount,
                                         txnCount,
                                         stake,
                                         validBet,
                                         prizeWon,
                                         pnl,
                                         pnlRate,
                                         currency):
    for records in report['records']:
        if records['vendorId'] == 'ISAPI':
            pytest.assume(records['betUserCount'] == betUserCount)
            pytest.assume(records['betCount'] == betCount)
            pytest.assume(records['txnCount'] == txnCount)
            pytest.assume(records['stake'] == stake)
            pytest.assume(records['validBet'] == validBet)
            pytest.assume(records['presetValidBet'] is None)
            pytest.assume(records['notPresetPnl'] is None)
            pytest.assume(records['currency'] == currency)

            if records['prizeWon'] == 0:
                pytest.assume(records['pnl'] == -3)
                pytest.assume(records['pnlRate'] == -1)
            else:
                pytest.assume(records['prizeWon'] == prizeWon)
                pytest.assume(records['pnl'] == pnl)
                pytest.assume(records['pnlRate'] == pnlRate)


def assert_MX2_with_profit_loss_report(report,
                                       betUserCount,
                                       betCount,
                                       txnCount,
                                       stake,
                                       validBet,
                                       prizeWon,
                                       pnl,
                                       pnlRate,
                                       currency):
    for records in report['records']:
        if records['vendorId'] == 'MX2':
            pytest.assume(records['betUserCount'] == betUserCount)
            pytest.assume(records['betCount'] == betCount)
            pytest.assume(records['txnCount'] == txnCount)
            pytest.assume(records['stake'] == stake)
            pytest.assume(records['validBet'] == validBet)
            pytest.assume(records['presetValidBet'] is None)
            pytest.assume(records['notPresetPnl'] is None)
            pytest.assume(records['currency'] == currency)

            if records['prizeWon'] == 0:
                pytest.assume(records['pnl'] == -4)
                pytest.assume(records['pnlRate'] == -1)
            else:
                pytest.assume(records['prizeWon'] == prizeWon)
                pytest.assume(records['pnl'] == pnl)
                pytest.assume(records['pnlRate'] == pnlRate)



def wait_for_reports_info_updated(username, start, end):
    report = cms.profit_loss_report(username, start, end)

    times = 0
    while len(report['records']) == 0:
        log(f"wait for reports update")
        time.sleep(10)
        times += 1

        report = cms.profit_loss_report(username, start, end)

        if times > 6:
            raise ValueError(f"it's too slow to update report, spend time: 60")

    return report
