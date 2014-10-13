#!/bin/env python
# -*- coding: utf-8 -*-

"""
This module hooks into django-cms' menu system by providing a clear menu
hierarchy for every news item.
"""

from django.utils.translation import ugettext_lazy as _
from cmsplugin_newsplus.models import Topic, News
from menus.menu_pool import menu_pool
from cms.menu_bases import CMSAttachMenu
from menus.base import NavigationNode
from django.core.urlresolvers import reverse
from menus.base import Modifier
from django.shortcuts import get_object_or_404
from datetime import datetime

class NewsItemMenu(CMSAttachMenu):
    name = _("News menu")

    def get_nodes(self, request):
        result = []
        for topic in Topic.objects.all():
            result.append(NavigationNode(
                topic.title,
                reverse(
                    'news_archive_by_topic',
                    kwargs={'topic': topic.slug}),
                'newsitem-topic-{}'.format(topic.slug)))

        return result

menu_pool.register_menu(NewsItemMenu)
