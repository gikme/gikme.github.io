# -*- coding: utf-8 -*-

# from pelican.generators import ArticlesGenerator
from six.moves.urllib.parse import urlparse

# from feedgenerator import Atom1Feed, Rss201rev2Feed
from jinja2 import Markup
from pelican import signals
from pelican.writers import Writer
from pelican.utils import set_date_tzinfo
from feedgenerator.django.utils.feedgenerator import Enclosure


class MediaWriter(Writer):
    """
    Media file support in feed writer
    """

    def _add_item_to_the_feed(self, feed, item):
        title = Markup(item.title).striptags()
        enclosure = getattr(item, 'enclosure', '')
        mime = getattr(item, 'mime', '')
        enclosure = enclosure and Enclosure(enclosure, '', mime) or None
        image = getattr(item, 'image', '')

        if image:
            image = u'<img alt="{0}" src="{1}"/><br/>'.format(
                                                                title.replace('&', '&amp;'
                                                                ).replace('<', '&lt;'
                                                                ).replace('>', '&gt;'
                                                                ).replace('"', '&quot;'
                                                                ).replace("'", '&#39;'
                                                                ), image)

        link = '%s/%s' % (self.site_url, item.url)
        feed.add_item(
            title=title,
            link=link,
            unique_id='tag:%s,%s:%s' % (urlparse(link).netloc,
                                        item.date.date(),
                                        urlparse(link).path.lstrip('/')),
            description=image + item.get_content(self.site_url),
            categories=item.tags if hasattr(item, 'tags') else None,
            author_name=getattr(item, 'author', ''),
            enclosure=enclosure,
            pubdate=set_date_tzinfo(
                item.modified if hasattr(item, 'modified') else item.date,
                self.settings.get('TIMEZONE', None)))


def get_writer(writers):
    """Module function invoked by the signal 'get_generators'."""
    return MediaWriter


def register():
    """Registers the module function `get_writer`."""
    signals.get_writer.connect(get_writer)
