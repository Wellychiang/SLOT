class UrlCms:

    cms = 'https://sle-boapi.stgdevops.site/sle-cms/'

    _cms_newtokens = 'newTokens'
    _cms_txn_reports = 'txnreports'

    cms_newtokens = cms + _cms_newtokens
    cms_txn_reports = cms + _cms_txn_reports

    def __init__(self):
        pass

    def url_login(self):
        return self.cms_newtokens

    def url_txn_reports(self):
        return self.cms_txn_reports


class UrlSle:

    def __init__(self, env='stg'):
        self.env = env

        sle = f'https://mx2-api.{env}devops.site/mx2-ecp/api/v1/'

        sle_login = 'login'
        get_bet_token = 'games/NY/NY/NYSSC1F/launch'

        self.sle_login = sle + sle_login
        self.sle_get_bet_token = sle + get_bet_token

    def url_login(self):
        return self.sle_login

    def url_get_bet_token(self):
        return self.sle_get_bet_token

    sle_game_hall = 'https://sle-api.stgdevops.site/sle-portal/v2/'

    _sle_bet = 'txns'

    sle_bet = sle_game_hall + _sle_bet

    def url_bet(self):
        return self.sle_bet