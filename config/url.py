class UrlCms:

    def __init__(self, env='stg'):
        self.env = env

        cms = f'https://sle-boapi.{env}devops.site/sle-cms/'

        newtokens =                     'newTokens'
        txn_reports =                   'txnreports/'
        draws =                         'draws/'
        preset =                        'preset'
        little_game =                   'littleGame/'
        transaction_record =            'transactionrecord'
        report =                        little_game + 'report/'
        records =                       report + 'records'
        room_record =                   report + 'roomRecord'
        account_record =                report + 'accountRecord'
        MX2 =                           draws + 'MX2/'

        pnl_grp =                       txn_reports + 'pnl/grp'
        pnl_draw =                      txn_reports + 'pnl/draw'

        self.newtokens =                cms + newtokens
        self.bet_details =              cms + txn_reports.strip('/')
        self.draw_management =          cms + MX2
        self.lottery_draw =             cms + preset
        self.cls_report =               cms + pnl_grp
        self.single_profit_report =     cms + pnl_draw
        self.little_game_record =       cms + records
        self.little_game_get_or_patch = cms + little_game.strip('/')
        self.little_game_times_record = cms + room_record
        self.little_game_members_rp =   cms + account_record
        self.transaction_record =       cms + transaction_record

    def url_login(self):
        return self.newtokens

    def url_bet_details(self):
        return self.bet_details

    def url_draw_management(self, gameId):
        return self.draw_management + gameId

    def url_lottery_draw(self):
        return self.lottery_draw

    def url_cls_report(self):
        return self.cls_report

    def url_single_profit_report(self):
        return self.single_profit_report

    def url_little_game_record(self):
        return self.little_game_record

    def url_little_game_get_or_patch(self):
        return self.little_game_get_or_patch

    def url_little_game_times_record(self):
        return self.little_game_times_record

    def url_little_game_members_report(self):
        return self.little_game_members_rp

    def url_transaction_record(self):
        return self.transaction_record


class UrlSle:

    def __init__(self, env='stg'):
        self.env = env

        sle = f'https://mx2-api.{env}devops.site/mx2-ecp/api/v1/'

        login =                             'login'
        get_bet_token =                     'games/NY/NY/NYSSC1F/launch'

        self.login =                        sle + login
        self.get_launch_token =             sle + get_bet_token


        sle_portal = f'https://sle-api.{env}devops.site/sle-portal/v2/'

        txns =                              'txns'
        draw =                              'draw/'
        active_and_previous =               f'{draw}activeandprevious/'
        little_game =                       'littleGame/'
        transaction_record =                'transactionrecord'
        create =                            little_game + 'create'
        play =                              little_game + 'play'


        self.txns =                         sle_portal + txns
        self.active_and_previous_period =   sle_portal + active_and_previous
        self.little_game_create =           sle_portal + create
        self.little_game_play =             sle_portal + play
        self.transaction_record =           sle_portal + transaction_record

    def url_login(self):
        return self.login

    def url_get_launch_token(self):
        return self.get_launch_token

    def url_txns(self):
        return self.txns

    def url_active_and_previous_period(self, bet_name):
        return f'{self.active_and_previous_period}{bet_name}'

    def url_little_game_create(self):
        return self.little_game_create

    def url_little_game_play(self):
        return self.little_game_play

    def url_transaction_record(self):
        return self.transaction_record
