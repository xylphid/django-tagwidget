from django import forms
from django.forms import fields
from portal.widgets import TagWidget

class TagField(fields.MultiValueField):
    widget = TagWidget

    def __init__(self, *args, **kwargs):
        """
        Have to pass a list of field types to the constructor, else we
        won't get any data to our compress method.
        """
        choices = kwargs.pop("choices",[])
        all_fields = (
            fields.MultipleChoiceField(choices=choices),
            fields.CharField(required=False)
            )
        super(TagField, self).__init__(all_fields, require_all_fields=False, *args, **kwargs)

    def compress(self, data_list):
        """
        Takes the values from the MultiWidget and passes them as a
        list to this function. This function needs to compress the
        list into a single object to save.
        """
        if data_list:
            if not data_list[0]:
                raise forms.ValidationError("Field is missing data.")

            return data_list[0]
        return None