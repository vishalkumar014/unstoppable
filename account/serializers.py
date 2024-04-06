from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import make_password,check_password
from .models import *


class UserRegistrationSerializer(serializers.ModelSerializer):
    def validate_email(self, value):
        ModelClass = self.Meta.model
        if ModelClass.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email is already exists')
        return value
    
    def validate_phone_number(self, value):
        ModelClass = self.Meta.model
        if ModelClass.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError('Phone number is already exists')
        return value
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            'email':        {'required': True},
            'password':     {'required': True},
            'phone_number': {'required': False},
            'username': {
                'required': False,
                'validators': []
            }
        }


class UserLoginSerializer(serializers.Serializer):
    email       = serializers.EmailField(required=True)
    password    = serializers.CharField(required=True)
    
    class Meta:
        model = User
        fields = "__all__"

    def validate(self, data):
        email       = data.get('email')
        password    = data.get('password')
        if email and password:
            ModelClass = self.Meta.model
            userObj = ModelClass.objects.filter(email=email)
            if not userObj.exists():
                raise serializers.ValidationError('Invalid credentials')
            
            savedPasswordHash = userObj.first().password
            if not check_password(password,savedPasswordHash):
                raise serializers.ValidationError('Invalid credentials')
            
            data['user'] = userObj.first()
        else:
            raise serializers.ValidationError('Must include "email" and "password"')
        return data


class UserEditProfileSerializer(serializers.ModelSerializer):
    email           = serializers.EmailField(required=False)
    first_name      = serializers.CharField(required=False)
    phone_number    = serializers.CharField(required=False)
    class Meta:
        model = User
        fields = "__all__" 
        extra_kwargs = {
            'username': {
                'validators': []
            }
        }


class UserForgetAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email"]
        extra_kwargs = {
            'email': {'required': True},
            'username': {
                'validators': []
            }
        }

    def validate(self, data):
        email = data.get('email')
        if email:
            ModelClass  = self.Meta.model
            userObj     = ModelClass.objects.filter(email=email)
            if not userObj.exists():
                raise serializers.ValidationError({'email':'Invalid credentials'})
            
            data['user'] = userObj
        else:
            raise serializers.ValidationError({"email":'Must include email'})
        return data


class UserTokenValidationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["token","otp"]
        extra_kwargs = {
            'token': {'required': False},
            'otp': {'required': False},
        }
    def validate(self, data):
        token = data.get('token')
        otp   = data.get('otp')
        if token and otp:
            ModelClass  = self.Meta.model
            userObj     = ModelClass.objects.filter(token=token,otp=otp)
            if not userObj.exists():
                raise serializers.ValidationError('Otp is invalid or expired')
            data['user'] = userObj
        else:
            raise serializers.ValidationError('Otp is invalid or expired')
        return data


class UserResendOtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["token"]
        extra_kwargs = {
            'token' : {'required': True},
        }
        
    def validate(self, data):
        token       = data.get('token')
        if token:
            ModelClass  = self.Meta.model
            userObj     = ModelClass.objects.filter(token=token)
            if not userObj.exists():
                raise serializers.ValidationError('Session is expired.')
            data['user'] = userObj
        else:
            raise serializers.ValidationError('Session is expired.')
        return data
    

class UserUpdatePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["token","password"]
        extra_kwargs = {
            'password'  : {'required': True},
            'token'     : {'required': True},
            'username': {
                'validators': []
            }
        }
    def validate(self, data):
        token       = data.get('token')
        if token:
            ModelClass  = self.Meta.model
            userObj     = ModelClass.objects.filter(token=token)
            if not userObj.exists():
                raise serializers.ValidationError({'session':'Session is expired'})
            data['user'] = userObj
        else:
            raise serializers.ValidationError({'session':'Session is expired'})
        return data


class SocialAuthSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            'email': {'required': True},
            'username': {
                'validators': []
            }
        }