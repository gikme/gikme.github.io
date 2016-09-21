# encoding: utf-8
from __future__ import unicode_literals

import re, urllib

from jinja2 import Markup
from pelican import signals
from pelican.writers import Writer
from pelican.generators import Generator
from pelican.utils import set_date_tzinfo
from feedgenerator import Rss201rev2Feed
from feedgenerator.django.utils.feedgenerator import rfc2822_date
from beeprint import pp

from .sanitizer import sanitize

# These are the attributes we want to pass to iTunes.
# TODO: provide a link to documentation about expected attributes.
ITEM_ELEMENTS = (
    'title',
    'itunes:author',
    'itunes:subtitle',
    'itunes:summary',
    'itunes:image',
    'enclosure',
    'description',
    'link',
    'guid',
    'pubDate',
    'itunes:duration',
    )

DEFAULT_ITEM_ELEMENTS = {}
for key in ITEM_ELEMENTS:
    DEFAULT_ITEM_ELEMENTS[key] = None


class ResroeUrlMixin(object):
    def _restore_url(self, url):
        if not url.startswith('http'):
            url = url.startswith('/') or u'/%s' % url

            return u'%s/%s' % (self.site_url, url)

        return url


class PodcastFeed(Rss201rev2Feed, ResroeUrlMixin):
    """Helper class which generates the XML based in the global settings"""
    def __init__(self, *args, **kwargs):
        self.category = kwargs.pop('category', '')
        self.site_url = kwargs.get('link', ' ')[:-1]
        self.feed_url = kwargs.get('feed_url', self.site_url)
        super(PodcastFeed, self).__init__(*args, **kwargs)

    def set_settings(self, settings):
        """Helper function which just receives the podcast settings.
        :param settings: A dictionary with all the site settings.
        """
        self.settings = settings

    def rss_attributes(self):
        """Returns the podcast feed's attributes.

        :return: A dictionary containing the feed's attributes.
        """
        attrs = super(PodcastFeed, self).root_attributes()
        attrs['xmlns:itunes'] = "http://www.itunes.com/dtds/podcast-1.0.dtd"
        attrs['xmlns:media'] = "http://search.yahoo.com/mrss/"
        attrs['xmlns:creativeCommons'] = "http://backend.userland.com/creativeCommonsRssModule"
        attrs['version'] = '2.0'
        return attrs

    def add_root_elements(self, handler):
        """Adds some basic but useful attributes for an iTunes feed.

        :param handler: A SimplerXMLGenerator instance.
        """
        super(PodcastFeed, self).add_root_elements(handler)
        handler.addQuickElement(
            'atom10:link', attrs={
                'xmlns:atom10': "http://www.w3.org/2005/Atom",
                'rel': "self",
                'type': "application/rss+xml",
                'href': self.feed_url,
            }
        )

        # Creative Commons

        # Adds a copyright root tag. Ex:
        #  <copyright>℗ &© 2014 Hack 'n' Cast</copyright>
        if 'CC_TEXT' in self.settings:
            handler.addQuickElement(
                'copyright', self.settings['CC_TEXT']
            )
            handler.addQuickElement(
                'media:copyright', self.settings['CC_TEXT']
            )

        # Adds a copyright root tag. Ex:
        #  <creativeCommons:license>℗ &© 2014 Hack 'n' Cast</creativeCommons:license>
        if 'CC_LINK' in self.settings:
            handler.addQuickElement(
                'creativeCommons:license', self.settings['CC_LINK']
            )

        # podcast

        podcast_meta = self.settings.get('PODCAST', {}).get(self.category, None)

        if podcast_meta:
            # Adds a language root tag. Ex:
            #  <language>en</language>
            if 'language' in podcast_meta:
                handler.addQuickElement(
                    'language', podcast_meta['language']
                )
            # Adds a explicit content root tag. Ex:
            #  <itunes:explicit>No</itunes:explicit>
            if 'explicit' in podcast_meta:
                handler.addQuickElement(
                    'itunes:explicit', podcast_meta['explicit']
                )
            # Adds a show subtitle root tag. Ex:
            #  <itunes:subtitle>The hacker podcast!</itunes:subtitle>
            if 'subtitle' in podcast_meta:
                handler.addQuickElement(
                    'itunes:subtitle', podcast_meta['subtitle']
                )
            # Adds a author root tag. Ex:
            #  <itunes:author>John Doe</itunes:author>
            if 'author' in podcast_meta:
                handler.addQuickElement(
                    'itunes:author', podcast_meta['author']
                )
            # Adds a podcast summary root tag. Ex:
            #  <itunes:summary>A podcast about... </itunes:summary>
            if 'summary' in podcast_meta:
                handler.addQuickElement(
                    'itunes:summary', podcast_meta['summary']
                )
            # Adds a podcast summary root tag. Ex:
            #  <itunes:keywords>tag1,tag2</itunes:keywords>
            if 'keywords' in podcast_meta:
                handler.addQuickElement(
                    'itunes:keywords', podcast_meta['keywords']
                )
                handler.addQuickElement(
                    'media:keywords', podcast_meta['keywords']
                )
            # Adds a podcast logo image root tag. Ex:
            #  <itunes:image href="http://example.com/logo.jpg" />
            if 'image' in podcast_meta:
                handler.addQuickElement(
                'itunes:image', attrs={
                    'href': self._restore_url(podcast_meta['image'])
                    }
                )
                handler.addQuickElement(
                'media:thumbnail', attrs={
                    'url': self._restore_url(podcast_meta['image'])
                    }
                )
            # Adds a feed owner root tag an some child tags. Ex:
            #  <itunes:owner>
            #    <itunes:name>John Doe</itunes:name>
            #    <itunes:email>john.doe@example.com</itunes:email>
            #  </itunes:owner>
            if ('owner' in podcast_meta and
                    'email' in podcast_meta):
                handler.startElement('itunes:owner', {})
                handler.addQuickElement(
                    'itunes:name', podcast_meta['owner']
                )
                handler.addQuickElement(
                    'itunes:email', podcast_meta['email']
                )
                handler.endElement('itunes:owner')
            # Adds a show category root tag and some child tags. Ex:
            #  <itunes:category text="Technology">
            #   <itunes:category text="Gadgets"/>
            #  </itunes:category>
            if 'categories' in podcast_meta:
                for category in podcast_meta['categories']:
                  if type(category) in (list, tuple):
                      handler.startElement(
                          'itunes:category', attrs={'text': category[0]}
                      )
                      handler.addQuickElement(
                          'itunes:category', attrs={'text': category[1]}
                      )
                      handler.endElement('itunes:category')
                      handler.addQuickElement(
                          'media:category', u'/'.join(category), attrs={'scheme': "http://www.itunes.com/dtds/podcast-1.0.dtd"}
                      )
                  else:
                      handler.addQuickElement(
                          'itunes:category', attrs={'text': category}
                      )
                      handler.addQuickElement(
                          'media:category', category, attrs={'scheme': "http://www.itunes.com/dtds/podcast-1.0.dtd"}
                      )

    def add_item_elements(self, handler, item):
        """Adds a new element to the iTunes feed, using information from
        ``item`` to populate it with relevant information about the article.

        :param handler: A SimplerXMLGenerator instance
        :param item: The dict generated by iTunesWriter._add_item_to_the_feed

        """
        for key in DEFAULT_ITEM_ELEMENTS:
            # empty attributes will be ignored.
            if item[key] is None:
                continue
            if key == 'description':
                content = item[key]
                handler.startElement('description', {})
                if not isinstance(content, unicode):
                    content = unicode(content, handler._encoding)
                content = content.replace("<html><body>", "")
                handler._write(content)
                handler.endElement('description')
            elif type(item[key]) in (str, unicode):
                handler.addQuickElement(key, item[key])
            elif type(item[key]) is dict:
                handler.addQuickElement(key, attrs=item[key])


