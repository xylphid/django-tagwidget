from django.forms.widgets import MultiWidget, MultipleHiddenInput, TextInput

class TagWidget(MultiWidget):
    
    def __init__(self, attrs=None, datalist=None):
        self.rawlist = datalist
        self.list_id = 'xy-' + self._generate_id()
        text_attrs = attrs or {}
        hidden_attrs = attrs or {}

        if datalist:
            text_attrs['list'] = self.list_id

        widgets = (
            MultipleHiddenInput(attrs=hidden_attrs),
            TextInput(attrs=text_attrs))
        super(TagWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        """ Decompress values """
        if value:
            return value, None
        else:
            return None, None

    def format_output(self, rendered_widgets):
        """
        Given a list of rendered widgets (as strings), it is structured in
        HTML code you may change to fit your needs.
        Here, meridian is not rendered.
        
        Returns a Unicode string representing the HTML for the whole lot.
        """

        import re
        p = re.compile(r'<input .*>')
        tags = []
        selected = []
        for input in p.findall(rendered_widgets[0]):
            # Extract tag id
            q = re.compile('value="(\d+)"')
            m = q.search(input)

            # Define selected option and update rendered widget
            selected.append(m.group(1))
            tags.append( 
                    '<div class="tag">%s%s</div>' % 
                    ( input, next((x['name'] for x in self.rawlist if x['id'] == m.group(1)), None) ) 
                )

        return """
            <div class="xylphid-tags">
                %s
                %s
                %s
            </div>
            %s
        """ % (self.render_datalist(selected), ''.join(tags), rendered_widgets[1], self.media)

    def render_datalist(self, selected):
        options = []
        for item in self.rawlist:
            if item['id'] not in selected:
                options.append('<option value="%s" data-id="%s" />' % (item['name'], item['id']))

        return """
            <datalist id="%s">
                %s
            </datalist>
        """ % (self.list_id, ''.join(options))

    def _generate_id(self):
        import uuid

        return str(uuid.uuid4())

    class Media:
        css = {
            'screen':('portal/css/widget.xylphid-tags.css',)
            }
        js = (
            'portal/js/widget.xylphid-tags.js',
            )