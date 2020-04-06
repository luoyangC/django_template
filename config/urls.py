from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from api.general.views import send_sms_code
from api.general.views import custom_token
from api.user import views as user_views

router = DefaultRouter()

router.register('user', user_views.UserViewSet, basename='user')


schema_view = get_schema_view(
   openapi.Info(
      title="Island API 文档",
      default_version='v1',
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # 后台管理
    path('admin/', admin.site.urls),
    # 文档功能
    path('swagger/', schema_view.with_ui('swagger'), name='swagger文档'),
    # 获取授权
    path('api/<str:version>/token/', custom_token),
    # 发送短信验证码
    path('api/<str:version>/code/', send_sms_code),
    # 获取当前用户信息
    path('api/<str:version>/user/info/', user_views.UserInfoAPIView.as_view()),
    # API入口
    path('api/<str:version>/', include(router.urls)),
]


