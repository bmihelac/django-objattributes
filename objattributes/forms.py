from django.forms.models import ModelForm


class ObjectAttributeModelForm(ModelForm):
    """
    Default ModelForm for editing object attribute.

    ``form_empty`` allows removing object attribute instance
    if all fields are empty.
    """

    @property
    def form_empty(self):
        """
        Returns ``True`` if all fields data is empty.
        """
        for name, field in self.fields.items():
            value = field.widget.value_from_datadict(self.data, self.files, self.add_prefix(name))
            if value:
                return False
        return True
