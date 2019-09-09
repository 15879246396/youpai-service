# coding=utf-8
import datetime

import requests
from django.conf import settings
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_decode_handler
from rest_framework_jwt.settings import api_settings

from account.permissions import IsAuthenticatedWechat
from base.exceptions import LogicException, ValidateException
from account.models import MyUser
from common.decorator import common_api


class WechatLoginView(APIView):
    """
    微信登录逻辑
    """
    URL = 'https://api.weixin.qq.com/sns/jscode2session'

    @common_api
    def post(self, request):
        code = request.data.get("code")
        if not code:
            raise ValidateException().add_message('error:param', 'Incomplete Params!')

        params = {
            'appid': settings.WEAAPP_KEY,
            'secret': settings.WEAAPP_SECRET,
            'js_code': code,
            'grant_type': 'authorization_code',
        }
        data = requests.post(self.URL, data=params, timeout=600)
        json_data = data.json()
        openid = json_data.get('openid')
        if not openid:
            raise LogicException('error:error', 'Getting openid exceptions!')

        unionid = json_data.get('unionid')
        print(json_data)
        # 获取用户ip
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            user_ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            user_ip = request.META['REMOTE_ADDR']
        user, _created = MyUser.objects.get_or_create(
            openid=openid,
            defaults={
                'unionid': unionid,
                'provider': 'Wechat',
                'user_lastip': user_ip,
            }
        )

        user.last_login = datetime.datetime.today()
        if _created:
            # 首次授权登陆，注册，记录登陆ip
            user.set_password(openid)
            user.user_regip = user_ip
            user.save()
        else:
            user.user_lastip = user_ip
            user.save()

        # 手动签发jwt
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        result = {
            'data': {
                'openid': openid,
                'unionid': unionid,
                'nick_name': user.nick_name,
                'pic': user.pic,
                'user_status': user.is_active,
                'access_token': token,
            }
        }
        return Response(result)


class WechatUserInfoAPI(APIView):
    permission_classes = (IsAuthenticatedWechat,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    @common_api
    def get(self, request):
        user = request.auth
        # token = self.request.META['Authorization']
        # print(jwt_decode_handler(token))
        # toke_user = jwt_decode_handler(token) # auth

        # jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
        # user_dict = jwt_decode_handler(token)
        # user_id = user_dict['user_id']
        # # 获得user_id
        # user_id = toke_user.get("user_id")
        user = MyUser.objects.get(id=user.id)
        data = {
            "id": user.id,
            "nick_name": user.nick_name,
            "pic": user.pic,
            "real_name": user.real_name,
            "sex": user.sex,
            "email": user.email,
            "birth_date": user.birth_date,
            "user_mobile": user.user_mobile,
            "score": user.score,
        }
        return Response(data)

    @common_api
    def put(self, request):
        user_info = request.data.get('user_info')
        if not user_info:
            raise ValidateException().add_message('error:error', 'Incomplete Params!')
        user_id = request.auth.get('user_id')
        nick_name = user_info.get('nickName')
        pic = user_info.get('avatarUrl')
        sex = user_info.get('gender')
        MyUser.objects.filter(id=user_id).update(
            nick_name=nick_name,
            pic=pic,
            sex=sex,
        )
        return Response('success')
