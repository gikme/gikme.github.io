from html5lib import HTMLParser
from bleach import (
    BleachSanitizer,
    force_unicode,
    _render,
    PROTOCOLS,
)

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALLOWED_PROTOCOLS = PROTOCOLS + ['data', 'cid']
ALLOWED_TAGS = ['a', 'abbr', 'acronym', 'address', 'area', 'b',
                'big', 'blockquote', 'br', 'button', 'caption', 'center', 'cite',
                'code', 'col', 'colgroup', 'dd', 'del', 'dfn', 'dir', 'div', 'dl', 'dt',
                'em', 'fieldset', 'font', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                'hr', 'i', 'img', 'input', 'ins', 'kbd', 'label', 'legend', 'li', 'map',
                'menu', 'ol', 'optgroup', 'option', 'p', 'pre', 'q', 's', 'samp',
                'select', 'small', 'span', 'strike', 'strong', 'sub', 'sup', 'table',
                'tbody', 'td', 'textarea', 'tfoot', 'th', 'thead', 'tr', 'tt', 'u',
                'ul', 'var', 'iframe']
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title'],
    'abbr': ['title'],
    'acronym': ['title'],
    'img': ['alt', 'src', 'title'],
    '*': ['style']
}
ALLOWED_STYLES = ['color', 'background-color', 'font-weight', 'text-decoration']


def clean(text, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES,
          styles=ALLOWED_STYLES, protocols=ALLOWED_PROTOCOLS, strip=False,
          strip_comments=True):
    """
    Clean an HTML fragment and return it

    `protocols` added
    """
    if not text:
        return ''

    text = force_unicode(text)

    class s(BleachSanitizer):
        allowed_elements = tags
        allowed_attributes = attributes
        allowed_css_properties = styles
        allowed_protocols = protocols
        strip_disallowed_elements = strip
        strip_html_comments = strip_comments

    parser = HTMLParser(tokenizer=s)

    return _render(parser.parseFragment(text))


def sanitize(value, strip=True):
    if not value:
        return value

    return clean(value, strip=strip)
