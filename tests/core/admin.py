from django.contrib import admin

from objattributes.admin import AttributeEditMixin

from .models import (
        ObjectAttribute,
        Attribute,
        Tshirt,
        AdvancedAttribute,
        AdvancedObjectAttribute,
        Book
        )


class TshirtAdmin(AttributeEditMixin, admin.ModelAdmin):
    attribute_models = [ObjectAttribute]


class BookAdmin(AttributeEditMixin, admin.ModelAdmin):
    attribute_models = [ObjectAttribute, AdvancedObjectAttribute]

    def get_objattributes_form_class(self, object_attribute):
        if isinstance(object_attribute, AdvancedObjectAttribute):
            from django.forms.models import modelform_factory
            from objattributes.forms import ObjectAttributeModelForm
            fields = object_attribute.get_editable_fields()
            return modelform_factory(type(object_attribute),
                    form=ObjectAttributeModelForm,
                    fields=fields)
        return super(BookAdmin, self).get_objattributes_form_class(
                object_attribute_model, attribute)

admin.site.register(Attribute)
admin.site.register(Tshirt, TshirtAdmin)
admin.site.register(AdvancedAttribute)
admin.site.register(Book, BookAdmin)
