from base import Base, log, UrlCms
import time


class Cms(Base):

    cms = UrlCms()

    # 注單明細查詢
    def txn_reports(self, username='imwelly',
                    limit='25',
                    offset='0',
                    prize_cmp='get',
                    tm_end='1605196799999',
                    tm_mode='txntime',
                    tm_start='1605110400000'):

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

        data = {
            'limit': limit,
            'offset': offset,
            'prizeCmp': prize_cmp,
            'tmMode': tm_mode,
            'tmEnd': tm_end,
            'tmStart': tm_start,
        }
        r = self.s.get(url, headers=headers, data=data)
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
        log(str(r.json()).encode('utf8').decode('cp950', 'ignore'))

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

        log(r.json())
        return r.json()

    # 單期盈虧報表
    def pnl_draw(self,
                 all='false',
                 drawIdString='202011300983',
                 end='1606838399999',
                 gameId='',
                 limit='100',
                 offset='0',
                 start='1606752000000',
                 username='wellyadmin'
                 ):

        url = self.cms.url_pnl_draw()
        _, get_token = self.cms_login(username)

        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
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
        log(r.json())
        return r.json