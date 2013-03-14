from django.test import TestCase

from core.models import (
        Attribute,
        ObjectAttribute,
        Tshirt,
        )


class AttributeTest(TestCase):

    def setUp(self):
        self.tshirt = Tshirt.objects.create(name="my shirt")
        self.tshirt2 = Tshirt.objects.create(name="shirt 2")
        self.attribute_color = Attribute.objects.create(name="Color")

    def test_create_object_attribute(self):
        ObjectAttribute.objects.create(
                obj=self.tshirt,
                attribute=self.attribute_color,
                value="Blue")

    def test_create_object_attribute_through_attribute(self):
        self.attribute_color.set_value(self.tshirt, "Blue")
        objattribute = ObjectAttribute.objects.get(value="Blue")
        self.assertEqual(objattribute.obj, self.tshirt)

    def test_object_attributes(self):
        self.attribute_color.set_value(self.tshirt, "Blue")

        res = Tshirt.objects.filter(attributes__attribute__name="Color")
        self.assertIn(self.tshirt, res)
        self.assertNotIn(self.tshirt2, res)

        self.attribute_color.set_value(self.tshirt2, "Black")
        res = Tshirt.objects.filter(attributes__attribute__name="Color",
                attributes__value="Black")
        self.assertNotIn(self.tshirt, res)
        self.assertIn(self.tshirt2, res)
