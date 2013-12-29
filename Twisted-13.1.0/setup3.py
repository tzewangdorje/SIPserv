#!/usr/bin/env python3.3

# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

# This is a temporary helper to be able to build and install distributions of
# Twisted on/for Python 3.  Once all of Twisted has been ported, it should go
# away and setup.py should work for either Python 2 or Python 3.

from __future__ import division, absolute_import

import sys


# A list of modules that have been ported, e.g. "twisted.python.versions"; a
# package name (e.g. "twisted.python") indicates the corresponding __init__.py
# file has been ported (e.g. "twisted/python/__init__.py"). To reduce merge
# conflicts, add new lines in alphabetical sort.
modules = [
    "twisted",
    "twisted.copyright",
    "twisted.internet",
    "twisted.internet.abstract",
    "twisted.internet.address",
    "twisted.internet.base",
    "twisted.internet.default",
    "twisted.internet.defer",
    "twisted.internet.endpoints",
    "twisted.internet.epollreactor",
    "twisted.internet.error",
    "twisted.internet.interfaces",
    "twisted.internet.fdesc",
    "twisted.internet.gireactor",
    "twisted.internet._glibbase",
    "twisted.internet.gtk3reactor",
    "twisted.internet.main",
    "twisted.internet._newtls",
    "twisted.internet.posixbase",
    "twisted.internet.protocol",
    "twisted.internet.pollreactor",
    "twisted.internet.reactor",
    "twisted.internet.selectreactor",
    "twisted.internet._signals",
    "twisted.internet.ssl",
    "twisted.internet.task",
    "twisted.internet.tcp",
    "twisted.internet.test",
    "twisted.internet.test.connectionmixins",
    "twisted.internet.test.modulehelpers",
    "twisted.internet.test._posixifaces",
    "twisted.internet.test.reactormixins",
    "twisted.internet.threads",
    "twisted.internet.udp",
    "twisted.internet.util",
    "twisted.names",
    "twisted.names.cache",
    "twisted.names.client",
    "twisted.names.common",
    "twisted.names.dns",
    "twisted.names.error",
    "twisted.names.hosts",
    "twisted.names.resolve",
    "twisted.names.test",
    "twisted.names._version",
    "twisted.protocols",
    "twisted.protocols.basic",
    "twisted.protocols.policies",
    "twisted.protocols.test",
    "twisted.protocols.tls",
    "twisted.python",
    "twisted.python.compat",
    "twisted.python.components",
    "twisted.python.context",
    "twisted.python.deprecate",
    "twisted.python.failure",
    "twisted.python.filepath",
    "twisted.python.log",
    "twisted.python.monkey",
    "twisted.python.randbytes",
    "twisted.python._reflectpy3",
    "twisted.python.runtime",
    "twisted.python.test",
    "twisted.python.test.deprecatedattributes",
    "twisted.python.test.modules_helpers",
    "twisted.python.threadable",
    "twisted.python.threadpool",
    "twisted.python.util",
    "twisted.python.versions",
    "twisted.test",
    "twisted.test.proto_helpers",
    "twisted.test.ssl_helpers",
    "twisted.trial",
    "twisted.trial._asynctest",
    "twisted.trial.itrial",
    "twisted.trial._synctest",
    "twisted.trial.test",
    "twisted.trial.test.detests",
    "twisted.trial.test.erroneous",
    "twisted.trial.test.suppression",
    "twisted.trial.test.packages",
    "twisted.trial.test.skipping",
    "twisted.trial.test.suppression",
    "twisted.trial.unittest",
    "twisted.trial.util",
    "twisted._version",
    "twisted.web",
    "twisted.web.http_headers",
    "twisted.web.resource",
    "twisted.web._responses",
    "twisted.web.test",
    "twisted.web.test.requesthelper",
    "twisted.web._version",
]



