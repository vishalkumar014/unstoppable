from django.utils import timezone
import math, random
import uuid


def generateToken(email):
    try:
        email_datetime =  str( email ) + str( timezone.now() )
        return str(uuid.uuid5(uuid.NAMESPACE_DNS,  email_datetime ))
    except Exception as e:
        return str(timezone.now())
    


def generateOTP():
    try:
        string = '01234567891011121314151617181920'
        OTP = ""
        length = len(string)
        for i in range(4):
            OTP += string[math.floor(random.random() * length)]
        return OTP
    except Exception as e:
        return '4546'