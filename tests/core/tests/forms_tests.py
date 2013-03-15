from django.test import TestCase
from django.forms.models import modelform_factory

from objattributes.forms import ObjectAttributeModelForm

from core.models import ObjectAttribute


class ObjectAttributeModelFormTest(TestCase):

    def setUp(self):
        self.form_class = modelform_factory(ObjectAttribute,
                    form=ObjectAttributeModelForm,
                    exclude=['content_type', 'object_id', 'attribute'])

    def test_form_empty(self):
        form = self.form_class()
        self.assertTrue(form.form_empty)

        form = self.form_class({'value': 'foo'})
        self.assertFalse(form.form_empty)

        form = self.form_class({'value': ''}, initial={'value': 'aa'})
        self.assertTrue(form.form_empty)