# A list of test modules that have been ported, e.g
# "twisted.python.test.test_versions". To reduce merge conflicts, add new
# lines in alphabetical sort.
testModules = [
    "twisted.internet.test.test_abstract",
    "twisted.internet.test.test_address",
    "twisted.internet.test.test_base",
    "twisted.internet.test.test_core",
    "twisted.internet.test.test_default",
    "twisted.internet.test.test_endpoints",
    "twisted.internet.test.test_epollreactor",
    "twisted.internet.test.test_fdset",
    "twisted.internet.test.test_filedescriptor",
    "twisted.internet.test.test_inlinecb",
    "twisted.internet.test.test_gireactor",
    "twisted.internet.test.test_glibbase",
    "twisted.internet.test.test_main",
    "twisted.internet.test.test_newtls",
    "twisted.internet.test.test_posixbase",
    "twisted.internet.test.test_protocol",
    "twisted.internet.test.test_sigchld",
    "twisted.internet.test.test_tcp",
    "twisted.internet.test.test_threads",
    "twisted.internet.test.test_tls",
    "twisted.internet.test.test_udp",
    "twisted.internet.test.test_udp_internals",
    "twisted.names.test.test_cache",
    "twisted.names.test.test_client",
    "twisted.names.test.test_common",
    "twisted.names.test.test_dns",
    "twisted.names.test.test_hosts",
    "twisted.protocols.test.test_basic",
    "twisted.protocols.test.test_tls",
    "twisted.python.test.test_components",
    "twisted.python.test.test_deprecate",
    "twisted.python.test.test_reflectpy3",
    "twisted.python.test.test_runtime",
    "twisted.python.test.test_util",
    "twisted.python.test.test_versions",
    "twisted.test.test_abstract",
    "twisted.test.test_compat",
    "twisted.test.test_context",
    "twisted.test.test_cooperator",
    "twisted.test.test_defer",
    "twisted.test.test_defgen",
    "twisted.test.test_error",
    "twisted.test.test_factories",
    "twisted.test.test_failure",
    "twisted.test.test_fdesc",
    "twisted.test.test_internet",
    "twisted.test.test_iutils",
    "twisted.test.test_log",
    "twisted.test.test_loopback",
    "twisted.test.test_monkey",
    "twisted.test.test_paths",
    "twisted.test.test_policies",
    "twisted.test.test_randbytes",
    "twisted.test.test_setup",
    "twisted.test.test_ssl",
    "twisted.test.test_sslverify",
    "twisted.test.test_task",
    "twisted.test.test_tcp",
    "twisted.test.test_tcp_internals",
    "twisted.test.test_threadable",
    "twisted.test.test_threads",
    "twisted.test.test_twisted",
    "twisted.test.test_threadpool",
    "twisted.test.test_udp",
    "twisted.trial.test.test_assertions",
    "twisted.trial.test.test_asyncassertions",
    "twisted.trial.test.test_deferred",
    "twisted.trial.test.test_pyunitcompat",
    "twisted.trial.test.test_suppression",
    "twisted.trial.test.test_testcase",
    "twisted.trial.test.test_tests",
    "twisted.trial.test.test_util",
    "twisted.trial.test.test_warning",
    # downloadPage tests weren't ported:
    "twisted.web.test.test_webclient",
    "twisted.web.test.test_http",
    "twisted.web.test.test_http_headers",
    "twisted.web.test.test_resource",
    "twisted.web.test.test_web",
]



# A list of any other modules which are needed by any of the modules in the
# other two lists, but which themselves have not actually been properly ported
# to Python 3.  These modules might work well enough to satisfy some of the
# requirements of the modules that depend on them, but cannot be considered
# generally usable otherwise.
almostModules = [
    # Missing test coverage, see #6156:
    "twisted.internet._sslverify",
    # twisted.names.client semi-depends on twisted.names.root, but only on
    # Windows really:
    "twisted.names.root",
    # Missing test coverage:
    "twisted.protocols.loopback",
    # Minimally used by setup3.py:
    "twisted.python.dist",
    # twisted.python.filepath depends on twisted.python.win32, but on Linux it
    # only really needs to import:
    "twisted.python.win32",
    "twisted.test.reflect_helper_IE",
    "twisted.test.reflect_helper_VE",
    "twisted.test.reflect_helper_ZDE",
    # Required by some of the ported trial tests:
    "twisted.trial.reporter",
    # Agent code and downloadPage aren't ported, test coverage isn't complete:
    "twisted.web.client",
    # twisted.web.resource depends on twisted.web.error, so it is sorta
    # ported, but its tests are not yet ported, so it probably doesn't
    # completely work.
    "twisted.web.error",
    # Required by twisted.web.server, no actual code here:
    "twisted.web.iweb",
    # Required by twisted.web.server for an error handling case:
    "twisted.web.html",
    # This module has a lot of missing test coverage.  What tests it has pass,
    # but it needs a lot more.  It was ported only enough to make the client
    # work.
    "twisted.web.http",
    # GzipEncoder and allowed methods functionality not ported, no doubt
    # missing lots of test coverage:
    "twisted.web.server",
]



if __name__ == "__main__":
    sys.path.insert(0, '.')

    from distutils.core import setup

    from twisted.python.dist import STATIC_PACKAGE_METADATA

    args = STATIC_PACKAGE_METADATA.copy()
    args['classifiers'] = ["Programming Language :: Python :: 3.3"]
    args['py_modules'] = modules + testModules + almostModules

    if 'sdist' in sys.argv:
        args['data_files'] = [('admin', ['admin/run-python3-tests'])]

    setup(**args)
