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
    clsreport01 = 'clsreport01'
    clsreport02 = 'clsreport02'
    clsreport03 = 'clsreport03'
    clsreport04 = 'clsreport04'
    clsreport05 = 'clsreport05'
    clsreport06 = 'clsreport06'
    spreport01 = 'spreport01'
    spreport02 = 'spreport02'
    spreport03 = 'spreport03'


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
                     clsreport01: {'username': clsreport01,
                                   'pwd': '55234cbc1b3c6f7a076b9b0bba8fd9e3150e3ae7'},
                     clsreport02: {'username': clsreport02,
                                   'pwd': 'b784bbd85c2e8682aef64e23514ba2cef5f21314'},
                     clsreport03: {'username': clsreport03,
                                   'pwd': 'ee507b6bf3151e3d86ea109fe83b23b548ff789c'},
                     clsreport04: {'username': clsreport04,
                                   'pwd': '8068a7ec5d3dd8a9bfe17885610b6b45489d838c'},
                     clsreport05: {'username': clsreport05,
                                   'pwd': '679677c297f5bd9355e79ff86a736761103e56df'},
                     clsreport06: {'username': clsreport06,
                                   'pwd': 'a8c2029ed8feb5cfcc60386127d32f7e73a25a72'},
                     spreport01: {'username': spreport01,
                                  'pwd': 'c2f4bc4830c2ec293eda61fddbabb9dd3ba478aa'},
                     spreport02: {'username': spreport02,
                                  'pwd': 'f9bc7df343501139d9b383d786498763e9c7b23d'},
                     spreport03: {'username': spreport03,
                                  'pwd': 'aee05fb17e1377e6b05ff24ca2bd636a6b736907'}
                     }

    def sle_username(self):
        return self.sle_user_info[self.user]['username']

    def sle_pwd(self):
        return self.sle_user_info[self.user]['pwd']
