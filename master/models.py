from django.db import models

# Create your models here.
class NN_DEF_LIST_INFO(models.Model):
    nn_id = models.CharField(max_length=50, blank=False, primary_key=True)
    biz_cate = models.CharField(max_length=10, blank=False)
    biz_sub_cate = models.CharField(max_length=10, blank=False)
    nn_title = models.CharField(max_length=100, blank=False)
    nn_desc = models.CharField(max_length=5000, blank=True, default='')
    use_flag = models.CharField(max_length=1, blank=True, default='')
    dir = models.CharField(max_length=200, blank=True, default='')
    config = models.CharField(max_length=1, blank=True, default='')
    created_by = models.CharField(max_length=50, blank=True, default='')
    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated_by = models.CharField(max_length=50, blank=True, default='')
    last_updated_date = models.DateTimeField(auto_now_add=True)

class NN_VER_WFLIST_INFO(models.Model):
    nn_wf_ver_id = models.CharField(max_length=50, blank=False, primary_key=True)
    nn_def_list_info_nn_id = models.CharField(max_length=50, blank=True, default='')
    nn_wf_ver_info = models.CharField(max_length=100, blank=False)
    condition = models.CharField(max_length=50, blank=True, default='')
    active_flag = models.CharField(max_length=1, blank=True, default='')
    nn_id = models.ForeignKey(NN_DEF_LIST_INFO, on_delete=models.CASCADE)
    created_by = models.CharField(max_length=50, blank=True, default='')
    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated_by = models.CharField(max_length=50, blank=True, default='')
    last_updated_date = models.DateTimeField(auto_now_add=True)