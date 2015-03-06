from django import forms
from django_bootstrap_markdown.widgets import MarkdownInput


class NewPostForm(forms.Form):
    edit_area = forms.CharField(widget=MarkdownInput)
