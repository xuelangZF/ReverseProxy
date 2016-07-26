#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Last Modified time: 2016-06-06 09:26:32

from .urlprocess import get_url_suffix
from .pageparse import HtmlParse, JSCssParse, ImageParse, CommonParse


class PageManagement(object):
    @classmethod
    def get_page_obj(cls, new_path, **kwargs):
        """Get the suitable pages object from the suffix information

        headers:    used in the method: requests.get().
        kwargs[ip]: visitor's ip address.
        """
        suffix = get_url_suffix(new_path)
        if suffix == "html":
            return HtmlParse(new_path, **kwargs)
        elif suffix in ["js", "css"]:
            return JSCssParse(new_path, suffix, **kwargs)
        elif suffix in ["jpg", "png", "gif", "ico", "jpeg"]:
            return ImageParse(new_path, suffix, **kwargs)
        elif suffix:
            return CommonParse(new_path, suffix, **kwargs)
        else:
            pass
