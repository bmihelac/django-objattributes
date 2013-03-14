from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class BaseAttribute(models.Model):

    class Meta:
        abstract = True

    def get_object_attribute(self, obj):
        """
        Returns existing object attribute or initialize new
        if it does not exits.
        """
        ObjectAttribute = self.objectattribute_set.model
        try:
            object_attribute = ObjectAttribute.objects.get(
                    content_type=ContentType.objects.get_for_model(obj),
                    object_id=obj.pk,
                    attribute=self)
        except ObjectAttribute.DoesNotExist:
            object_attribute = ObjectAttribute(obj=obj,
                    attribute=self)
        return object_attribute

    def set_value(self, obj, value):
        object_attribute = self.get_object_attribute(obj)
        object_attribute.set_value(value)
        object_attribute.save()

    def get_value(self, obj):
        object_attribute = self.get_object_attribute(obj)
        if not object_attribute:
            return None
        return object_attribute.get_value()


class BaseObjectAttribute(models.Model):
    """
    Maps objects and attributes.
    """
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    obj = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return str(self.value)

    class Meta:
        abstract = True

    def set_value(self, value):
        raise NotImplementedError

    def get_value(self):
        raise NotImplementedError
