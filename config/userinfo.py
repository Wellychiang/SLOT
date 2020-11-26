class UserInfo:

    def __init__(self, user):
        self.user = user

    cms_user_info = {'imwelly':     {'username': 'imwelly',
                                     'pwd': '6e97679a803cee7c930f1bc8d5fa42a5098f901d'},
                     'wellyadmin':  {'username': 'wellyadmin',
                                     'pwd': '64e89cab6f9b5560931d87399d916faf08e95c49'},
                     'welly2':      {'username': 'welly2',
                                     'pwd': '3578165f887bbdf37a15e1e62c919e7471c73d1b'}}

    def cms_username(self):
        return self.cms_user_info[self.user]['username']

    def cms_pwd(self):
        return self.cms_user_info[self.user]['pwd']

    """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

    welly1 = 'welly1'
    welly2 = 'welly2'
    yahoo = 'yahoo'
    autowelly001 = 'autowelly001'
    autowelly002 = 'autowelly002'
    autowelly003 = 'autowelly003'
    autowelly004 = 'autowelly004'

    sle_user_info = {welly1:        {'username': welly1,
                                     'pwd': '21e7692cef417d7be81d44054f9b3c1bb5dc7f30'},
                     welly2:        {'username': welly2,
                                     'pwd': '8b433bc37805cf9420099c895bb1d32e5786ed1c'},
                     yahoo:         {'username': yahoo,
                                     'pwd': 'f6f49e30f8af1f5136c1b0feaec03d95145d1a3f'},
                     autowelly001:  {'username': autowelly001,
                                     'pwd': 'd9f499dd02d95bd1fa180de9fb2096ced67749a2'},
                     autowelly002:  {'username': autowelly002,
                                     'pwd': '0e26c94bc5971ba81f9065c7112acbd387b346dc'},
                     autowelly003:  {'username': autowelly003,
                                     'pwd': '0c23de608f7b9e9096fe2def1c8c8d2dfd6b4603'},
                     autowelly004:  {'username': autowelly004,
                                     'pwd': '59bcde24bf38a52ab665ca013d6d82c85f6dd977'},
                     'welly16': {'username': 'welly16',
                                'pwd': '21e7692cef417d7be81d44054f9b3c1bb5dc7f30'},
                     }

    def sle_username(self):
        return self.sle_user_info[self.user]['username']

    def sle_pwd(self):
        return self.sle_user_info[self.user]['pwd']
