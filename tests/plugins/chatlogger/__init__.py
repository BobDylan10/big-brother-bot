# BigBrotherBot(B3) (www.bigbrotherbot.net)
# Copyright (C) 2012 Thomas LEVEIL <courgette@bigbrotherbot.net>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA


import time
import unittest2 as unittest
import threading
import sys

from mockito import when, unstub
from mock import Mock
from b3.config import XmlConfigParser
from b3.plugins.admin import AdminPlugin
from tests import logging_disabled

testcase_lock = threading.Lock() # together with flush_console_streams, helps getting logging output related to the correct
# test in test runners such as the one in PyCharm IDE.


def flush_console_streams():
    sys.stderr.flush()
    sys.stdout.flush()


def cleanUp():
    unstub()
    flush_console_streams()
    testcase_lock.release()


class ChatloggerTestCase(unittest.TestCase):

    def setUp(self):
        testcase_lock.acquire()
        self.addCleanup(cleanUp)
        flush_console_streams()
        # create a FakeConsole parser
        self.parser_conf = XmlConfigParser()
        self.parser_conf.loadFromString(r"""<configuration/>""")
        with logging_disabled():
            from b3.fake import FakeConsole
            self.console = FakeConsole(self.parser_conf)

        with logging_disabled():
            self.adminPlugin = AdminPlugin(self.console, '@b3/conf/plugin_admin.ini')
            self.adminPlugin.onStartup()

        # make sure the admin plugin obtained by other plugins is our admin plugin
        when(self.console).getPlugin('admin').thenReturn(self.adminPlugin)

        self.console.screen = Mock()
        self.console.time = time.time
        self.console.upTime = Mock(return_value=3)

    def tearDown(self):
        try:
            self.console.storage.shutdown()
        except:
            pass