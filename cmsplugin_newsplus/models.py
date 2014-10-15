#!/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.utils.timezone import utc
import datetime

from cms.models import CMSPlugin

from . import settings


class PublishedNewsManager(models.Manager):
    """
        Filters out all unpublished and items with a publication
        date in the future
    """
    def get_query_set(self):
        return super(PublishedNewsManager, self).get_query_set() \
            .filter(is_published=True) \
            .filter(
                pub_date__lte=datetime.datetime.utcnow().replace(tzinfo=utc))


class Topic(models.Model):
    ''' Topic '''
    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(_('slug'), unique=True, null=True, blank=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _(u'тема')
        verbose_name_plural = _(u'темы')


class News(models.Model):
    """
    News
    """
    objects = models.Manager()
    published = PublishedNewsManager()

    topic = models.ForeignKey(
        Topic, verbose_name=_('topic'),
        null=False, default=1)

    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(_('slug'), unique_for_date='pub_date',
                            help_text=_('A slug is a short name which uniquely'
                                        ' identifies the news item for this'
                                        ' day'))

    excerpt = models.TextField(verbose_name=_(u'анонс'), blank=True)
    content = models.TextField(verbose_name=_(u'содержимое'), blank=True)

    is_published = models.BooleanField(_('published'), default=True)
    pub_date = models.DateTimeField(
        _('publication date'),
        default=datetime.datetime.utcnow().replace(tzinfo=utc))

    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    author = models.CharField(
        max_length=256, verbose_name=_(u'автор'),
        blank=True, default="")

    source_url = models.URLField(
        max_length=512, verbose_name=_(u'URL источника'),
        blank=True, default="")

    source = models.CharField(
        max_length=512, verbose_name=_(u'источник'),
        blank=True, default="")

    def get_absolute_url(self):
        # if this is default topic - do not specify topic argument in url
        if self.topic.id == 1:
            return reverse(
                'news_detail',
                kwargs={'year': self.pub_date.strftime("%Y"),
                        'month': self.pub_date.strftime("%m"),
                        'day': self.pub_date.strftime("%d"),
                        'slug': self.slug})
        else:
            return reverse(
                'news_detail_by_topic',
                kwargs={
                    'topic': self.topic.slug,
                    'year': self.pub_date.strftime("%Y"),
                    'month': self.pub_date.strftime("%m"),
                    'day': self.pub_date.strftime("%d"),
                    'slug': self.slug})

    class Meta:
        verbose_name = _('news')
        verbose_name_plural = _('news')
        ordering = ('-pub_date', )

    def __unicode__(self):
        return self.title


class NewsImage(models.Model):
    class Meta:
        verbose_name = _('image')
        verbose_name_plural = _('images')

    news = models.ForeignKey(News, related_name='images')
    image = models.ImageField(upload_to="news_images")

    def __unicode__(self):
        return self.image.url


class LatestNewsPlugin(CMSPlugin):
    """
        Model for the settings when using the latest news cms plugin
    """
    limit = models.PositiveIntegerField(
        _(u'количество последних новостей для отображения'))

    default_img = models.ImageField(
        verbose_name=_(u'изображение по умолчанию'),
        upload_to="news_images", blank=True)

    topic = models.ForeignKey(
        Topic, verbose_name=_('topic'),
        null=True, blank=True)
