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


ATTRIBUTE_CHOICES = (
        ('string', 'String'),
        ('number', 'Integer'),
        ('boolean', 'Boolean'),
        )


class AdvancedAttribute(BaseAttribute):
    name = models.CharField(_('Name'), max_length=250)
    description = models.CharField(_('Description'), max_length=100, blank=True)
    type = models.CharField(_('Type'), choices=ATTRIBUTE_CHOICES, max_length=30)
    ordering = models.IntegerField(_('Ordering'), default=0)

    class Meta:
        verbose_name = _('AdvancedAttribute')
        verbose_name_plural = _('AdvancedAttributes')
        ordering = []

    def __unicode__(self):
        return self.name


class AdvancedObjectAttribute(BaseObjectAttribute):
    attribute = models.ForeignKey(AdvancedAttribute,
            verbose_name=_('Attribute'),
            related_name="object_attributes")
    string_value = models.CharField(_('String'), max_length=250, blank=True,
            null=True)
    number_value = models.DecimalField(_('Number'), decimal_places=4,
            max_digits=10, blank=True, null=True)
    boolean_value = models.NullBooleanField('Boolean value', blank=True,
            null=True)

    def get_field_name_for_attribute(self):
        return "%s_value" % self.attribute.type

    def get_editable_fields(self):
        return [self.get_field_name_for_attribute()]

    def set_value(self, value):
        setattr(self, self.get_field_name_for_attribute(), value)

    def get_value(self):
        getattr(self, self.get_field_name_for_attribute())


class Book(models.Model):
    name = models.CharField(max_length=100)
    attributes = GenericRelation(AdvancedObjectAttribute)

    def __unicode__(self):
        return self.name
