# -*- coding: utf8 -*-
from rest_framework.request import Request
from rest_framework.exceptions import AuthenticationFailed

class MyRequest(Request):
    def _authenticate(self):
        """
        重载基类的_authenticate
        访问request.user时会调用此方法
        在view层对该请求进行权限验证
        """
        # 这里使用self._request.user，如果使用self.request.user会造成递归调用
        if self.path in ('/Blog/', '/Blog/login/'):
            return

        if self._request.user in (None, ''):
            return
            #raise AuthenticationFailed('Please login first')

        # 授权
        self.user = self._request.user
        # print self.path, self._request.user.name, '-> valid'