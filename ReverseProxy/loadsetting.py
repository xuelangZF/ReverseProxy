#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Last Modified time: 2016-06-07 16:27:35

import ConfigParser
import codecs


class Setting(object):
    """The basic class used to load different settings.
    """
    def __init__(self, path):
        self.path = path
        self.cf = ConfigParser.ConfigParser()
        with codecs.open(self.path, 'r', encoding='utf-8') as f:
            self.cf.readfp(f)
        # if not self.cf.read(self.path):
        #     print "No such file %s, load configure failed!  Exit the program immediately." % self.path
        #     exit(-1)

    def _get_(self, section, key, default_val=None):
        if self.cf.has_option(section, key):
            return self.cf.get(section, key)
        else:
            return default_val

    def _getint_(self, section, key, default_val=None):
        if self.cf.has_option(section, key):
            return self.cf.getint(section, key)
        else:
            return default_val


class DomainSetting(Setting):
    """Load configure of flask and the reverse domain.
    """
    def __init__(self, path="setting.conf"):
        Setting.__init__(self, path)
        self.secret_key = self._get_('flask', 'secret_key')

        self.server_domain = self._get_("domain", "server_domain")
        self.server_port = self._getint_('domain', 'server_port') or 5000
        self.proxy_domain = self._get_("domain", "proxy_domain")
        self.proxy_port = self._getint_('domain', 'proxy_port') or 80

        self.html_expired = self._getint_("time", "html_expired")
        self.js_css_expired = self._getint_("time", "js_css_expired")
        self.img_expired = self._getint_("time", "img_expired")
        self.common_expired = self._getint_("time", "common_expired")
