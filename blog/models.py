import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# Create your models here.

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class Person(AbstractUser):
    desc = models.TextField()
    avatar = models.ImageField(upload_to="avatars/", default='avatars/user.png')



class Blog(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    desc = models.TextField()
    imgage = models.ImageField(upload_to="blog/")
    
    sub_title = models.CharField(max_length=255, null=True, blank=True)
    sub_desc = models.TextField(null=True, blank=True)
    sub_imgage = models.ImageField(upload_to="blog/", null=True, blank=True)

    @property
    def comment_count(self):
        return self.comments.filter(parent__isnull=True).count()




class Comment(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    text = models.TextField()
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies")
    
    def __str__(self):
        return f"{self.user.username} - {self.blog.title}"