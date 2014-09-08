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


class News(models.Model):
    """
    News
    """

    published = PublishedNewsManager()

    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(_('slug'), unique_for_date='pub_date',
                            help_text=_('A slug is a short name which uniquely'
                                        ' identifies the news item for this'
                                        ' day'))
    excerpt = models.TextField(_('excerpt'), blank=True)
    content = models.TextField(_('content'), blank=True)

    is_published = models.BooleanField(_('published'), default=True)
    pub_date = models.DateTimeField(
        _('publication date'),
        default=datetime.datetime.utcnow().replace(tzinfo=utc))

    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    link = models.URLField(
        _('link'), blank=True, null=True,
        help_text=_('This link will be used a absolute url'
                    ' for this item and replaces the view'
                    ' logic. <br />Note that by default'
                    ' this only applies for items with '
                    ' an empty "content" field.'))

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
    limit = models.PositiveIntegerField(_('number of news items to show'),
                                        help_text=_('Limits the number of '
                                                    'items that will be '
                                                    'displayed'))
