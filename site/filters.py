# -*- coding: utf-8 -*-


def cat_name(cat):
    from publishconf import CATEGORY_MAP

    return CATEGORY_MAP.get(cat, '')
