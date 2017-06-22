from django.contrib.postgres.fields import JSONField
from django.db import models

# Create your models here.
class CB_DEF_LIST_INFO(models.Model):
    cb_id = models.CharField(max_length=50, blank=False, primary_key=True)
    chat_cate = models.CharField(max_length=10, blank=True)
    chat_sub_cate = models.CharField(max_length=10, blank=True)
    cb_title = models.CharField(max_length=100, blank=True)
    cb_desc = models.CharField(max_length=5000, blank=True)
    creation_date = models.DateTimeField(blank=True)
    last_update_date = models.DateTimeField(blank=True)
    created_by =  models.CharField(max_length=10, blank=True)
    last_updated_by = models.CharField(max_length=10, blank=True)

class CB_INTENT_LIST_INFO(models.Model):
    cb_id = models.ForeignKey(CB_DEF_LIST_INFO, on_delete=models.CASCADE)
    intent_id = models.CharField(max_length=10, blank=False)
    intent_type = models.CharField(max_length=10, blank=False) #model/custom
    intent_desc = models.CharField(max_length=50, blank=True)
    rule_value = JSONField() # custom case
    nn_type = models.CharField(max_length=10, blank=True)

class CB_STORYBOARD_LIST_INFO(models.Model):
    intent_id = models.ForeignKey(CB_INTENT_LIST_INFO, on_delete=models.CASCADE)
    story_id = models.CharField(max_length=10, blank=False, primary_key=True)
    story_desc = models.CharField(max_length=50, blank=True)

class CB_ENTITY_LIST_INFO(models.Model):
    cb_id = models.ForeignKey(CB_DEF_LIST_INFO, on_delete=models.CASCADE)
    intent_id = models.ForeignKey(CB_INTENT_LIST_INFO, on_delete=models.CASCADE)
    entity_type = models.CharField(max_length=10, blank=False)
    entity_list = JSONField()

class CB_MODEL_LIST_INFO(models.Model):
    cb_id = models.ForeignKey(CB_DEF_LIST_INFO, on_delete=models.CASCADE)
    nn_id = models.CharField(max_length=10, blank=True)
    nn_purpose = models.CharField(max_length=10, blank=True)
    nn_type = models.CharField(max_length=10, blank=True)
    nn_label_data = JSONField()
    nn_desc = models.CharField(max_length=50, blank=True)

class CB_SERVICE_LIST_INFO(models.Model):
    story_id = models.ForeignKey(CB_STORYBOARD_LIST_INFO, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=10, blank=True)
    service_name = models.CharField(max_length=10, blank=True)
    service_model = models.CharField(max_length=10, blank=True)
    service_url = models.CharField(max_length=100, blank=True)
    nn_id = models.CharField(max_length=10, blank=True)

class CB_RESPONSE_LIST_INFO(models.Model):
    story_id = models.ForeignKey(CB_STORYBOARD_LIST_INFO, on_delete=models.CASCADE)
    response_type = models.CharField(max_length=10, blank=True)
    output_entity = JSONField()
    output_data = models.CharField(max_length=50, blank=True)
    nn_id = models.CharField(max_length=10, blank=True)

class CB_TAGGING_INFO(models.Model):
    cb_id = models.ForeignKey(CB_DEF_LIST_INFO, on_delete=models.CASCADE)
    pos_type = models.CharField(max_length=10, blank=True)
    proper_noun = JSONField()
    parsed_length = models.IntegerField(default=10)

class CB_ONTOLOGY_INFO(models.Model):
    cb_id = models.ForeignKey(CB_DEF_LIST_INFO, on_delete=models.CASCADE)
    ontology_id = models.CharField(max_length=10, blank=True)
    ontology_desc = models.CharField(max_length=50, blank=True)