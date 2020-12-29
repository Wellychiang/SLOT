import requests
from config.url import UrlCms, UrlSle
from config.userinfo import UserInfo
import logging
import time


log_path = 'log\log.log'
logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')

console_log = logging.StreamHandler()  # sys.stdout
logger.addHandler(console_log)

file_handler = logging.FileHandler(log_path)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

log = lambda x: logger.info(str(x).encode('cp950', 'replace').decode('cp950', 'ignore'))


class Base:

    s = requests.session()

    def __init__(self, env='stg'):
        self.env = env

    def cms_login(self, username='imwelly', vndorid='MX2'):

        cms = UrlCms()
        url = cms.url_login()

        user = UserInfo(username)
        userid = user.cms_username()
        pwd = user.cms_pwd()

        headers = {
            'accept': '*/*',
            'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'authorization': 'undefined',
            'content-length': '91',
            'content-type': 'application/json;charset=UTF-8',
            'origin': 'https://sle-bo.stgdevops.site',
            'referer': 'https://sle-bo.stgdevops.site/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 '
                          '(KHTML, like Gecko)'
                          ' Chrome/86.0.4240.193 Mobile Safari/537.36',
        }

        data = {
            'password': pwd,
            'userId': userid,
            'vendorId': vndorid,
        }

        r = self.s.post(url, headers=headers, json=data)
        log(f'Response: {r.json()}')
        return r.status_code, r.json()

    def sle_login(self, username='welly1'):

        sle = UrlSle()
        url = sle.url_login()

        user = UserInfo(username)
        loginname = user.sle_username()
        pwd = user.sle_pwd()

        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-length': '200',
            'content-type': 'application/json',
            'origin': 'https://mx2.stgdevops.site',
            'referer': 'https://mx2.stgdevops.site/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/86.0.4240.193 Mobile Safari/537.36',
        }

        data = {
            'captcha': '2222',
            'captchauuid': 'ef711bf9-ecbb-44cc-8419-def680a10ff3',
            'fingerprint': '64b185c6bdcd5bf3588b40b414063ee9',
            'loginname': loginname,
            'loginpassword': pwd,
        }

        r = self.s.post(url, headers=headers, json=data, verify=False)
        log(f'Response: {r.json()}')
        return r.status_code, r.json()

    # 轉換成可用的timestamp
    def start_and_end_time(self, start_m,
                                 start_d,
                                 end_m,
                                 end_d):
        strftimes = (time.strftime('%Y') + f'-{start_m}-{start_d} 00:00:00',
                     time.strftime('%Y') + f'-{end_m}-{end_d} 23:59:59')

        for strftime in strftimes:
            strptime = time.strptime(strftime, '%Y-%m-%d %H:%M:%S')
            if strftime == strftimes[0]:
                todays_start = time.mktime(strptime)
            else:
                todays_end = time.mktime(strptime)

        return str(int(todays_start))+'000', str(int(todays_end))+'999'


    def return_now_start_time(self):
        strftime = time.strftime('%Y-%m-%d %H:%M:%S')
        strptime = time.strptime(strftime, '%Y-%m-%d %H:%M:%S')
        now_start_time = time.mktime(strptime)

        return str(int(now_start_time)) + '000'
