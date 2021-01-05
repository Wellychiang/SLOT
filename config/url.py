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
        vendor_game =                   'vendorGame'
        games =                         'games/'
        plays =                         'plays/'
        pnl =                           'pnl/'
        report =                        little_game + 'report/'
        records =                       report + 'records'
        room_record =                   report + 'roomRecord'
        account_record =                report + 'accountRecord'
        MX2 =                           draws + 'MX2/'
        clear =                         draws + 'clear/'
        status =                        games + 'status/'

        game =                          txn_reports + pnl + 'game'
        grp =                           txn_reports + pnl + 'grp'
        draw =                          txn_reports + pnl + 'draw'
        user =                          txn_reports + pnl + 'user'
        vendor =                        txn_reports + pnl + 'vendor'

        self.newtokens =                cms + newtokens
        self.bet_details =              cms + txn_reports.strip('/')
        self.draw_management =          cms + MX2
        self.lottery_draw =             cms + preset
        self.cls_report =               cms + grp
        self.single_profit_report =     cms + draw
        self.little_game_record =       cms + records
        self.little_game_get_or_patch = cms + little_game.strip('/')
        self.little_game_times_record = cms + room_record
        self.little_game_members_rp =   cms + account_record
        self.transaction_record =       cms + transaction_record
        self.singled_out_setting =      cms + vendor_game
        self.win_prize_limit =          cms + games.strip('/')
        self.draw_null =                cms + clear
        self.games_close_or_open =      cms + status
        self.game_report =              cms + user
        self.game_profit_report =       cms + game
        self.profit_loss_report =       cms + vendor
        self.lg_profit_loss_report =    cms + report + pnl.strip('/')

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

    def url_singled_out_setting(self):
        return self.singled_out_setting

    def url_win_prize_limit(self):
        return self.win_prize_limit

    def url_draw_null(self, period):
        return self.draw_null + period

    def url_games_close_or_open(self, gameId):
        return self.games_close_or_open + gameId

    def url_game_report(self):
        return self.game_report

    def url_game_profit_report(self):
        return self.game_profit_report

    def url_profit_loss_report(self):
        return self.profit_loss_report

    def url_lg_profit_loss_report(self):
        return self.lg_profit_loss_report


class UrlSle:

    def __init__(self, env='stg'):
        self.env = env

        sle = f'https://mx2-api.{env}devops.site/mx2-ecp/api/v1/'

        login =                             'login'
        get_bet_token =                     'games/NY/NY/NYSSC1F/launch'
        withdrawl =                         'withdrawals/'
        profile =                           'profile'
        apply_info =                        withdrawl + 'applyinfo'

        self.login =                        sle + login
        self.get_launch_token =             sle + get_bet_token
        self.transfer_out =                 sle + apply_info
        self.profile =                      sle + profile

        sle_portal = f'https://sle-api.{env}devops.site/sle-portal/v2/'

        txns =                              'txns/'
        draw =                              'draw/'
        active_and_previous =               f'{draw}activeandprevious/'
        little_game =                       'littleGame/'
        transaction_record =                'transactionrecord'
        create =                            little_game + 'create'
        play =                              little_game + 'play'
        cancel =                            txns + 'cancel'
        chase =                             txns + 'chase'

        self.txns =                         sle_portal + txns.strip('/')
        self.active_and_previous_period =   sle_portal + active_and_previous
        self.little_game_create =           sle_portal + create
        self.little_game_play =             sle_portal + play
        self.transaction_record =           sle_portal + transaction_record
        self.cancel_bet =                   sle_portal + cancel
        self.chase_bet =                    sle_portal + chase

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

    def url_cancel_bet(self):
        return self.cancel_bet

    def url_transfer_out(self):
        return self.transfer_out

    def url_profile(self):
        return self.profile

    def url_chase_bet(self):
        return self.chase_bet


class UrlAe:

    def __init__(self, env='stg'):

        self.env = env

        ae = f'https://ae-api.{env}devops.site/ae-ecp/api/v1/'

        games = 'games/AE_LOT/AE_LOT/Lobby/launch'

        self.launch_game =      ae + games
        self.login =            ae + 'login'


    def url_login(self):
        return self.login

    def url_launch_game(self):
        return self.launch_game
