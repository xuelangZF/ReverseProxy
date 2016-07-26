#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Last Modified time: 2016-06-07 14:25:27
from ReverseProxy.appfactory import create_app
from flask_script import Manager
app = create_app()
manager = Manager(app)


@manager.command
def test():
    """Run the unit tests.

    $ python manage.py test
    """
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()
