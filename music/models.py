from django.db import models
from account.models import User
import json
import uuid


class Common(models.Model):
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    is_activate = models.BooleanField(default=True)
    class Meta:
        abstract = True

class Music(Common):
    title   = models.CharField(max_length=50,null=True,blank=True)
    content = models.TextField(null=True,blank=True)
    details  = models.TextField(null=True,blank=True)
    duration = models.CharField(max_length=50,null=True,blank=True)
    type    = models.CharField(max_length=50,null=True,blank=True)
    label   = models.CharField(max_length=50,null=True,blank=True)
    cover   = models.ImageField(upload_to='cover/',null=True,blank=True)
    avatar  = models.ImageField(upload_to='avatar/',null=True,blank=True)
    music   = models.FileField(upload_to='music/',null=True,blank=True)
    video   = models.FileField(upload_to='video/',null=True,blank=True)
    uuid    = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tags    = models.TextField(null=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)

    def set_tags(self, x):
        self.tags = json.dumps(x)

    def get_tags(self):
        return json.loads(self.tags)
    
    def set_details(self, x):
        self.details = json.dumps(x)

    def get_details(self):
        return json.loads(self.details)
    
class singer(Common):
    name    = models.CharField(max_length=50,null=True,blank=True)
    dob     = models.CharField(max_length=20,null=True,blank=True)
    details = models.TextField(null=True,blank=True)
    social  = models.TextField(null=True,blank=True)
    avatar  = models.ImageField(upload_to='singer_avatar/',null=True,blank=True)
    music   = models.ManyToManyField(Music,related_name='singer_music')
    uuid    = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tags    = models.TextField(null=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)

    def set_tags(self, x):
        self.tags = json.dumps(x)

    def get_tags(self):
        return json.loads(self.tags)
    
    def set_social(self, x):
        self.social = json.dumps(x)

    def get_social(self):
        return json.loads(self.social)

class PlayList(Common):
    user    = models.ForeignKey(User, related_name='playlist_user',on_delete=models.CASCADE)
    music   = models.ManyToManyField(Music,related_name='playlist_music')
    title   = models.CharField(max_length=100,null=True,blank=True)
    content = models.TextField(null=True,blank=True)
    cover   = models.ImageField(upload_to='playlist_cover/',null=True,blank=True)
    uuid    = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tags    = models.TextField(null=True,blank=True)
    play_count = models.IntegerField(null=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)

    def set_tags(self, x):
        self.tags = json.dumps(x)

    def get_tags(self):
        return json.loads(self.tags)