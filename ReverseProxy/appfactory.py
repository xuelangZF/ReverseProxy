#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Last Modified time: 2016-06-06 09:26:32

from flask import Flask, render_template, request
from flask import send_from_directory
from .getpage import PageManagement
from .requestinfo import head_convert_to_dict
from .urlprocess import replace_domain, remove_anchor, replace_sub_domain
from . import app_setting, cache_dir


def create_app():
    app = Flask(__name__, static_folder=None)
    app.config['SECRET_KEY'] = app_setting.secret_key
    app.config["SERVER_NAME"] = "%s:%s" % (app_setting.server_domain, app_setting.server_port)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    @app.route('/', defaults={'url': ''})
    @app.route('/<path:url>')
    def general_page(url=None):
        replace_d = replace_domain(request.url, app_setting.proxy_domain, app_setting.proxy_port)
        new_path = remove_anchor(replace_d)

        page = PageManagement.get_page_obj(new_path,
                                           headers=head_convert_to_dict(request.headers),
                                           url=request.url)

        return send_from_directory(cache_dir, str(page))

    @app.route("/", subdomain="<sub>")
    @app.route("/<path:p>", subdomain="<sub>")
    def sub_domain_page(sub, p=None):
        replace_d = replace_sub_domain(request.url, app_setting.proxy_domain, app_setting.proxy_port)
        new_path = remove_anchor(replace_d)

        page = PageManagement.get_page_obj(new_path,
                                           headers=head_convert_to_dict(request.headers),
                                           url=request.url)
        return send_from_directory(cache_dir, str(page))

    return app
