# Create your models here.
from django.contrib.postgres.fields import JSONField
from django.db import models

# Create your models here.
class AGENT_DEF_LIST_INFO(models.Model):
    chat_id = models.CharField(max_length=50, blank=False, primary_key=True)
    biz_cate = models.CharField(max_length=10, blank=False)
    biz_sub_cate = models.CharField(max_length=10, blank=False)
    chat_title = models.CharField(max_length=100, blank=False)
    chat_desc = models.CharField(max_length=5000, blank=True, default='')
    use_flag = models.CharField(max_length=1, blank=True, default='')
    dir = models.CharField(max_length=200, blank=True, default='')
    config = models.CharField(max_length=1, blank=True, default='')
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(default=0)
    last_updated_by = models.IntegerField(default=0)

# response list here.
class AGENT_RESPONSE_LIST_INFO(models.Model):

class AGENT_MODEL_LIST_INFO(models.Model):

class AGENT_STORYBOARD_LIST_INFO(models.Model):

class AGENT_CORPUS_LIST_INFO(models.Model):
