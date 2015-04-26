from django import forms
#from django_bootstrap_markdown.widgets import MarkdownInput
from django.utils.translation import ugettext_lazy as _
from qishi.models import Post
from bootstrap_markdown.widgets import MarkdownEditor

class NewPostForm(forms.ModelForm):
    subject = forms.CharField(
        label  = 'Subject', 
        widget = forms.TextInput(attrs={
            'size': '80', 
            'placeholder' : 'A title is required',
            'required':'required'})
    )
    message = forms.CharField(widget=MarkdownEditor(
        attrs={
            'id': 'content',
            'rows': '100',
            'height': 600,
        }),
        initial = """
Markdown Syntax - A Tutorial

Click the Preview button to see the formatted version.

This is a header
==========

This is a smaller header
----------

This is a paragraph.

To make another paragraph, add an empty line.

This is how you make "bold words".

This is an unordered list:

- List item A
- List item B

This is an ordered list:

1. List item A
2. List item B

To insert an image:

![sm](/static/qishi/logo.png)

![md](/static/qishi/logo.png)

![lg](/static/qishi/logo.png)

To include source code, add four spaces in the front:

    int main(int argc, char const * const * const argv) {
        // hello world!
    }

That's pretty much it. For full features of the markdown language (such as insert tables, etc.), please visit 
[Daring Fireball's website](http://daringfireball.net/projects/markdown/basics). ... Oops, and this is how 
you create a link.
"""
    )

    class Meta:
        model = Post
        fields = ('message', )


class ReplyPostForm(forms.ModelForm):
	message = forms.CharField(widget=MarkdownEditor(
        attrs = {
            'id': 'content',
        }))
	class Meta:
		model = Post
		fields = ('message', )

class QuickReplyPostForm(ReplyPostForm):
    message = forms.CharField(widget=MarkdownEditor(
        attrs = {
            'id': 'content',
        }))
    class Meta:
        model = Post
        fields = ('message', )
	
class EditPostForm(NewPostForm):
    def __init__(self, *args, **kwargs):
        super(EditPostForm, self).__init__(*args, **kwargs)
        self.initial['subject'] = self.instance.subject()
        self.initial['message'] = self.instance.message
        if not self.instance.topic_post:
            self.fields['subject'].required = False
        
    
