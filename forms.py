from django import forms

class TaggedObjectForm(forms.Form):
    from portal.fields import TagField
    from portal.utils import get_tags # Function to get a list of tag object ({'id':1, 'name':'Tag1', ...}, {...}, ...)

    tags = get_tags()

    name = forms.CharField(label="Object name", widget=forms.TextInput(attrs={'autocomplete':'off'}))
    tags = TagField(label="Tags", choices=tags)

    def __init__(self, *args, **kwargs):
        """ This function is used to get user params from the view """
        from project.utils import get_tags
        from project.widgets import TagWidget

        self.fields['tags'].widget = TagWidget(attrs={'autocomplete':'off'}, datalist=get_tags())
        