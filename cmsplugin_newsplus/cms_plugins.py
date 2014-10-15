from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from cmsplugin_newsplus.models import LatestNewsPlugin, News
from cmsplugin_newsplus import settings


class CMSLatestNewsPlugin(CMSPluginBase):
    """
        Plugin class for the latest news
    """
    model = LatestNewsPlugin
    name = _('Latest news')
    render_template = "cmsplugin_newsplus/latest_news.html"

    def render(self, context, instance, placeholder):
        """
            Render the latest news
        """
        latest = News.published.all()

        if instance.topic:
            latest = latest.filter(topic=instance.topic)

        latest = latest[:instance.limit]

        context.update({
            'instance': instance,
            'latest': latest,
            'placeholder': placeholder,
            'add_placeholder': News(pk=0)
        })
        return context

if not settings.DISABLE_LATEST_NEWS_PLUGIN:
    plugin_pool.register_plugin(CMSLatestNewsPlugin)
