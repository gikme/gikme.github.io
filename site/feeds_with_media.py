# -*- coding: utf-8 -*-

# from pelican.generators import ArticlesGenerator
from six.moves.urllib.parse import urlparse

# from feedgenerator import Atom1Feed, Rss201rev2Feed
from jinja2 import Markup
from pelican import signals
from pelican.writers import Writer
from pelican.utils import set_date_tzinfo
from feedgenerator.django.utils.feedgenerator import Enclosure, iri_to_uri
from feedgenerator import Atom1Feed, Rss201rev2Feed as Rss


class Image(object):
    "Represents an RSS image"
    def __init__(self, link, title, url, width=None, height=None, description=''):
        "All args are expected to be Python Unicode objects"
        self.link = iri_to_uri(link)
        self.url = iri_to_uri(url)
        self.title, self.width, self.height, self.description = title, width, height, \
            description


class Rss201rev2Feed(Rss):
    # Spec: http://blogs.law.harvard.edu/tech/rss
    _version = "2.0"

    def add_root_elements(self, handler):
        super(Rss201rev2Feed, self).add_root_elements(handler)

        if self.feed['image'] is not None:
            handler.startElement(u"image", {})
            handler.addQuickElement(u"title", unicode(self.feed['image'].title))
            handler.addQuickElement(u"url", unicode(self.feed['image'].url))
            handler.addQuickElement(u"link", unicode(self.feed['image'].link))

            if self.feed['image'].description:
                handler.addQuickElement(u"description", unicode(self.feed['image'].description))

            if self.feed['image'].height:
                handler.addQuickElement(u"height", unicode(self.feed['image'].height))

            if self.feed['image'].width:
                handler.addQuickElement(u"width", unicode(self.feed['image'].width))

            handler.endElement(u"image")


class MediaWriter(Writer):
    """
    Media file support in feed writer
    """
    def _create_new_feed(self, feed_type, context):
        feed_class = Rss201rev2Feed if feed_type == 'rss' else Atom1Feed
        sitename = Markup(context['SITENAME']).striptags()
        image = context.get('FEED_IMAGE', None)

        if image:
            if not image.startswith('http'):
                image = self.settings['SITEURL'] + image

            image = Image(context.get('SITEURL'), sitename, image)

        feed = feed_class(
            title=sitename,
            link=(self.site_url + '/'),
            feed_url=self.feed_url,
            description=context.get('SITESUBTITLE', ''),
            image=image)

        return feed

    def _add_item_to_the_feed(self, feed, item):
        title = Markup(item.title).striptags()
        enclosure = getattr(item, 'enclosure', '')
        mime = getattr(item, 'mime', '')
        image = getattr(item, 'image', '')

        if enclosure:
            if not enclosure.startswith('http'):
                enclosure = self.settings['SITEURL'] + enclosure

            enclosure = Enclosure(enclosure, '', mime)
        else:
            enclosure = None

        if image:
            if not image.startswith('http'):
                image = self.settings['SITEURL'] + image

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
