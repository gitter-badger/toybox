from django import forms
from django_bootstrap_markdown.widgets import MarkdownInput
from django.utils.translation import ugettext_lazy as _
from qishi.models import Post

class NewPostForm(forms.ModelForm):
    subject = forms.CharField(label=_('Subject'), widget=forms.TextInput(attrs={'size': '80'}))
    message = forms.CharField(widget=MarkdownInput)

    class Meta:
        model = Post
        fields = ('message', )


class ReplyPostForm(forms.ModelForm):
	message = forms.CharField(widget=MarkdownInput)
	class Meta:
		model = Post
		fields = ('message', )

class QuickReplyPostForm(ReplyPostForm):
	message = forms.CharField(widget=forms.Textarea)
        
    
