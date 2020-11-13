from base.base import Base, log
from config.url import UrlCms


class Cms(Base):

    def txn_reports(self, username='imwelly',
                    limit='25',
                    offset='0',
                    prize_cmp='get',
                    tm_end=None,
                    tm_mode='txntime',
                    tm_start=None):

        cms = UrlCms()
        url = cms.url_txn_reports()

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

            # 'tmEnd': '1605196799999',
            # 'tmStart': '1605110400000',

        }
        r = self.s.get(url, headers=headers, data=data)
        log.info(f'Response: {r.json()}')

        return r.status_code, r.json()