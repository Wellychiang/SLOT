from base import Base, log, UrlSle
import time


class Sle(Base):

    sle = UrlSle()

    # Launch game
    def get_launch_token(self, username='welly1'):

        url = self.sle.url_get_launch_token()

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
        log(f"\nGet game's launch token:\n{r.json()}")
        time.sleep(1)

        return r.status_code, r.json()

    #  NYSSC15F = 上海1.5分3, betString map playRateId
    def bet(self,
            drawId='2020111200738',
            gameId='NYSSC15F',          # Lottery species
            platform='Desktop',
            playType='SIMPLE',
            betString='sum,small',      # Bet option, changed this will effect playRateId
            comment='',
            playId=17,                  # Lottery species's play option,
            playRateId=16080,
            rebatePackage=None,
            stake=10,                   # Bet moeny
            times=1,                    # Bet how many times, like stake*1, this bet money is 10
            unit='DOLLAR',
            token=None,
            more_data=None,
            vendor='MX2'):

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
            'x-vendor-id': vendor,
        }

        betString = betString.split(',')
        data = {
            'drawId': drawId,
            'gameId': gameId,
            'platform': platform,
            'playType': playType,
            'txns': [{
                'betString': '|'.join(betString),
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

        r = self.s.post(url, headers=headers, json=data, verify=False)
        log(f'\nBet:\n{r.json()}')

        return r.status_code, r.json()

    def active_and_previous_period(self, gameId):

        url = self.sle.url_active_and_previous_period(gameId)

        r = self.s.get(url)

        log(f"\nActive and previous period:\n{r.json()}")
        return r.json()

    def little_game_create(self,
                           token=None,
                           amount="10",
                           choice="HEAD",
                           gameId="SC",
                           platform="Desktop"):

        url = self.sle.url_little_game_create()

        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'authorization': token,
            'content-length': '66',
            'content-type': 'application/json',
            'origin': 'https://mx2.stgdevops.site',
            'referer': 'https://mx2.stgdevops.site/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/86.0.4240.198 Mobile Safari/537.36',
            'x-vendor-id': 'MX2',
        }

        data = {
            'amount': amount,
            'choice': choice,
            'gameId': gameId,
            'platform': platform,
        }

        r = self.s.post(url, headers=headers, json=data)
        log(f"\nLittle game's create:\n{r.json()}")

        return r.json()

    def little_game_play(self,
                         token=None,
                         choice="TAIL" or 'HEAD',
                         gameId="SC" or "RPS" or "HL",
                         platform="Desktop",
                         roomId=1271981426123892,):

        url = self.sle.url_little_game_play()

        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'authorization': token,
            'content-length': '78',
            'content-type': 'application/json',
            'origin': 'https://mx2.stgdevops.site',
            'referer': 'https://mx2.stgdevops.site/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/86.0.4240.198 Mobile Safari/537.36',
            'x-vendor-id': 'MX2',
        }

        data = {
            'choice': choice,
            'gameId': gameId,
            'platform': platform,
            'roomId': roomId,
        }

        r = self.s.post(url, headers=headers, json=data)
        log(f"\nLittle game's play:\n{r.json()}")

        return r.json()

    def transaction_record(self,
                           token=None,
                           start='1607270400000',
                           end='1607443199999',
                           types='LITTLE_GAME_DRAW_RETURN_BET,'
                                 'LITTLE_GAME_TIMEOUT_RETURN_BET,'
                                 'LITTLE_GAME_CLOSE_RETURN_BET',
                           offset='0',):

        url = self.sle.url_transaction_record()

        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'authorization': token,
            'origin': 'https://mx2.stgdevops.site',
            'referer': 'https://mx2.stgdevops.site/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 ABuild/MRA58N) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36',
            'x-vendor-id': 'MX2',
        }

        params = {
            'start': start,
            'end': end,
            'types': types,
            'offset': offset,
        }

        r = self.s.get(url, headers=headers, params=params)
        log(f"\rTransaction record: {r.json()}")

        return r.json()

    def cancel_bet(self,
                   token=None,
                   drawIdString='202012160932',
                   drawid='2020121600932',
                   gameid='NYSSC1F',
                   txnid='1282027396351040',
                   ):
        url = self.sle.url_cancel_bet()

        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'authorization': token,
            'content-length': '100',
            'content-type': 'application/json',
            'origin': 'https://mx2.stgdevops.site',
            'referer': 'https://mx2.stgdevops.site/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 '
                          '(KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
            'x-vendor-id': 'MX2',
        }

        data = [{
            'drawIdString': drawIdString,
            'drawid': drawid,
            'gameid': gameid,
            'txnid': txnid,
        }]

        r = self.s.put(url, headers=headers, json=data)
        log(f"Cancel bet:{r.json()}\nStatus code: {r.status_code}")

        return r.status_code, r.json()

    def transfer_out(self, username='welly1'):
        url = self.sle.url_transfer_out()

        _, get_token = self.sle_login(username)
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'authorization': get_token['token'],
            'origin': 'https://mx2.stgdevops.site',
            'referer': 'https://mx2.stgdevops.site/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 '
                          '(KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
        }
        params = {
            'language': 2
        }
        r = self.s.get(url, headers=headers, params=params)
        log(f"Status code: {r.status_code}")

        return r.status_code

    def profile(self, username='welly1'):
        url = self.sle.url_profile()

        _, get_token = self.sle_login(username)
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'authorization': get_token['token'],
            'origin': 'https://mx2.stgdevops.site',
            'referer': 'https://mx2.stgdevops.site/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 '
                          '(KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
        }

        r = self.s.get(url, headers=headers)
        log(f"Status code: {r.status_code}\nProfile{r.json()}")

        return r.status_code, r.json()

    def chase_bet(self,
                  gameId='NYK31F',
                  playType='STANDALONE',
                  betString='s3sum|3',
                  playId=30001,
                  playRateId=14876,
                  rebatePackage=1980,
                  stake=1,
                  drawId=None,
                  token='token',
                  vendorId='MX2'):

        url = self.sle.url_chase_bet()

        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'authorization': token,
            'origin': 'https://mx2.stgdevops.site',
            'referer': 'https://mx2.stgdevops.site/',
            'content-type': 'application/json',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 '
                          '(KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
            'x-vendor-id': vendorId
        }
        data = {
                "gameId": gameId,
                "platform": "Desktop",
                "playType": playType,
                "stopIfOpenNull": True,
                "stopIfWin": True,
                "chasePlans": [
                    {
                        "betString": betString,
                        "playId": playId,
                        "playRateId": playRateId,
                        "rebatePackage": rebatePackage,
                        "stake": stake,
                        "unit": "DOLLAR"
                    }
                ],
                "txns": [

                ]
        }
        for draw in drawId:
            data['txns'].append(draw)

        r = self.s.post(url, headers=headers, json=data)
        log(f"Status code: {r.status_code}")

        return r.status_code

    def retrieved_draw(self, gameId, token, drawCount):
        url = self.sle.url_retrieved_draw(gameId)

        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'authorization': token,
            'origin': 'https://mx2.stgdevops.site',
            'referer': 'https://mx2.stgdevops.site/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 '
                          '(KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',

        }
        params = {
            'drawcount': drawCount
        }
        r = self.s.get(url, headers=headers, params=params)
        log(f"Retrieved draw: {r.json()}")

        return r.json()