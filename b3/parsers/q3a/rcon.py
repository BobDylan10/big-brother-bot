#
# BigBrotherBot(B3) (www.bigbrotherbot.net)
# Copyright (C) 2005 Michael "ThorN" Thornton
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
#
# CHANGELOG
#
# 2009/12/06 - 1.3.5  - Courgette       - make default socketTimeout 800 ms
#                                       - custom socketTimeout and maxRetries can be specified on a per call basis
# 2009/12/11 - 1.3.6  - Courgette       - make errors warnings until maxRetries is not reached
# 2011/02/01 - 1.3.7  - Bravo17         - added variables for rcon & qserver send & reply strings
# 2011/04/02 - 1.3.8  - Just a baka     - quit command should never be retried
# 2011/04/13 - 1.3.9  - Courgette       - hopefully filter out non ascii characters
# 2011/04/13 - 1.3.10 - Courgette       - should get rid of UnicodeDecodeError
# 2011/04/20 - 1.4    - Courgette       - now sent data is encoded as UTF-8
# 2011/10/30 - 1.5    - xlr8or, Bravo17 - add encoding to QSERVER and RCON snd methods
# 2012/04/04 - 1.5.1  - Courgette       - remove 2 confusing debug msg
# 2012/06/17 - 1.6    - Courgette       - rewrite method writelines so it does not lock until all lines have been
#                                         sent: this allows other commands made by another thread to be sent in
#                                         between commands sent via writelines (and B3 won't appear to be unresponsive)
# 2012/07/18 - 1.6.1  - Courgette       - fix the 'RCON: too much tries' error message when using commands sending
#                                         multiple lines of text
# 2012/11/27 - 1.7    - Courgette       - rollback changes made in 1.6 as it does not solve much (at least with UrT) and
#                                         break some rcon commands with at least cod6
# 2012/12/22 - 1.8    - Courgette       - do not strip data in game server responses
# 2014/04/14 - 1.8.1  - Fenix           - PEP8 coding standards
# 2014/08/02 - 1.9    - Fenix           - syntax cleanup
#                                       - uniform log message format
#
__author__ = 'ThorN'
__version__ = '1.9'

import re
import socket
import select
import time
import thread
import threading
import Queue

from b3.lib.beaker.cache import CacheManager
from b3.lib.beaker.util import parse_cache_config_options


