from .views import (UserRegistrationView,CSRFTokenAPIView,UserLoginView,UserForgetAuthView,UserTokenView,UserResetAuthView)
from rest_framework_simplejwt.views import TokenRefreshView
# from rest_framework.schemas import get_schema_view
from django.urls import path
# from django.views.generic import TemplateView


urlpatterns = [
    path('token/', CSRFTokenAPIView.as_view()),
    path('signup/', UserRegistrationView.as_view()),
    path('signin/', UserLoginView.as_view()),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('forgot/', UserForgetAuthView.as_view(), name='forgot_auth'),
    path('token-validate/', UserTokenView.as_view(), name='token_validate'),
    path('reset-auth/', UserResetAuthView.as_view(), name='update_auth'),
    # path("api_schema",get_schema_view(title="Auth API", description="API for all things…", version="1.0.0"),name="api_schema",),
    # path('swagger-ui/', TemplateView.as_view(template_name='docs.html',extra_context={'schema_url':'api_schema'}), name='swagger-ui'),
]