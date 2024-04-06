from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import *
from .models import *

# Create your views here.
@method_decorator(csrf_protect, name='dispatch')
class GetAllMusic(APIView):
    def get(self, request):
        try:
            querySets = Music.objects.all()
            serializer = MusicSerializer(querySets,many=True)
            data = {'code':status.HTTP_200_OK,'message':'success','data':serializer.data}
            return Response(data, status=status.HTTP_200_OK)    
        except Exception as e:
            data = {"code":status.HTTP_500_INTERNAL_SERVER_ERROR,'message':{str(e)},'data':[]}
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


# Create your views here.
@method_decorator(csrf_protect, name='dispatch')
class GetSingerMusic(APIView):
    def get(self, request):
        try:
            querySets = singer.objects.all()
            serializer = SingerSerializer(querySets,many=True)
            data = {'code':status.HTTP_200_OK,'message':'success','data':serializer.data}
            return Response(data, status=status.HTTP_200_OK)    
        except Exception as e:
            data = {"code":status.HTTP_500_INTERNAL_SERVER_ERROR,'message':{str(e)},'data':[]}
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)