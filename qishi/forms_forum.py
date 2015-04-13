from django import forms
#from django_bootstrap_markdown.widgets import MarkdownInput
from django.utils.translation import ugettext_lazy as _
from qishi.models import Post
from bootstrap_markdown.widgets import MarkdownEditor

class NewPostForm(forms.ModelForm):
    subject = forms.CharField(label=_('Subject'), widget=forms.TextInput(attrs={'size': '80'}))
    message = forms.CharField(widget=MarkdownEditor(
        attrs={'id': 'content'}))

    class Meta:
        model = Post
        fields = ('message', )


class ReplyPostForm(forms.ModelForm):
	message = forms.CharField(widget=MarkdownEditor(
        attrs={'id': 'content'}))
	class Meta:
		model = Post
		fields = ('message', )

class QuickReplyPostForm(ReplyPostForm):
	message = forms.CharField(widget=forms.Textarea)
	
class EditPostForm(NewPostForm):
    def __init__(self, *args, **kwargs):
        super(EditPostForm, self).__init__(*args, **kwargs)
        self.initial['subject'] = self.instance.subject()
        self.initial['message'] = self.instance.message
        if not self.instance.topic_post:
            self.fields['subject'].required = False
        
    
