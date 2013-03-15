from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.contenttypes.generic import GenericRelation

from objattributes.models import BaseAttribute, BaseObjectAttribute


class Attribute(BaseAttribute):
    name = models.CharField(_('Name'), max_length=250)

    def __unicode__(self):
        return self.name


class ObjectAttribute(BaseObjectAttribute):
    attribute = models.ForeignKey(Attribute,
            verbose_name=_('Attribute'),
            related_name="object_attributes")
    value = models.TextField(_('Value'), max_length=250)

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value


class Tshirt(models.Model):
    name = models.CharField(max_length=100)
    attributes = GenericRelation(ObjectAttribute)
