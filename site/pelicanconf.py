#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

import os
import sys
sys.path.append(os.curdir)

from filters import cat_name


AUTHOR = u'gikme'
SITENAME = u'gik.me'
SITESUBTITLE = u'Гиковский IT подкаст'
SITEURL = 'http://gik.me'
DISQUS_SITENAME = 'gikme'

PATH = 'content'
# STATIC_PATHS = ['audio', 'podcast', 'overflow', 'text', 'downloads']
# ARTICLE_PATHS = ['audio', 'podcast', 'overflow', 'text']
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{slug}.html'
ARTICLE_URL = '{date:%Y}/{date:%m}/{slug}.html'

TIMEZONE = 'Asia/Omsk'

DEFAULT_LANG = u'ru_RU'

# Feed generation is usually not desired when developing
FEED_DOMAIN = SITEURL
FEED_MAX_ITEMS = 15
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
FEED_ALL_RSS = 'feeds/all.rss.xml'
FEED_ALL_ATOM = None
CATEGORY_FEED_RSS = 'feeds/%s.rss.xml'
CATEGORY_FEED_ATOM = None
# TAG_FEED_RSS = 'feeds/%s.tag.rss.xml'
# TAG_FEED_ATOM = 'feeds/%s.tag.atom.xml'
JINJA_FILTERS = {
    'cat_name': cat_name,
}

DEFAULT_PAGINATION = 10
LOAD_CONTENT_CACHE = False

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
TYPOGRIFY = True

THEME = './themes/gikme-light'
# THEME = './themes/blue-penguin'
# THEME = 'simple'

STATIC_PATHS = ['images', 'extra/robots.txt', 'extra/favicon.ico']
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/favicon.ico': {'path': 'favicon.ico'}
}

DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = False
USE_FOLDER_AS_CATEGORY = False
DEFAULT_CATEGORY = 'text'
DEFAULT_DATE_FORMAT = '%a %d %B %Y'
DELETE_OUTPUT_DIRECTORY = True

SUMMARY_MAX_LENGTH = 30
PAGE_ORDER_BY = 'order'

PLUGINS = ['feeds_with_media', ]

FEED_IMAGE = '/image/logotry1400x1400.png'
FEED_FOOTER = {
    'podcast': '''<p><strong>Музыка:</strong>
<a href="http://vk.com/bacc3" target="_blank">Василий Корчагин - Аляска</a></p>'''
}
CATEGORY_MAP = {
    'hangout': u'хэнгаут',
    'link': u'ссылки',
    'overflow': u'не вошедшее',
    'podcast': u'подкаст',
    'quote': u'цитаты',
    'text': u'текст',
    'blog': u'блог',
    'news': u'новости',
    'prelude': u'прелюдии',
}

MENUITEMS = (
    ('podcast', '/category/podcast.html', u'Подкаст'),
    ('overflow', '/category/overflow.html', u'Не вошедшее'),
    ('prelude', '/category/prelude.html', u'Прелюдии [18+]'),
    ('news', '/category/news.html', u'Новости'),
)

from sidebar_items import *
