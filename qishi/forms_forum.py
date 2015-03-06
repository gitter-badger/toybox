from django import forms
from django_bootstrap_markdown.widgets import MarkdownInput

from qishi.models import Post

class NewPostForm(forms.ModelForm):
    message = forms.CharField(widget=MarkdownInput)

    class Meta:
        model = Post
        fields = ('message', )
        
    
