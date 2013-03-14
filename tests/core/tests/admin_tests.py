from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User


from core.models import (
        Tshirt,
        ObjectAttribute,
        Attribute,
        )


class AdminIntegrationTest(TestCase):

    def setUp(self):
        user = User.objects.create_user('admin', 'admin@example.com',
                'password')
        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.client.login(username='admin', password='password')

        self.tshirt = Tshirt.objects.create(name="Tshirt")
        self.attribute = Attribute.objects.create(name="Color")

    def test_change_form(self):
        url = reverse("admin:core_tshirt_change", args=(self.tshirt.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                'admin/objattributes/change_form.html')
        self.assertContains(response,
                _('Edit %(title)s') % {
                    'title': ObjectAttribute._meta.verbose_name_plural
                    })

    def test_edit_attributes(self):
        url = reverse("admin:core_tshirt_edit_attributes", kwargs={
            'object_id': self.tshirt.pk, 
            'app_label': 'core',
            'model': 'objectattribute',
            })
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        prefix = self.attribute.pk
        data = {
                '%s-value' % prefix: "blue",
                }
        response = self.client.post(url, data)
        self.assertRedirects(response,
                reverse("admin:core_tshirt_change", args=(self.tshirt.pk,)))

        self.assertEqual(self.attribute.get_value(self.tshirt), "blue")