class Rcon(object):

    host = ()
    password = None
    lock = thread.allocate_lock()
    socket = None
    queue = None
    console = None
    socket_timeout = 0.80
    rconsendstring = '\377\377\377\377rcon "%s" %s\n'
    rconreplystring = '\377\377\377\377print\n'
    qserversendstring = '\377\377\377\377%s\n'

    # caching options
    cache_opts = {
        'cache.data_dir': 'b3/cache/data',
        'cache.lock_dir': 'b3/cache/lock',
    }

    # create cache
    cache = CacheManager(**parse_cache_config_options(cache_opts))

    # default expiretime for the status cache in seconds and cache type
    status_cache_expire_time = 2
    status_cache_type = 'memory'

    def __init__(self, console, host, password):
        """
        Object contructor.
        :param console: The console implementation
        :param host: The host where to send RCON commands
        :param password: The RCON password
        """
        self.console = console
        self.queue = Queue.Queue()

        if self.console.config.has_option('caching', 'status_cache_type'):
            self.status_cache_type = self.console.config.get('caching', 'status_cache_type').lower()
            if self.status_cache_type not in ['file', 'memory']:
                self.status_cache_type = 'memory'
        if self.console.config.has_option('caching', 'status_cache_expire'):
            self.status_cache_expire_time = abs(self.console.config.getint('caching', 'status_cache_expire'))
            if self.status_cache_expire_time > 5:
                self.status_cache_expire_time = 5

        self.console.bot('rcon status cache expire time: [%s sec] Type: [%s]' % (self.status_cache_expire_time,
                                                                                 self.status_cache_type))

        self.socket = socket.socket(type=socket.SOCK_DGRAM)
        self.host = host
        self.password = password
        self.socket.settimeout(2)
        self.socket.connect(self.host)

        self._stopEvent = threading.Event()
        thread.start_new_thread(self._writelines, ())

    def encode_data(self, data, source):
        """
        Encode data before sending them onto the socket.
        :param data: The string to be encoded
        :param source: Who requested the encoding
        """
        try:
            if isinstance(data, str):
                data = unicode(data, errors='ignore')
            data = data.encode(self.console.encoding, 'replace')
        except Exception, msg:
            self.console.warning('%s: ERROR encoding data: %r', source, msg)
            data = 'Encoding error'
            
        return data
        
    def send(self, data, maxRetries=None, socketTimeout=None):
        """
        Send data over the socket.
        :param data: The string to be sent
        :param maxRetries: How many times we have to retry the sending upon failure
        :param socketTimeout: The socket timeout value
        """
        if socketTimeout is None:
            socketTimeout = self.socket_timeout
        if maxRetries is None:
            maxRetries = 2

        data = data.strip()
        # encode the data
        if self.console.encoding:
            data = self.encode_data(data, 'QSERVER')

        self.console.verbose('QSERVER sending (%s:%s) %r', self.host[0], self.host[1], data)
        start_time = time.time()

        retries = 0
        while time.time() - start_time < 5:
            readables, writeables, errors = select.select([], [self.socket], [self.socket], socketTimeout)
            if len(errors) > 0:
                self.console.warning('QSERVER: %r', errors)
            elif len(writeables) > 0:
                try:
                    writeables[0].send(self.qserversendstring % data)
                except Exception, msg:
                    self.console.warning('QSERVER: error sending: %r', msg)
                else:
                    try:
                        data = self.readSocket(self.socket, socketTimeout=socketTimeout)
                        self.console.verbose2('QSERVER: received %r' % data)
                        return data
                    except Exception, msg:
                        self.console.warning('QSERVER: error reading: %r', msg)
            else:
                self.console.verbose('QSERVER: no writeable socket')

            time.sleep(0.05)
            retries += 1

            if retries >= maxRetries:
                self.console.error('QSERVER: too much tries: aborting (%r)', data.strip())
                break

            self.console.verbose('QSERVER: retry sending %r (%s/%s)...', data.strip(), retries, maxRetries)

        self.console.debug('QSERVER: did not send any data')
        return ''

    def sendRcon(self, data, maxRetries=None, socketTimeout=None):
        """
        Send an RCON command.
        :param data: The string to be sent
        :param maxRetries: How many times we have to retry the sending upon failure
        :param socketTimeout: The socket timeout value
        """
        if socketTimeout is None:
            socketTimeout = self.socket_timeout
        if maxRetries is None:
            maxRetries = 2

        data = data.strip()
        # encode the data
        if self.console.encoding:
            data = self.encode_data(data, 'RCON')

        self.console.verbose('RCON sending (%s:%s) %r', self.host[0], self.host[1], data)
        start_time = time.time()

        retries = 0
        while time.time() - start_time < 5:
            readables, writeables, errors = select.select([], [self.socket], [self.socket], socketTimeout)

            if len(errors) > 0:
                self.console.warning('RCON: %s', str(errors))
            elif len(writeables) > 0:
                try:
                    writeables[0].send(self.rconsendstring % (self.password, data))
                except Exception, msg:
                    self.console.warning('RCON: error sending: %r', msg)
                else:
                    try:
                        data = self.readSocket(self.socket, socketTimeout=socketTimeout)
                        self.console.verbose2('RCON: received %r' % data)
                        return data
                    except Exception, msg:
                        self.console.warning('RCON: error reading: %r', msg)

                if re.match(r'^quit|map(_rotate)?.*', data):
                    # do not retry quits and map changes since they prevent the server from responding
                    self.console.verbose2('RCON: no retry for %r', data)
                    return ''

            else:
                self.console.verbose('RCON: no writeable socket')

            time.sleep(0.05)

            retries += 1

            if retries >= maxRetries:
                self.console.error('RCON: too much tries: aborting (%r)', data.strip())
                break

            self.console.verbose('RCON: retry sending %r (%s/%s)...', data.strip(), retries, maxRetries)

        self.console.debug('RCON: did not send any data')
        return ''

    def stop(self):
        """
        Stop the rcon writelines queue.
        """
        self._stopEvent.set()

    def _writelines(self):
        """
        Write multiple RCON commands on the socket.
        """
        while not self._stopEvent.isSet():
            lines = self.queue.get(True)
            for cmd in lines:
                if not cmd:
                    continue
                with self.lock:
                    self.sendRcon(cmd, maxRetries=1)

    def writelines(self, lines):
        """
        Enqueue multiple RCON commands for later processing.
        :param lines: A list of RCON commands.
        """
        self.queue.put(lines)

    def write(self, cmd, maxRetries=None, socketTimeout=None, Cached=True):
        """
        Write a RCON command.
        :param cmd: The string to be sent
        :param maxRetries: How many times we have to retry the sending upon failure
        :param socketTimeout: The socket timeout value
        """
        # intercept status request for caching construct
        if cmd == 'status' and Cached:
            status_cache = self.cache.get_cache('status', type=self.status_cache_type,
                                                expire=self.status_cache_expire_time)

            return status_cache.get(key='status', createfunc=self._requestStatusCached)

        with self.lock:
            data = self.sendRcon(cmd, maxRetries=maxRetries)

        return data if data else ''

    def _requestStatusCached(self):
        with self.lock:
            _data = self.sendRcon('status', maxRetries=5)
        if _data:
            return _data
        else:
            return ''

    def flush(self):
        pass

    def readNonBlocking(self, sock):
        """
        Read data from the socket (non blocking).
        :param sock: The socket from where to read data
        """
        sock.settimeout(2)
        start_time = time.time()
        data = ''
        while time.time() - start_time < 1:
            try:
                d = str(sock.recv(4096))
            except socket.error, detail:
                self.console.debug('RCON: error reading: %s' % detail)
                break
            else:
                if d:
                    # remove rcon header
                    data += d.replace(self.rconreplystring, '')
                elif len(data) > 0 and ord(data[-1:]) == 10:
                    break

        return data.strip()

    def readSocket(self, sock, size=4096, socketTimeout=None):
        """
        Read data from the socket.
        :param sock: The socket from where to read data
        :param size: The read size
        :param socketTimeout: The socket timeout value
        """
        if socketTimeout is None:
            socketTimeout = self.socket_timeout

        data = ''
        readables, writeables, errors = select.select([sock], [], [sock], socketTimeout)

        if not len(readables):
            self.console.verbose('no readable socket')
            return ''

        while len(readables):
            d = str(sock.recv(size))

            if d:
                # remove rcon header
                data += d.replace(self.rconreplystring, '')

            readables, writeables, errors = select.select([sock], [], [sock], socketTimeout)
            if len(readables):
                self.console.verbose('RCON: more data to read in socket')

        return data

    def close(self):
        pass

    def getRules(self):
        self.lock.acquire()
        try:
            data = self.send('getstatus')
        finally:
            self.lock.release()
        return data if data else ''

    def getInfo(self):
        self.lock.acquire()
        try:
            data = self.send('getinfo')
        finally:
            self.lock.release()
        return data if data else ''

