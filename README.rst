====================
django-objattributes
====================

django-objattributes provides abstract models and admin mixins to make easier defining various attributes and storing attribute values for
objects.

.. figure:: https://raw.github.com/bmihelac/django-objattributes/master/docs/_static/objattributes-1.png

   Example 1. - Test application. Each attribute can be of String, Number or Boolean type.
   Attributes are defined in administration.

Getting started
---------------

Define Attribute and ObjectAttribute that will store text values::

    from objattributes.models import BaseAttribute, BaseObjectAttribute

    # define model that will handle attributes
    class Attribute(BaseAttribute):
        name = models.CharField(_('Name'), max_length=250)

    # define model that will handle attributes values for object
    class ObjectAttribute(BaseObjectAttribute):
        attribute = models.ForeignKey(Attribute,
                verbose_name=_('Attribute'),
                related_name="object_attributes")
        value = models.TextField(_('Value'), max_length=250)

        def set_value(self, value):
            self.value = value

        def get_value(self):
            return self.value

Use ``AttributeEditMixin`` to add attribute editing to administration::

    from objattributes.admin import AttributeEditMixin

    class TshirtAdmin(AttributeEditMixin, admin.Model  Admin):
        attribute_models = [ObjectAttribute]

For other examples check test appplication.

TODO:
-----

* translations 
