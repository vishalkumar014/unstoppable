from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .functions import generateToken
from rest_framework import status
from .serializers import *


@method_decorator(ensure_csrf_cookie, name='dispatch')
class CSRFTokenAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        context={}
        context['message'] = 'CSRF Cookie Set'
        context['status']  =  True
        return Response(context, status=status.HTTP_200_OK)


@method_decorator(csrf_protect, name='dispatch')
class UserRegistrationView(APIView):
    def post(self, request):
        try:
            payLoad = request.data
            payLoad['first_name'] = "Guest"
            serializer = UserRegistrationSerializer(data=payLoad)
            if serializer.is_valid():
                user    = serializer.save(username=payLoad['email'])
                refresh = RefreshToken.for_user(user)
                data = {
                    'code':status.HTTP_200_OK,
                    'message':'success',
                    'data':{
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'info':{
                            'first_name':user.first_name,
                            'email':user.email,
                            'phone_number':user.phone_number,
                            'dob':user.dob,
                            'uuid':user.uuid,
                            'avatar':user.avatar.url if user.avatar else ""
                        },
                    },
                }
                return Response(data, status=status.HTTP_200_OK)
            data = {'code':status.HTTP_400_BAD_REQUEST,'message':'error','data':serializer.errors}
            return Response(data,status=status.HTTP_400_BAD_REQUEST)
        except:
            data = {'code':status.HTTP_500_INTERNAL_SERVER_ERROR,'message':'Something went wrong please try again','data':[]}
            return Response(data,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

@method_decorator(csrf_protect, name='dispatch')
class UserLoginView(TokenObtainPairView):
    def post(self, request):
        try:
            serializer = UserLoginSerializer(data=request.data)
            if serializer.is_valid():
                user  = serializer.validated_data.get('user')
                refresh = RefreshToken.for_user(user)
                data = {
                        'code':status.HTTP_200_OK,
                        'message':'success',
                        'data':{
                            'refresh': str(refresh),
                            'access': str(refresh.access_token),
                            'info':{
                                'first_name':user.first_name,
                                'email':user.email,
                                'phone_number':user.phone_number,
                                'dob':user.dob,
                                'uuid':user.uuid,
                                'avatar':user.avatar.url if user.avatar else ""
                            },
                        },
                    }
                return Response(data, status=status.HTTP_200_OK)
            data = {'code':status.HTTP_400_BAD_REQUEST,'message':'error','data':serializer.errors}
            return Response(data,status=status.HTTP_400_BAD_REQUEST)
        except:
            data = {'code':status.HTTP_500_INTERNAL_SERVER_ERROR,'message':'Something went wrong please try again','data':[]}
            return Response(data,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
        
@method_decorator(csrf_protect, name='dispatch')
class UserForgetAuthView(APIView):
    def post(self, request):
        try:
            payLoad = request.data
            serializer = UserForgetAuthSerializer(data=payLoad)
            if serializer.is_valid():
                user =  serializer.validated_data.get('user')
                user_ = user.first()
                otp     = generateToken.generateOTP()
                token   = generateToken.generateToken(user_.email)
                user.update(token=token,otp=otp)
                data = {'code':status.HTTP_200_OK,'data':{'token':token,"email":user_.email}}
                return Response(data, status=status.HTTP_200_OK)    
            data = {'code':status.HTTP_400_BAD_REQUEST,'message':'error','data':serializer.errors}
            return Response(data,status=status.HTTP_400_BAD_REQUEST)
        except:
            data = {"code":status.HTTP_500_INTERNAL_SERVER_ERROR,'message':'Something went wrong please try again','data':[]}
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

@method_decorator(csrf_protect, name='dispatch')
class UserTokenView(APIView):
    def post(self, request):
        try:
            payLoad = request.data
            serializer = UserTokenValidationSerializer(data=payLoad)
            if serializer.is_valid():
                user    =  serializer.validated_data.get('user')
                user_   = user.first()
                token   = generateToken.generateToken(user_.email)
                user.update(otp='',token=token)
                data = {'code':status.HTTP_200_OK,'message':'success','data':{'token':token}} 
                return Response(data, status=status.HTTP_200_OK) 
            data = {'code':status.HTTP_400_BAD_REQUEST,'message':'error','data':serializer.errors}   
            return Response(data,status=status.HTTP_400_BAD_REQUEST)
        except:
            data = {"code":status.HTTP_500_INTERNAL_SERVER_ERROR,'message':'Something went wrong please try again','data':[]}
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def get(self, request):
        try:
            payLoad     = request.GET
            serializer  = UserResendOtpSerializer(data=payLoad)
            if serializer.is_valid():
                user    =  serializer.validated_data.get('user')
                otp     = generateToken.generateOTP()
                user.update(otp=otp)
                data = {"code":status.HTTP_200_OK,"message":'success','data':[]}
                return Response(data, status=status.HTTP_200_OK)    
            data = {'code':status.HTTP_400_BAD_REQUEST,'message':'error','data':serializer.errors}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except:
            data = {"code":status.HTTP_500_INTERNAL_SERVER_ERROR,'message':'Something went wrong please try again','data':[]}
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_protect, name='dispatch')
class UserResetAuthView(APIView):
    def post(self, request):
        try:
            payLoad = request.data
            serializer = UserUpdatePasswordSerializer(data=payLoad)
            if serializer.is_valid():
                password_   = payLoad.get('password')
                user        = serializer.validated_data.get('user')
                password    = make_password(password_)
                user.update(password=password,token='')
                data = {'code':status.HTTP_200_OK,'message':'Your password is sucessfully updated','data':[]}
                return Response(data, status=status.HTTP_200_OK)    
            data = {'code':status.HTTP_400_BAD_REQUEST,'message':'error','data':serializer.errors}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except:
            data = {"code":status.HTTP_500_INTERNAL_SERVER_ERROR,'message':'Something went wrong please try again','data':[]}
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
