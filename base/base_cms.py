from base import Base, log, UrlCms
import time


class Cms(Base):

    cms = UrlCms()

    # 注單明細查詢
    def txn_reports(self,
                    username='imwelly',
                    limit='25',
                    offset='0',
                    prize_cmp='gte',
                    tm_end='1605196799999',
                    tm_mode='txntime',
                    tm_start='1605110400000',
                    drawIdString=None):

        url = self.cms.url_txn_reports()
        _, get_token = self.cms_login(username)

        headers = {
            'accept': '*/*',
            'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'authorization': get_token['token'],
            'origin': 'https://sle-bo.stgdevops.site',
            'referer': 'https://sle-bo.stgdevops.site/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/86.0.4240.193 Safari/537.36',
        }

        params = {
            'limit': limit,
            'offset': offset,
            'prizeCmp': prize_cmp,
            'tmMode': tm_mode,
            'tmEnd': tm_end,
            'tmStart': tm_start,
            'drawIdString': drawIdString
        }
        r = self.s.get(url, headers=headers, params=params)
        log(f'Response: {r.json()}')

        return r.status_code, r.json()

    # 開獎管理查詢 (imwelly帳號無法查詢, 是因為是輸入獎號帳號)
    def MX2(self,
            gameId='NYTHAIFFC',
            startBefore=int(float(time.time()) * 1000),  # 開獎日期
            drawIdString=None,  # 獎號 (可以為None)
            username='wellyadmin'):

        url = self.cms.url_MX2(gameId)
        _, get_token = self.cms_login(username)

        headers = {
            'accept': '*/*',
            'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'authorization': get_token['token'],
            'origin': 'https://sle-bo.stgdevops.site',
            'referer': 'https://sle-bo.stgdevops.site/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/86.0.4240.198 Safari/537.36',
        }

        params = {
            'expand': 'crawlerResult',
            'startBefore': startBefore,
            'drawIdString': drawIdString,
        }
        log(url)
        r = self.s.get(url, headers=headers, params=params)
        log(f"Response: {str(r.json()).encode('utf8').decode('cp950', 'ignore')}")

        return r.json()

    # 自行開獎, 只能用imwelly帳號 (輸入獎號帳號)
    def preset(self,
               drawId=2020111900340,
               gameId="NYSSC3F",
               result="1,2,3,4,5",
               username='imwelly'):

        url = self.cms.url_preset()
        _, get_token = self.cms_login(username)

        headers = {
            'accept': '*/*',
            'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'authorization': get_token['token'],
            'content-length': '64',
            'content-type': 'application/json;charset=UTF-8',
            'origin': 'https://sle-bo.stgdevops.site',
            'referer': 'https://sle-bo.stgdevops.site/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/86.0.4240.198 Safari/537.36',
        }

        result = result.split(',')

        data = {
            'drawId':  drawId,
            'gameId':  gameId,
            'result':  '|'.join(result)
        }

        r = self.s.post(url, headers=headers, json=data)
        log(r.status_code)

        return r.status_code

    # 分類報表
    def pnl_grp(self,
                end=1606147199999,
                start=1606060800000,
                userId='SL3yahoo',
                vendorId='MX2',
                username='wellyadmin'):

        url = self.cms.url_pnl_grp()
        _, get_token = self.cms_login(username)

        headers = {
            'accept': '*/*',
            'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'authorization': get_token['token'],
            'origin': 'https://sle-bo.stgdevops.site',
            'referer': 'https://sle-bo.stgdevops.site/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/86.0.4240.198 Safari/537.36',
        }

        params = {
            'end': end,
            'start': start,
            'userId': userId,
            'vendorId': vendorId,
        }

        r = self.s.get(url, headers=headers, params=params)

        log(f'Response: {r.json()}')

        return r.json()

    # 單期盈虧報表
    def pnl_draw(self,
                 all=False,
                 drawIdString='20201201230',
                 end='1606838399999',
                 gameId='',
                 limit='100',
                 offset='0',
                 start='1606752000000',
                 username='wellyadmin'):

        url = self.cms.url_pnl_draw()
        _, get_token = self.cms_login(username)

        headers = {
            'accept': '*/*',
            'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'authorization': get_token['token'],
            'origin': 'https://sle-bo.stgdevops.site',
            'referer': 'https://sle-bo.stgdevops.site/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/86.0.4240.198 Safari/537.36',
        }

        params = {
            'all': all,
            'drawIdString': drawIdString,
            'end': end,
            'gameId': gameId,
            'limit': limit,
            'offset': offset,
            'start': start,
        }

        r = self.s.get(url, headers=headers, params=params)
        log(f'Response: {r.json()}')

        return r.json()

    # 小遊戲 > 遊戲紀錄
    def little_game_report(self,
                           username='wellyadmin',
                           endTime='1606924799999',
                           limit='25',
                           offset='0',
                           startTime='1606838400000',
                           userId=None,
                           roomId=None,
                           vendorId='MX2',
                           ):

        url = self.cms.url_little_game_report()

        _, get_token = self.cms_login(username)

        headers = {
            'accept': '*/*',
            'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'authorization': get_token['token'],
            'origin': 'https://sle-bo.stgdevops.site',
            'referer': 'https://sle-bo.stgdevops.site/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/86.0.4240.198 Safari/537.36',
        }

        params = {
            'endTime': endTime,
            'limit': limit,
            'offset': offset,
            'startTime': startTime,
            'userId': userId,
            'roomId': roomId,
            'vendorId': vendorId,
        }

        r = self.s.get(url, headers=headers, params=params)
        log(f'Response: {r.json()}')

        return r.json()

    # Patch != True, get report
    def little_game_patch(self,
                          username='wellyadmin',
                          commission=5,
                          patch=True,):
        url = self.cms.url_little_game_patch()

        _, get_token = self.cms_login(username)

        headers = {
            'accept': '*/*',
            'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'authorization': get_token['token'],
            'origin': 'https://sle-bo.stgdevops.site',
            'referer': 'https://sle-bo.stgdevops.site/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/86.0.4240.198 Safari/537.36',
        }

        if patch:
            data = {
                "vendorId": "MX2",
                "data":
                    [{"commission": commission, "betAmountItems":
                        ["10", "40", "100", "150", "300", "500", "800", "9990", "1234560"],
                      "status": "NORMAL", "gameId": "SC"},
                     {"commission": "31.7", "betAmountItems":
                         ["10", "20", "40", "90", "150", "500", "800", "1600", "3200"],
                      "status": "NORMAL", "gameId": "RPS"},
                     {"commission": "11.7", "betAmountItems":
                         ["20", "50", "110", "150", "300", "490", "800", "1600", "9999990"],
                      "status": "NORMAL", "gameId": "HL"}]
        }
            r = self.s.patch(url, headers=headers, json=data)
            log(f'\nResponse: {r.status_code}')

            return r.status_code
        else:
            data = {
                'vendorId': 'MX2'
            }

            r = self.s.get(url, headers=headers, data=data)
            log(f'\nResponse: {r.json()}')

            return r.json()
