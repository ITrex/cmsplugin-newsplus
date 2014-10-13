#!/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns

from cmsplugin_newsplus import feeds
from cmsplugin_newsplus import views

urlpatterns = patterns(
    'django.views.generic.date_based',
    url(r'^$',
        views.ArchiveIndexView.as_view(), name='news_archive_index'),
    url(r'^by_topic/(?P<topic>[-\w]+)/$',
        views.TopicIndexView.as_view(), name='news_archive_by_topic'),
    url(r'^by_topic/(?P<topic>[-\w]+)/'
        r'(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        views.TopicDetailView.as_view(), name='news_detail_by_topic'),
    url(r'^(?P<year>\d{4})/$',
        views.YearArchiveView.as_view(), name='news_archive_year'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$',
        views.MonthArchiveView.as_view(), name='news_archive_month'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
        views.DayArchiveView.as_view(), name='news_archive_day'),
    url((r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/'
         r'(?P<slug>[-\w]+)/$'),
        views.DetailView.as_view(), name='news_detail'),

    url(r'^feed/$', feeds.NewsFeed())
)
