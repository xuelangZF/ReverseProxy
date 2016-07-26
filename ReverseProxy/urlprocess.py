#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Last Modified time: 2016-06-01 20:14:13
import urlparse
import requests


def replace_domain(original_url, target_domain, port=80):
    """Replace the domain of the original_url.

    http://original.com/pages         --> http://baidu.com/pages
    """
    result = urlparse.urlparse(original_url)
    return result._replace(netloc="%s:%d" % (target_domain, port)).geturl()


def replace_sub_domain(original_url, target_domain, port=80):
    """Replace top domain of the url

    http://sub.original.com/pages       --> http://sub.baidu.com/pages
    http://sub.original.com:8000/pages  --> http://sub.baidu.com:8000/pages
    """
    result = urlparse.urlparse(original_url)
    domain_list = result.netloc.split(".")
    if len(domain_list) <= 2:
        print "Error!!! %s" % original_url
        return
    # Get the top domain's position.
    else:
        new_netloc = "%s.%s" % ("".join(domain_list[:-2]), target_domain)
    return result._replace(netloc="%s:%d" % (new_netloc, port)).geturl()


def remove_anchor(original_url):
    """Remove the anchor in url.

    http://original.com/pages?time=1#23 --> http://baidu.com/pages?time=1
    """
    result = urlparse.urlparse(original_url)
    return result._replace(fragment=None).geturl()


def get_url_suffix(path):
    """ Get the requested type of resource.

    Use HEAD request is to check the content type of the URL.
    We need to allow redirect in 'request.head' method, otherwise we may get wrong info.
    """
    res = requests.head(path, allow_redirects=True)
    content_type = res.headers.get('content-type', None) or res.headers.get('Content-Type', None)
    if content_type:
        if any(x in content_type for x in ["html", "htm"]):
            return "html"
        elif any(x in content_type for x in ["jpeg", "jpg"]):
            return "jpg"
        elif any(x in content_type for x in ["png"]):
            return "png"
        elif any(x in content_type for x in ["gif"]):
            return "gif"
        elif any(x in content_type for x in ["javascript", "js", "x-javascript"]):
            return "js"
        elif any(x in content_type for x in ["css"]):
            return "css"
        else:
            pass

    # Go here means that we have meet some unknown types.
    # Then check the file type using url meta information.
    # https://v2ex.com/static/fonts/font.woff2?v=4.6.1 --> woff2
    url_path = urlparse.urlparse(path).path
    url_path_l = url_path.split(".")
    if len(url_path_l) != 1:
        return url_path_l[-1]
    else:
        return None
