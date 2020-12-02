class UrlCms:

    def __init__(self, env='stg'):
        self.env = env

        cms = f'https://sle-boapi.{env}devops.site/'

        sle_cms =                   'sle-cms/'
        newtokens =                 sle_cms + 'newTokens'
        txn_reports =               sle_cms + 'txnreports/'
        draws =                     sle_cms + 'draws/'
        preset =                    sle_cms + 'preset'
        little_game_report =        sle_cms + 'littleGame/report/records'
        little_game_patch =         sle_cms + 'littleGame'
        MX2 =                       draws + 'MX2/'


        pnl_grp =                   txn_reports + 'pnl/grp'
        pnl_draw =                  txn_reports + 'pnl/draw'

        self.newtokens =            cms + newtokens
        self.txn_reports =          cms + txn_reports.strip('/')
        self.MX2 =                  cms + MX2
        self.preset =               cms + preset
        self.pnl_grp =              cms + pnl_grp
        self.pnl_draw =             cms + pnl_draw
        self.little_game_report =   cms + little_game_report
        self.little_game_patch =    cms + little_game_patch

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

    def url_pnl_draw(self):
        return self.pnl_draw

    def url_little_game_report(self):
        return self.little_game_report

    def url_little_game_patch(self):
        return self.little_game_patch


class UrlSle:

    def __init__(self, env='stg'):
        self.env = env

        sle = f'https://mx2-api.{env}devops.site/mx2-ecp/api/v1/'

        login =                     'login'
        get_bet_token =             'games/NY/NY/NYSSC1F/launch'
        self.login =                sle + login
        self.get_bet_token =        sle + get_bet_token


        sle_portal = f'https://sle-api.{env}devops.site/sle-portal/v2/'

        txns =                      'txns'
        draw =                      'draw/'
        active_and_previous =       f'{draw}activeandprevious/'
        little_game_create =        'littleGame/create'
        little_game_play =          'littleGame/play'
        self.txns =                 sle_portal + txns
        self.active_and_previous =  sle_portal + active_and_previous
        self.little_game_create =   sle_portal + little_game_create
        self.little_game_play =     sle_portal + little_game_play

    def url_login(self):
        return self.login

    def url_get_bet_token(self):
        return self.get_bet_token

    def url_txns(self):
        return self.txns

    def url_active_and_previous(self, bet_name):
        return f'{self.active_and_previous}{bet_name}'

    def url_little_game_create(self):
        return self.little_game_create

    def url_little_game_play(self):
        return self.little_game_play