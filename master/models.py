from django.contrib.postgres.fields import JSONField
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
    automl_parms = JSONField()
    automl_runtime = JSONField()
    automl_stat = JSONField()
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(default=0)
    last_updated_by = models.IntegerField(default=0)

class NN_DEF_LIST_ID_INFO(models.Model):
    nn_id = models.ForeignKey(NN_DEF_LIST_INFO, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(default=0)
    last_updated_by = models.IntegerField(default=0)

class NN_VER_WFLIST_INFO(models.Model):
    class Meta:
        unique_together = (('nn_id', 'nn_wf_ver_id'),)
    nn_wf_ver_id = models.IntegerField(default=1)
    nn_def_list_info_nn_id = models.CharField(max_length=50, blank=True, default='')
    automl_gen = models.CharField(max_length=10, blank=True, default='')
    nn_wf_ver_info = models.CharField(max_length=100, blank=False)
    condition = models.CharField(max_length=50, blank=True, default='')
    active_flag = models.CharField(max_length=1, blank=True, default='')
    nn_wf_ver_desc = models.CharField(max_length=5000, blank=True)
    nn_id = models.ForeignKey(NN_DEF_LIST_INFO, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(default=0)
    last_updated_by = models.IntegerField(default=0)

class NN_VER_BATCHLIST_INFO(models.Model):
    nn_batch_ver_id = models.CharField(max_length=50, blank=False, primary_key=True)
    nn_ver_wflist_info_nn_ver = models.CharField(max_length=50, blank=False)
    nn_batch_ver_info = models.CharField(max_length=50, blank=True, default='')
    active_flag = models.CharField(max_length=1, blank=False, default='Y')
    train_flag = models.CharField(max_length=1, blank=False, default='N')
    eval_flag = models.CharField(max_length=1, blank=False, default='Y')
    nn_wf_ver_id = models.ForeignKey(NN_VER_WFLIST_INFO, on_delete=models.CASCADE)
    job_end_time = models.DateTimeField(null=True)
    model_acc = models.IntegerField(default=0)
    train_progress = models.IntegerField(default=0)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(default=0)
    last_updated_by = models.IntegerField(default=0)

class TRAIN_SUMMARY_RESULT_INFO(models.Model):
    nn_id = models.CharField(max_length=50, blank=False)
    nn_wf_ver_id = models.CharField(max_length=50, blank=False)
    nn_batch_ver_id = models.ForeignKey(NN_VER_BATCHLIST_INFO, on_delete=models.CASCADE)
    result_info = JSONField()
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(default=0)
    last_updated_by = models.IntegerField(default=0)

class TRAIN_SUMMARY_ACCLOSS_INFO(models.Model):
    nn_id = models.CharField(max_length=50, blank=False)
    nn_wf_ver_id = models.CharField(max_length=50, blank=False)
    nn_batch_ver_id = models.ForeignKey(NN_VER_BATCHLIST_INFO, on_delete=models.CASCADE)
    acc_info = JSONField()
    loss_info = JSONField()
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(default=0)
    last_updated_by = models.IntegerField(default=0)

class BATCH_INFO_JOBCONFIG(models.Model):
    nn_id = models.CharField(max_length=50, blank=False, primary_key=True)
    nn_wf_ver_id = models.CharField(max_length=50, blank=False)
    nn_batch_ver_id = models.ForeignKey(NN_VER_BATCHLIST_INFO, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    period = models.IntegerField()
    type = models.CharField(max_length=1, blank=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(default=0)
    last_updated_by = models.IntegerField(default=0)

class NN_WF_STATE_INFO(models.Model):
    wf_state_id = models.CharField(max_length=50, blank=False, primary_key=True)
    nn_id = models.CharField(max_length=50, blank=False)
    nn_wf_ver_id = models.ForeignKey(NN_VER_WFLIST_INFO, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(default=0)
    last_updated_by = models.IntegerField(default=0)

class NN_WF_EASY_MODE_RULE(models.Model):
    key = models.IntegerField(primary_key=True)
    easy_mode_purp = models.CharField(max_length=2, blank=False)
    easy_mode_data_type = models.CharField(max_length=2, blank=False)
    easy_mode_store_type = models.CharField(max_length=2, blank=False)
    wf_state_id = models.ForeignKey(NN_WF_STATE_INFO, on_delete=models.CASCADE)
    easy_mode_data_size = models.CharField(max_length=2, blank=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(default=0)
    last_updated_by = models.IntegerField(default=0)

class NN_WF_NODE_RELATION(models.Model):
    class Meta:
        unique_together = (('nn_wf_node_id_1', 'nn_wf_node_id_2'),)
    nn_wf_node_id_1 = models.CharField(max_length=50, blank= False)
    nn_wf_node_id_2 = models.CharField(max_length=50, blank= False)
    wf_state_id = models.ForeignKey(NN_WF_STATE_INFO, on_delete=models.CASCADE)
    nn_wf_relation_id = models.AutoField(primary_key=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(default=0)
    last_updated_by = models.IntegerField(default=0)

class WF_TASK_MENU_RULE(models.Model):
    wf_task_menu_id = models.CharField(max_length=50, blank=False, primary_key=True)
    wf_task_menu_name = models.CharField(max_length=50, blank=True)
    wf_task_menu_desc = models.CharField(max_length=50, blank=True)
    visible_flag = models.BooleanField
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(default=0)
    last_updated_by = models.IntegerField(default=0)

class WF_TASK_SUBMENU_RULE(models.Model):
    wf_task_menu_id = models.ForeignKey(WF_TASK_MENU_RULE,on_delete=models.CASCADE)
    wf_task_submenu_id = models.CharField(max_length=50, blank=False, primary_key=True)
    wf_task_submenu_name = models.CharField(max_length=100, blank=True)
    wf_task_submenu_desc = models.CharField(max_length=200, blank=True)
    wf_node_class_path = models.CharField(max_length=200)
    wf_node_class_name = models.CharField(max_length=200)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(default=0)
    last_updated_by = models.IntegerField(default=0)

class NN_WF_NODE_INFO(models.Model):
    nn_wf_node_id = models.CharField(max_length=50, blank=False, primary_key=True)
    nn_wf_node_name = models.CharField(max_length=50, blank= False)
    wf_state_id = models.ForeignKey(NN_WF_STATE_INFO, on_delete=models.CASCADE)
    wf_task_submenu_id = models.ForeignKey(WF_TASK_SUBMENU_RULE, on_delete=models.CASCADE)
    wf_node_status = models.IntegerField()
    node_config_data = JSONField()
    node_draw_x = models.IntegerField()
    node_draw_y = models.IntegerField()
    nn_wf_node_desc = models.CharField(max_length=250, blank=True)
    task_fin_flag = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(default=0)
    last_updated_by = models.IntegerField(default=0)

class WF_TASK_REALATION_RULE(models.Model):
    key = models.IntegerField(primary_key=True)
    wf_task_submenu_id_1 = models.CharField(max_length=10, blank=False)
    wf_task_submenu_id_2 = models.CharField(max_length=10, blank=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(default=0)
    last_updated_by = models.IntegerField(default=0)

class AUTO_ML_RULE(models.Model):
    graph_flow_id = models.CharField(max_length=20, blank=False, primary_key=True)
    graph_flow_data = JSONField()
    graph_flow_desc = models.CharField(max_length=5000, blank=True)
    graph_flow_group_id = models.CharField(max_length=100)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(default=0)
    last_updated_by = models.IntegerField(default=0)
    train_file_path = models.CharField(max_length=100, blank=True)
    eval_file_path = models.CharField(max_length=100, blank=True)
