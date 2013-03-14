from django.contrib import admin

from objattributes.admin import AttributeEditMixin

from .models import (
        ObjectAttribute,
        Attribute,
        Tshirt,
        )


class TshirtAdmin(AttributeEditMixin, admin.ModelAdmin):
    attribute_models = [ObjectAttribute]


admin.site.register(Attribute)
admin.site.register(Tshirt, TshirtAdmin)