########################################################################################################################
#
# import sys
#
# if __name__ == '__main__':
#     # To run tests : python b3/parsers/q3a_rcon.py <rcon_ip> <rcon_port> <rcon_password>
#     from b3.fake import fakeConsole
#     r = Rcon(fakeConsole, (sys.argv[1], int(sys.argv[2])), sys.argv[3])
#
#     for cmd in ['say "test1"', 'say "test2"', 'say "test3"', 'say "test4"', 'say "test5"']:
#         fakeConsole.info('Writing %s', cmd)
#         data = r.write(cmd)
#         fakeConsole.info('Received %s', data)
#
#     print '----------------------------------------'
#     for cmd in ['say "test1"', 'say "test2"', 'say "test3"', 'say "test4"', 'say "test5"']:
#         fakeConsole.info('Writing %s', cmd)
#         data = r.write(cmd, socketTimeout=0.45)
#         fakeConsole.info('Received %s', data)
#
#     print '----------------------------------------'
#     for cmd in ['.B3', '.Administrator', '.Admin', 'status', 'sv_mapRotation', 'players']:
#         fakeConsole.info('Writing %s', cmd)
#         data = r.write(cmd)
#         fakeConsole.info('Received %s', data)
#
#     print '----------------------------------------'
#     for cmd in ['.B3', '.Administrator', '.Admin', 'status', 'sv_mapRotation', 'players']:
#         fakeConsole.info('Writing %s', cmd)
#         data = r.write(cmd, socketTimeout=0.55)
#         fakeConsole.info('Received %s', data)
#
#     print '----------------------------------------'
#     fakeConsole.info('getRules')
#     data = r.getRules()
#     fakeConsole.info('Received %s', data)
#
#     print '----------------------------------------'
#     fakeConsole.info('getInfo')
#     data = r.getInfo()
#     fakeConsole.info('Received %s', data)