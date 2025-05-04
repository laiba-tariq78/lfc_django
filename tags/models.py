from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.

class TagItemManager(models.Manager):
    def get_tags_for(self, obj_type, obj_id):
        """Get all tags for a given object type and id"""
        content_type = ContentType.objects.get_for_model(obj_type)
        return TagItem.objects.filter(content_type=content_type, object_id=obj_id).select_related('tag')

class Tag(models.Model):
    label = models.CharField(max_length=255)

class TagItem(models.Model):
    objects = TagItemManager()
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    #type (product, video etc), id
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()  #generic foreign key to refer to any model

