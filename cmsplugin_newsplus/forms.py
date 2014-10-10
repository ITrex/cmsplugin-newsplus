from __future__ import absolute_import
from django import forms
from django.conf import settings

from cms.plugin_pool import plugin_pool
from djangocms_text_ckeditor.widgets import TextEditorWidget
from cmsplugin_newsplus.models import News
