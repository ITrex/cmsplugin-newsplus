from django.views import generic as generic_views

from . import models
from . import settings


class PublishedNewsMixin(object):
    """
    Since the queryset also has to filter elements by timestamp
    we have to fetch it dynamically.
    """
    def get_queryset(self):
        return models.News.published.all()


class ArchiveIndexView(PublishedNewsMixin, generic_views.ListView):
    """
    A simple archive view that exposes following context:

    * latest
    * date_list
    * paginator
    * page_obj
    * object_list
    * is_paginated

    The first two are intended to mimic the behaviour of the
    date_based.archive_index view while the latter ones are provided by
    ListView.
    """
    paginate_by = settings.ARCHIVE_PAGE_SIZE
    template_name = 'cmsplugin_newsplus/news_archive.html'
    include_yearlist = True
    date_field = 'pub_date'

    def get_context_data(self, **kwargs):
        context = super(ArchiveIndexView, self).get_context_data(**kwargs)
        context['latest'] = context['object_list']
        if self.include_yearlist:
            date_list = self.get_queryset().datetimes('pub_date', 'year')[::-1]
            context['date_list'] = date_list
        return context

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)


class TopicIndexView(generic_views.DetailView):
    """
    A simple archive view that exposes following context:

    * latest
    * date_list
    * paginator
    * page_obj
    * object_list
    * is_paginated

    The first two are intended to mimic the behaviour of the
    date_based.archive_index view while the latter ones are provided by
    ListView.
    """
    paginate_by = settings.ARCHIVE_PAGE_SIZE
    template_name = 'cmsplugin_newsplus/news_archive.html'
    include_yearlist = True
    date_field = 'pub_date'
    model = models.Topic

    def get_context_data(self, **kwargs):
        context = super(TopicIndexView, self).get_context_data(**kwargs)

        context['object_list'] = context['object'].news_set.filter(
            is_published=True).all()

        return context

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)


class DetailView(PublishedNewsMixin, generic_views.DateDetailView):
    month_format = '%m'
    date_field = 'pub_date'

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['all_news'] = models.News.objects.order_by('pub_date')
        return context


class MonthArchiveView(PublishedNewsMixin, generic_views.MonthArchiveView):
    month_format = '%m'
    date_field = 'pub_date'


class YearArchiveView(PublishedNewsMixin, generic_views.YearArchiveView):
    month_format = '%m'
    date_field = 'pub_date'


class DayArchiveView(PublishedNewsMixin, generic_views.DayArchiveView):
    month_format = '%m'
    date_field = 'pub_date'
