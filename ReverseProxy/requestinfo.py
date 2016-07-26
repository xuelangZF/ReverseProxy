#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Last Modified time: 2016-06-14 13:51:49

"""
Headers get from flask is just as follows, we need to do some process to use in requests.

Cookie: PRUM_EPISODES=s=1465881812146&r=http%3A//localhost%3A5000/t/283982%23reply7;
Content-Length:
User-Agent: ppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36
Connection: keep-alive
Pragma: no-cache
Host: localhost:5000
Upgrade-Insecure-Requests: 1
Cache-Control: no-cache
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4
Content-Type:
Accept-Encoding: gzip, deflate, sdch
"""


def head_convert_to_dict(environ_headers):
    """Get requests.header dict from the environ headers."""
    requests_headers = {"User-Agent": None,
                        }

    for key in requests_headers:
        requests_headers[key] = environ_headers.get(key)

    return requests_headers
