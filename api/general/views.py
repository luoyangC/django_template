from rest_framework.generics import GenericAPIView
from rest_framework_jwt.views import JSONWebTokenAPIView

from api.general.serializers import SMSCodeSerializer, CustomTokenSerializer
from custom.exception import CustomException
from custom.response import JsonResponse
from utils.ali_sms import send_sms


class SMSCodeAPIView(GenericAPIView):
    """
    发送短信验证码
    """
    permission_classes = ()
    authentication_classes = ()
    serializer_class = SMSCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data['mobile']
        send_type = serializer.validated_data['type']
        res = send_sms(mobile, send_type)
        if res['code'] != 'OK':
            raise CustomException(code=4103, message=res['message'])
        return JsonResponse(message='短信发送成功')


class CustomTokenAPIView(JSONWebTokenAPIView):
    """
    获取token
    """
    permission_classes = ()
    authentication_classes = ()
    serializer_class = CustomTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.get('user') or request.user
        token = serializer.validated_data.get('token')
        return JsonResponse({'user': user, 'token': token})


send_sms_code = SMSCodeAPIView.as_view()
custom_token = CustomTokenAPIView.as_view()
