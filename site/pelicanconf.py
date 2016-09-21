#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

import os
import sys
sys.path.append(os.curdir)

from filters import cat_name


AUTHOR = u'gik.me'
SITENAME = u'gik.me [closed]'
SITESUBTITLE = u'Закрытый гиковский подкаст'
SITEURL = 'http://gik.me'
DISQUS_SITENAME = 'gikme'

PATH = 'content'
DIRECT_TEMPLATES = ['index', 'tags', 'categories', 'archives', 'search']
# STATIC_PATHS = ['audio', 'podcast', 'overflow', 'text', 'downloads']
# ARTICLE_PATHS = ['audio', 'podcast', 'overflow', 'text']
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{slug}.html'
ARTICLE_URL = '{date:%Y}/{date:%m}/{slug}.html'

TIMEZONE = 'Asia/Omsk'

DEFAULT_LANG = u'ru_RU'

# Feed generation is usually not desired when developing
FEED_DOMAIN = SITEURL
# FEED_MAX_ITEMS = 15
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

STATIC_PATHS = ['images', 'extra/robots.txt', 'extra/favicon.ico', 'extra/CNAME']
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/favicon.ico': {'path': 'favicon.ico'},
    'extra/CNAME': {'path': 'CNAME'},
}

DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = False
USE_FOLDER_AS_CATEGORY = False
DEFAULT_CATEGORY = 'text'
DEFAULT_DATE_FORMAT = '%a %d %B %Y'
DELETE_OUTPUT_DIRECTORY = True

SUMMARY_MAX_LENGTH = 30
PAGE_ORDER_BY = 'order'

PLUGIN_PATHS = ['plugins']
PLUGINS = ['podcast_generator', 'tipue_search']

FEED_IMAGE = '/image/logotry1400x1400.png'
FEED_FOOTER = {
    'podcast': '''<p><strong>Музыка:</strong>
<a href="http://vk.com/bacc3" target="_blank">Василий Корчагин - Аляска</a></p>'''
}
CC_LINK = 'http://creativecommons.org/licenses/by-nc-nd/3.0/'
CC_TEXT = 'Creative Commons - Attribution, Noncommercial, No Derivative Works 3.0 License'


PODCAST = {
    'podcast': {
        'language': 'ru-ru',
        'explicit': 'yes',
        'subtitle': u'Подкаст об IT, айтишниках и всём к ним прилегающем',
        'author': 'gik.me',
        'image': '/images/gm_cover_2000x2000.png',
        'owner': 'gik.me',
        'categories': [
            ['Technology', 'Tech News'],
            ['Technology', 'Gadgets'],
            ['Technology', 'Software How-To'],
            ['Technology', 'Podcasting'],
        ],
        'keywords': u'it,gadgets,api,disign,technology,architecture,os,programming,language,дизайн,технологии,айти,ахитектура,язык,программирования',
        'summary': u'''С 1861 года в подкасчечной записывают лучшие подкасты на самые крутые темы (об айти, понятно-красно). Нас четверо:

Бекендер Вадя - на людёв кладя.
Дизайнер Саша — в голове каша.
Пээмка Даша — тупняша.
Фронтендер Тёма — шутит про хуи и не может в рифму.

У нас есть всё для подкастинации.
Мы — мухи-стервятники мира подкастов!
Мы — опоссумы-верхолазы здравого смысла!
Мы — манифест!
Семя безумного, дробного, млечного!

А ты подкастинировал сивоня?
Слушай наши подкасты, не будь мудаком!

Сео оптимизировал оптимизировал, да не выоптимизировал:
#google [90], #apple [73], #microsoft [56], #android [46], #facebook [37], #yandex [35], #samsung [31], #odnonazvanie [27], #windows [27], #gikme [26], #vkontakte [25], #ubuntu [24], #linux [21], #iphone [20], #steam [18], #telegram [18], #tesla [18], #valve [17], #playstation [17], #sony [16], #nokia [14], #russianpost [14]''',
    },
    'nedocast': {
        'language': 'ru-ru',
        'explicit': 'yes',
        'subtitle': u'18+ Аудиолог старых знакомых',
        'author': 'gik.me',
        'image': '/images/on_cover_2000x2000.png',
        'owner': 'gik.me',
        'categories': [
            'Comedy',
            'Kids &amp; Family',
            ['Games &amp; Hobbies', 'Video Games'],
            ['Society &amp; Culture', 'Places &amp; Travel']
        ],
        'keywords': u'life,personal,podcast,blog,jokes,stories,log,talks,humor',
        'summary': u'Сплошное ИМХО, трололо и азаза…',
    },
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
    'nedocast': u'недокаст',
    'perl': u'перлы',
}

MENUITEMS = (
    ('podcast', '/category/podcast.html', u'Подкаст<sup>18+</sup>'),
    ('nedocast', '/category/nedocast.html', u'Недокаст<sup>18+</sup>'),
)

SIDEMENUITEMS = (
    ('overflow', '/category/overflow.html', u'Не вошедшее'),
    ('news', '/category/news.html', u'Новости'),
    ('perl', '/category/perl.html', u'Перлы'),
    ('prelude', '/category/prelude.html', u'Прелюдии<sup>18+</sup>'),
)

from sidebar_items import *
