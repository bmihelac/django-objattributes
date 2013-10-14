from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.contrib import admin
from django.conf import settings
from django.conf.urls import patterns, url
from django.template.response import TemplateResponse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import generic_inlineformset_factory
from django.forms.models import modelform_factory
from django.contrib import messages
from django.http import HttpResponseRedirect


from .forms import ObjectAttributeModelForm


class AttributeEditMixin(object):
    """
    Attribute edit mixin.

    ``edit_attributes_classes``
    """
    change_form_template = 'admin/objattributes/change_form.html'
    attribute_models = None
    edit_attributes_template = 'admin/objattributes/edit_attributes.html'

    def get_urls(self):
        urls = super(AttributeEditMixin, self).get_urls()
        info = (
                self.model._meta.app_label,
                self.model._meta.module_name,
                )
        my_urls = patterns('')
        for m in self.attribute_models:
            my_urls.append(url(
                    r'^(?P<object_id>\d+)/(?P<app_label>\w+)/(?P<model>\w+)/$',
                    self.admin_site.admin_view(self.edit_attributes),
                    name="%s_%s_edit_attributes" % info
                ))
        return my_urls + urls

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['attribute_models'] = []
        info = (
                self.model._meta.app_label,
                self.model._meta.module_name,
                )
        for m in self.attribute_models:
            url = reverse("admin:%s_%s_edit_attributes" % info,
                kwargs={
                    'object_id': object_id,
                    'app_label': m._meta.app_label,
                    'model': m._meta.module_name,
                    })
            title = _("Edit %(name)s") % {'name': m._meta.verbose_name_plural}
            extra_context['attribute_models'].append((title, url,))
        return super(AttributeEditMixin, self).change_view(
            request,
            object_id,
            form_url=form_url,
            extra_context=extra_context)

    def get_objattributes_form_class(self, object_attribute):
        """
        Override this method to use different ModelForm class.
        """
        return modelform_factory(type(object_attribute),
                form=ObjectAttributeModelForm,
                exclude=['content_type', 'object_id', 'attribute'])

    def get_attributes(self, attribute_model_class, obj):
        """
        Override this method to filter attributes or change order.
        """
        return attribute_model_class.objects.all()

    def get_attributes_edit_success_url(self, obj, object_attribute_model):
        """
        Override this method to return different URL to redirect
        user after edit_attributes is saved.
        """
        return reverse('admin:%s_%s_change' % (
                    self.model._meta.app_label,
                    self.model._meta.module_name,
                    ),
                    args=(obj.id,))

    def edit_attributes(self, request, object_id, app_label, model,
            *args, **kwargs):
        obj = self.get_object(request, object_id)

        object_attribute = ContentType.objects.get(app_label=app_label,
                model=model)
        object_attribute_model = object_attribute.model_class()
        assert object_attribute_model in self.attribute_models

        attribute_model_class = object_attribute_model.attribute.field.rel.to
        obj_attr_name = object_attribute_model._meta.verbose_name_plural

        data = request.POST if request.method == "POST" else None

        formset = []
        all_attributes = self.get_attributes(attribute_model_class, obj)
        for attribute in all_attributes:
            prefix = attribute.pk
            instance = attribute.get_object_attribute(obj)

            ObjectAttributeForm = self.get_objattributes_form_class(instance)

            form = ObjectAttributeForm(data,
                    prefix=prefix,
                    instance=instance)
            formset.append(form)

        if request.method == "POST":
            is_valid = True
            for form in formset:
                if not getattr(form, 'form_empty', False):
                    is_valid = is_valid and form.is_valid()

            if is_valid:
                for form in formset:
                    if getattr(form, 'form_empty', False):
                        if form.instance.pk:
                            form.instance.delete()
                    else:
                        form.save()

                message = _("%(name)s have been saved.") % {
                        'name': obj_attr_name}
                messages.add_message(request, messages.INFO, message)
                success_url = self.get_attributes_edit_success_url(obj,
                        object_attribute_model)
                return HttpResponseRedirect(success_url)

        title = _("Edit %(name)s") % {'name': obj_attr_name}
        context = {
            'original': obj,
            'opts': self.model._meta,
            'attribute_model_title': object_attribute_model._meta.verbose_name_plural,
            'title': title,
            'formset': formset,
            }
        return TemplateResponse(request, [self.edit_attributes_template],
                context, current_app=self.admin_site.name)
