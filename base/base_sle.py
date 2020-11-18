from base.base import Base, log
from config.url import UrlCms, UrlSle
import requests


class Sle(Base):

    sle = UrlSle()

    def get_token(self, username='welly1'):

        url = self.sle.url_get_bet_token()

        _, get_token = self.sle_login(username)

        headers = {
            'Host': 'mx2-api.stgdevops.site',
            'Connection': 'keep-alive',
            'Content-Length': '33',
            'Accept': 'application/json, text/plain, */*',
            'Authorization': get_token['token'],
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/86.0.4240.193 Mobile Safari/537.36',
            'Content-Type': 'application/json',
            'Origin': 'https://mx2.stgdevops.site',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://mx2.stgdevops.site/',
            'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        }

        data = {
            "lang": "zh-CN",
            "platformtype": 1
        }

        r = self.s.put(url, headers=headers, json=data)
        log(r.json())

        return r.status_code, r.json()

    #  NYSSC15F = 上海1.5分3, betString map playRateId
    def bet(self,
            drawId='2020111200738',
            gameId='NYSSC15F',          # Lottery species
            platform='Desktop',
            playType='SIMPLE',
            betString='sum|small',      # Bet option, changed this will effect playRateId
            comment='',
            playId=17,                  # Lottery species's play option,
            playRateId=16080,
            rebatePackage=None,
            stake=10,                   # Bet moeny
            times=1,                    # Bet how many times, like stake*1, this bet money is 10
            unit='DOLLAR',
            token=None,
            more_data=None):

        url = self.sle.url_txns()

        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'authorization': f"{token}",
            'content-length': '222',
            'content-type': 'application/json',
            'origin': 'https://mx2.stgdevops.site',
            'referer': 'https://mx2.stgdevops.site/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/86.0.4240.193 Mobile Safari/537.36',
            'x-vendor-id': 'MX2',
        }
        data = {
            'drawId': drawId,
            'gameId': gameId,
            'platform': platform,
            'playType': playType,
            'txns': [{
                'betString': betString,
                'comment': comment,
                'playId': playId,
                'playRateId': playRateId,
                'rebatePackage': rebatePackage,
                'stake': stake,
                'times': times,
                'unit': unit,
            }]
        }

        if more_data is not None:
            data['txns'].append(more_data)

        r = requests.post(url, headers=headers, json=data, verify=False)
        log(f'\nResponse: {r.json()}')

        return r.status_code, r.json()

    def active_and_previous(self, gameId):

        url = self.sle.url_active_and_previous(gameId)

        r = self.s.get(url)

        log(r.json())
        return r.json()
