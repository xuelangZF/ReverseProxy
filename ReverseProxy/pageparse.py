#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Last Modified time: 2016-06-06 09:26:32
import requests
import hashlib
import os
import time
from lxml import html
from . import cache_dir, app_setting


class PageParse(object):
    def __init__(self, new_path, suffix, **kwargs):
        # Sometimes there are chinese in urls, so encode to utf-8
        # For example http://selfboot.cn/这是测试链接.html
        md5_val = hashlib.md5(new_path.encode("utf-8")).hexdigest()

        self.headers = kwargs['headers']

        self.url = new_path
        self.file_name = "%s%s" % (md5_val, ".%s" % suffix)


    def __str__(self):
        """Return the filename of the current requested url.
        """
        return self.get_file()

    def get_file(self):
        """Get the needed file from cache or crawl from the web.

        If we can find the cached file, return immediately.
        Else get the content and return.
        """
        path = self._is_cached_()
        return path if path else self.get_content()

    def _is_cached_(self, expired_time):
        """Check if the current url is cached in the static directory.

        Return the cache's path if it's cached and not expired, else return None.
        """
        file_path = "%s%s" % (cache_dir, self.file_name)
        if not os.path.isfile(file_path):
            return False

        modified_time = os.path.getmtime(file_path)
        cur_time = time.time()
        if cur_time - modified_time < expired_time:
            return self.file_name
        else:
            return False

    def _cache_file_(self, page_content):
        """Save the html, js or css file to cache, and return the path of the file.
        """
        with open("%s%s" % (cache_dir, self.file_name), 'wb') as file_:
            file_.write(page_content)

        return self.file_name


class HtmlParse(PageParse):
    def __init__(self, new_path, **kwargs):
        PageParse.__init__(self, new_path, 'html', **kwargs)

    def get_content(self):
        """Get the url's content from replaced url, and do some necessary modifications.

        Return the modified cached file path.
        """
        try:
            res = requests.get(self.url, headers=self.headers)
        except:
            pass
        if res.status_code != 200:
            return "templates/400.html"

        # Get the real encoding of the page.
        # refer to: http://sh3ll.me/2014/06/18/python-requests-encoding/
        # The encoding of the response will be ISO-8859-1 if there is no charset found in headers.
        # So we need to get its real encoding from apparent_encoding(not 100% correct)
        if res.encoding == "ISO-8859-1":
            res.encoding = res.apparent_encoding
        page_content = res.text

        page_tree = html.document_fromstring(page_content)
        page_tree = self._convert_links_(page_tree)

        page_content = html.tostring(page_tree, encoding="utf-8")
        return self._cache_file_(page_content)

    def _is_cached_(self, expired=None):
        return PageParse._is_cached_(self, app_setting.html_expired)

    def _convert_links_(self, page_tree):
        """Convert the links in the page's source code.

        Some site use absolute links inside the html, need to change the domain to our's domain.
        For example:
        http://jobbole.com/122277 --> http://our-domain-addr/122277
        http://design.jobbole.com/122277/ --> http://design.our-domain-addr/122277
        http://designjobbole.com/122277/ --> No change here.

        <script async="" src="//www.google-analytics.com/analytics.js"></script>
        <link rel="stylesheet" href="/css/style.css" type="text/css">
        """

        server_domain = app_setting.server_domain
        proxy_domain = app_setting.proxy_domain
        url_links = page_tree.xpath('//a')
        css_links = page_tree.xpath('//link')
        js_links = page_tree.xpath('//script')

        for link in url_links:
            l = link.get("href")
            if l:
                new_l = l.replace(".%s" % proxy_domain, ".%s" % server_domain)
                link.set("href", new_l)

        for link in css_links:
            l = link.get("href")
            if l:
                new_l = l.replace(".%s" % proxy_domain, ".%s" % server_domain)
                link.set("href", new_l)

        for link in js_links:
            l = link.get("src")
            if l:
                new_l = l.replace(".%s" % proxy_domain, ".%s" % server_domain)
                link.set("src", new_l)
        return page_tree


class JSCssParse(PageParse):
    def __init__(self, new_path, suffix, **kwargs):
        PageParse.__init__(self, new_path, suffix, **kwargs)

    def get_content(self):
        res = requests.get(self.url, headers=self.headers)
        if res.status_code != 200:
            # cur_log.warning("Get %s failed!", self.url)
            return "templates/400.html"

        page_content = res.content
        return self._cache_file_(page_content)

    def _is_cached_(self, expired=None):
        return PageParse._is_cached_(self, app_setting.js_css_expired)


class ImageParse(PageParse):
    """Image object, process all the image found in the page."""
    def __init__(self, new_path, suffix, **kwargs):
        PageParse.__init__(self, new_path, suffix, **kwargs)

    def get_content(self):
        res = requests.get(self.url, headers=self.headers)
        if res.status_code != 200:
            # cur_log.warning("Get %s failed!", self.url)
            return "templates/400.html"

        img_content = requests.get(self.url, headers=self.headers, stream=True)
        return self._cache_file_(img_content)

    def _is_cached_(self, expired=None):
        return PageParse._is_cached_(self, app_setting.img_expired)

    def _cache_file_(self, img_content):
        """Save the image file to cache, and return the path of the file.
        """
        if img_content.status_code == 200:
            with open("%s/%s" % (cache_dir, self.file_name), 'wb') as f:
                for chunk in img_content.iter_content(1024):
                    f.write(chunk)

        return self.file_name


class CommonParse(PageParse):
    """Some other pages: such as 'woff' font file."""
    def __init__(self, new_path, suffix, **kwargs):
        PageParse.__init__(self, new_path, suffix, **kwargs)

    def get_content(self):
        try:
            res = requests.get(self.url, headers=self.headers)
        except:
            pass

        if res.status_code != 200:
            return "templates/400.html"
        common_content = requests.get(self.url, headers=self.headers, stream=True)
        return self._cache_file_(common_content)

    def _is_cached_(self, expired=None):
        return PageParse._is_cached_(self, app_setting.common_expired)

    def _cache_file_(self, common_content):
        if common_content.status_code == 200:
            with open("%s/%s" % (cache_dir, self.file_name), 'wb') as f:
                for chunk in common_content.iter_content(1024):
                    f.write(chunk)

        return self.file_name
