class UrlCms:

    def __init__(self, env='stg'):
        self.env = env

        cms = f'https://sle-boapi.{env}devops.site/'

        sle_cms =               'sle-cms/'
        newtokens =             sle_cms + 'newTokens'
        txn_reports =           sle_cms + 'txnreports/'
        draws =                 sle_cms + 'draws/'
        MX2 =                   draws + 'MX2/'
        preset =                sle_cms + 'preset'
        pnl_grp =               txn_reports + 'pnl/grp'

        self.newtokens =        cms + newtokens
        self.txn_reports =      cms + txn_reports
        self.MX2 =              cms + MX2
        self.preset =           cms + preset
        self.pnl_grp =          cms + pnl_grp

    def url_login(self):
        return self.newtokens

    def url_txn_reports(self):
        return self.txn_reports

    def url_MX2(self, gameId):
        return self.MX2 + gameId

    def url_preset(self):
        return self.preset

    def url_pnl_grp(self):
        return self.pnl_grp


class UrlSle:

    def __init__(self, env='stg'):
        self.env = env

        sle =                       f'https://mx2-api.{env}devops.site/mx2-ecp/api/v1/'

        login =                     'login'
        get_bet_token =             'games/NY/NY/NYSSC1F/launch'
        self.login =                sle + login
        self.get_bet_token =        sle + get_bet_token


        sle_portal =                f'https://sle-api.{env}devops.site/sle-portal/v2/'

        txns =                      'txns'
        draw =                      'draw/'
        active_and_previous =       f'{draw}activeandprevious/'
        self.txns =                 sle_portal + txns
        self.active_and_previous =  sle_portal + active_and_previous

    def url_login(self):
        return self.login

    def url_get_bet_token(self):
        return self.get_bet_token

    def url_txns(self):
        return self.txns

    def url_active_and_previous(self, gameId):
        return f'{self.active_and_previous}{gameId}'
