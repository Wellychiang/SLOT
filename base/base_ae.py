from . import Base
from . import UrlAe
from . import log
import time


class Ae(Base):
    ae = UrlAe()

    def get_launch_token(self, username):

        url = self.ae.url_launch_game()
        _, get_token = self.ae_login(username)

        headers = {
            'Host': 'ae-api.stgdevops.site',
            'Connection': 'keep-alive',
            'Content-Length': '33',
            'Authorization': get_token['token'],
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/87.0.4280.88 Safari/537.36',
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept': '*/*',
            'Origin': 'https://ae.stgdevops.site',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://ae.stgdevops.site/',
            'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        }
        data = {
            "lang": "zh-CN",
            "platformtype": 2
        }
        r = self.s.put(url, headers=headers, json=data)
        log(f"Launch token: \n{r.json()}")
        time.sleep(1)


        return r.json()