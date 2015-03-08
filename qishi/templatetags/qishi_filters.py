# -*- coding: UTF-8 -*-
from django import template
from markdown import markdown

register = template.Library()


@register.filter
def text_markdown(text):
    return markdown(text, safe_mode="escape" )


 
