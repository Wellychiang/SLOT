class UserInfo:

    def __init__(self, user):
        self.user = user

    cms_user_info = {'imwelly': {'username': 'imwelly',
                                 'pwd': '6e97679a803cee7c930f1bc8d5fa42a5098f901d'},
                     'wellyadmin': {'username': 'wellyadmin',
                                    'pwd': '64e89cab6f9b5560931d87399d916faf08e95c49'},
                     'welly2': {'username': 'welly2',
                                'pwd': '3578165f887bbdf37a15e1e62c919e7471c73d1b'}}

    def cms_username(self):
        return self.cms_user_info[self.user]['username']

    def cms_pwd(self):
        return self.cms_user_info[self.user]['pwd']

    """這邊是分隔線啦~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

    welly1 = 'welly1'
    welly2 = 'welly2'

    sle_user_info = {welly1: {'username': welly1,
                              'pwd': '21e7692cef417d7be81d44054f9b3c1bb5dc7f30'},
                     welly2: {'username': welly2,
                              'pwd': '8b433bc37805cf9420099c895bb1d32e5786ed1c'},
                     'welly11': {'username': 'welly11',
                                'pwd': '21e7692cef417d7be81d44054f9b3c1bb5dc7f30'},
                     'welly12': {'username': 'welly12',
                                'pwd': '21e7692cef417d7be81d44054f9b3c1bb5dc7f30'},
                     'welly13': {'username': 'welly13',
                                'pwd': '21e7692cef417d7be81d44054f9b3c1bb5dc7f30'},
                     'welly14': {'username': 'welly14',
                                'pwd': '21e7692cef417d7be81d44054f9b3c1bb5dc7f30'},
                     'welly15': {'username': 'welly15',
                                'pwd': '21e7692cef417d7be81d44054f9b3c1bb5dc7f30'},
                     'welly16': {'username': 'welly16',
                                'pwd': '21e7692cef417d7be81d44054f9b3c1bb5dc7f30'},
                     }

    def sle_username(self):
        return self.sle_user_info[self.user]['username']

    def sle_pwd(self):
        return self.sle_user_info[self.user]['pwd']