class iTunesWriter(Writer, ResroeUrlMixin):
    """Writer class for our iTunes feed.  This class is responsible for
    invoking the PodcastFeed and writing the feed itself (using it's superclass
    methods)."""

    def __init__(self, *args, **kwargs):
        """Class initializer"""
        super(iTunesWriter, self).__init__(*args, **kwargs)

    def write_feed(self, elements, context, path=None, feed_type='atom', *args, **kwargs):
        path_template = self.settings.get('CATEGORY_FEED_RSS', '') or self.settings.get('CATEGORY_FEED_ATOM', '')

        if path and path_template:
            cat_regex = re.compile(path_template.replace('%s', r'(\S+?)'))
            self.category = cat_regex.findall(path)[0]
        else:
            self.category = ''

        return super(iTunesWriter, self).write_feed(elements, context, path, feed_type, *args, **kwargs)

    def _create_new_feed(self, feed_type, context):
        """Helper function (called by the super class) which will initialize
        the PodcastFeed object."""
        self.context = context
        description = self.settings.get('PODCAST_FEED_SUMMARY', '')
        title = (self.settings.get('PODCAST_FEED_TITLE', '') or
                 context['SITENAME'])
        feed = PodcastFeed(
            title=title,
            link=(self.site_url + '/'),
            feed_url=self.feed_url,
            description=description,
            category=self.category)
        feed.set_settings(self.settings)
        return feed

    def _add_item_to_the_feed(self, feed, item):
        """Performs an 'in-place' update of existing 'published' articles
        in ``feed`` by creating a new entry using the contents from the
        ``item`` being passed.
        This method is invoked by pelican's core.

        :param feed: A PodcastFeed instance.
        :param item: An article (pelican's Article object).

        """
        postfix = u''
        # Local copy of iTunes attributes to add to the feed.
        items = DEFAULT_ITEM_ELEMENTS.copy()

        # Link to the new article.
        #  http://example.com/episode-01
        items['link'] = self._restore_url(item.url)

        # Title for the article.
        #  ex: <title>Episode Title</title>
        items['title'] = Markup(item.title).striptags()

        # Date the article was last modified.
        #  ex: <pubDate>Fri, 13 Jun 2014 04:59:00 -0300</pubDate>
        items['pubDate'] = rfc2822_date(
            set_date_tzinfo(
                item.modified if hasattr(item, 'modified') else item.date,
                self.settings.get('TIMEZONE', None))
            )

        # Name(s) for the article's author(s).
        #  ex: <itunes:author>John Doe</itunes:author>
        if hasattr(item, 'author'):
            items['itunes:author'] = item.author.name

        # Subtitle for the article.
        #  ex: <itunes:subtitle>My episode subtitle</itunes:subtitle>
        if hasattr(item, 'subtitle'):
            items['itunes:subtitle'] = Markup(item.subtitle).striptags()

        # Ex:
        #  <itunes:image href="http://example.com/Episodio1.jpg" />
        if hasattr(item, 'image'):
            items['itunes:image'] = {
                'href': self._restore_url(item.image)}

            image = u'<img alt="{0}" src="{1}"/><br/>'.format(
                                                              items['title'].replace('&', '&amp;'
                                                              ).replace('<', '&lt;'
                                                              ).replace('>', '&gt;'
                                                              ).replace('"', '&quot;'
                                                              ).replace("'", '&#39;'
                                                              ), self._restore_url(item.image))
        else:
            image = ''

        # Information about the episode audio.
        #  ex: <enclosure url="http://example.com/episode.m4a"
        #   length="872731" type="audio/x-m4a" />
        if hasattr(item, 'enclosure'):
            enclosure = {'url': self._restore_url(item.enclosure)}
            # Include the file size if available.
            if hasattr(item, 'length'):
                enclosure['length'] = item.length
            else:
                if item.enclosure.startswith('http'):
                    enclosure['length'] = urllib.urlopen(item.enclosure).info().getheaders("Content-Length")[0]
                elif 'PODCAST_FILES_ROOT' in self.settings:
                    enclosure['length'] = os.path.getsize(os.path.join(self.settings['PODCAST_FILES_ROOT'],
                                                                       item.enclosure))
                else:
                    enclosure['length'] = '1000000000'
            # Include the audio mime type if available...
            if hasattr(item, 'mime'):
                enclosure['type'] = item.mime
            else:
                # ... or default to 'audio/mpeg'.
                enclosure['type'] = 'audio/mpeg'
            items['enclosure'] = enclosure

            postfix = u'<p><a href="{0}">Скачать вложение</a></p>'.format(item.enclosure)

        # Duration for the audio file.
        #  <itunes:duration>7:04</itunes:duration>
        if hasattr(item, 'duration'):
            items['itunes:duration'] = item.duration

        # Unique identifier for the episode.
        # Use a 'guid' if available...
        #  ex: <guid>http://example.com/aae20050615.m4a</guid>
        if hasattr(item, 'guid'):
            items['guid'] = item.guid
        # ... else, use the article's link instead.
        #  ex: <guid>http://example.com/episode-01</guid>
        else:
            items['guid'] = items['link']
        # Add the new article to the feed.

        content = image + item.get_content(self.site_url) + postfix

        items['description'] = "<![CDATA[{}]]>".format(sanitize(content))

        # Summary for the article. This can be obtained either from
        # a ``:description:`` or a ``:summary:`` directive.
        #  ex: <itunes:summary>In this episode... </itunes:summary>
        items['itunes:summary'] = Markup(item.content).striptags()

        feed.add_item(**items)


def get_writer(writers):
    """Module function invoked by the signal 'get_generators'."""
    return iTunesWriter


def register():
    # signals.get_generators.connect(get_generators)
    signals.get_writer.connect(get_writer)
