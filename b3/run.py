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
# 2010/02/24 - 1.2   - Courgette - uniformize SystemExit and uncatched exception handling between bot running
#                                  as a win32 standalone and running as a python script
# 2010/03/20 - 1.3   - xlr8or    - finished options -s --setup and -n, --nosetup where setup launches setup
#                                  procedure and nosetup prevents bot from entering setup procedure.
# 2010/08/05 - 1.3.1 - xlr8or    - fixing broken --restart mode
# 2010/10/22 - 1.3.3 - xlr8or    - restart counter
# 2011/05/19 - 1.4.0 - xlr8or    - added --update -u arg
# 2011/12/03 - 1.4.1 - Courgette - fix crash at bot start in restart mode when installed from egg
# 2014/07/21 - 1.5   - Fenix     - syntax cleanup
# 2014/12/15 - 1.5.1 - Fenix     - let the parser know if we are running B3 in auto-restart mode or not
# 2015/02/02 - 1.5.2 - Fenix     - keep looking for xml configuration files if ini/cfg are not found
# 2015/02/14 - 1.5.3 - Fenix     - removed _check_arg_configfile in favor of configuration file lookup
# 2015/05/07 - 1.6   - Fenix     - add GUI startup

__author__  = 'ThorN'
__version__ = '1.6'

import b3
import os
import sys
import pkg_handler
import time
import traceback

from b3.functions import main_is_frozen
from b3.setup import Setup
from b3.setup import Update

import argparse

modulePath = pkg_handler.resource_directory(__name__)


def run_autorestart(args=None):
    """
    Run B3 in auto-restart mode.
    """
    _restarts = 0

    if main_is_frozen():
        script = ''
    else:
        script = os.path.join(modulePath[:-3], 'b3_run.py')
        if not os.path.isfile(script):
            # must be running from the egg
            script = os.path.join(modulePath[:-3], 'b3', 'run.py')
        if os.path.isfile(script + 'c'):
            script += 'c'

    if args:
        script = '%s %s %s --console --autorestart' % (sys.executable, script, ' '.join(args))
    else:
        script = '%s %s --console --autorestart' % (sys.executable, script)

    while True:
        try:
            print 'Running in auto-restart mode...'
            if _restarts > 0:
                print 'Bot restarted %s times.' %_restarts
            time.sleep(1)

            try:
                import subprocess
                status = subprocess.call(script, shell=True)
            except ImportError:
                subprocess = None  # just to remove warnings
                print 'Restart mode not fully supported!\n' \
                      'Use B3 without the -r (--restart) option or update your python installation!'
                break

            print 'Exited with status %s' % status

            if status == 221:
                # restart
                print 'Restart requested...'
            elif status == 222:
                # stop
                print 'Shutdown requested.'
                break
            elif status == 220:
                # stop
                print 'B3 Error, check log file.'
                break
            elif status == 223:
                # stop
                print 'B3 Error Restart, check log file.'
                break
            elif status == 224:
                # stop
                print 'B3 Error, check console.'
                break
            elif status == 256:
                # stop
                print 'Python error, stopping, check log file.'
                break
            elif status == 0:
                # stop
                print 'Normal shutdown, stopping.'
                break
            elif status == 1:
                # stop
                print 'Error, stopping, check console.'
                break
            else:
                print 'Unknown shutdown status (%s), restarting...' % status
        
            _restarts += 1
            time.sleep(4)
        except KeyboardInterrupt:
            print 'Quit'
            break


def run(config=None, nosetup=False, autorestart=False):
    """
    Run B3.
    :param config: The B3 configuration file instance
    :param nosetup: Whether to execute the B3 setup or not
    :param autorestart: Whether to run B3 in autorestart mode or not
    """
    if config:
        config = b3.getAbsolutePath(config)
    else:
        for p in ('b3.%s', 'conf/b3.%s', 'b3/conf/b3.%s', '~/b3.%s', '~/conf/b3.%s', '~/b3/conf/b3.%s', '@b3/conf/b3.%s'):
            for e in ('ini', 'cfg', 'xml'):
                path = b3.getAbsolutePath(p % e)
                print 'Searching for config file: %s' % path
                if os.path.isfile(path):
                    config = path
                    break

    if not config:
        # This happens when no config was specified on the
        # commandline and the default configs are missing!
        if nosetup:
            raise SystemExit('ERROR: could not find config file: please run B3 with option: --setup or -s')
        else:
            Setup(config)

    b3.start(config, nosetup, autorestart)


def run_setup(config=None):
    """
    Run the B3 setup.
    :param config: The B3 configuration file instance
    """
    Setup(config)


def run_update(config=None):
    """
    Run the B3 update.
    :param config: The B3 configuration file instance
    """
    Update(config)


def run_gui(options):
    """
    Run B3 graphical user interface.
    Will raise an exception if the GUI cannot be initialized so we can fallback into console mode.
    :param options: command line options
    """
    from b3.gui import B3App
    from b3.gui import SplashScreen
    from b3.gui import MessageBox
    from b3.gui import Button

    if options.console:
        raise EnvironmentError

    # initialize outside try/except so if PyQT5 is not avaiable or there is
    # no display adapter available, this will raise an exception and we can
    # fallback into console mode
    app = B3App.Instance(sys.argv)

    try:
        with SplashScreen(min_splash_time=0):
            app.init()
    except Exception, e:
        box = MessageBox(icon=MessageBox.Critical)
        box.setWindowTitle('CRITICAL')
        box.setText(e.message)
        box.addButton(Button(text='Ok'), MessageBox.AcceptRole)
        box.exec_()
        sys.exit(127)
    else:
        sys.exit(app.exec_())


def run_console(options):
    """
    Run B3 in console mode.
    :param options: command line options
    """
    try:
        run(config=options.config, nosetup=options.nosetup, autorestart=options.autorestart)
    except SystemExit, msg:
        if main_is_frozen():
            if sys.stdout != sys.__stdout__:
                sys.stdout = sys.__stdout__
                sys.stderr = sys.__stderr__
            print msg
            raw_input("press any key to continue...")
        raise
    except:
        if sys.stdout != sys.__stdout__:
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__
        traceback.print_exc()
    if main_is_frozen():
        if sys.stdout != sys.__stdout__:
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__
        raw_input("press any key to continue...")


def main():
    """
    Main execution.
    """
    p = argparse.ArgumentParser()
    p.add_argument('-c', '--config', dest='config', default=None, metavar='b3.ini', help='B3 config file. Example: -c b3.ini')
    p.add_argument('-x', '--console', action='store_true', dest='console', default=False, help='Force B3 execution in console mode')
    p.add_argument('-r', '--restart', action='store_true', dest='restart', default=False, help='Auto-restart B3 on crash')
    p.add_argument('-s', '--setup',  action='store_true', dest='setup', default=False, help='Setup main b3.ini config file')
    p.add_argument('-n', '--nosetup', action="store_true", dest='nosetup', default=False, help='Do not enter setup mode when config is missing')
    p.add_argument('-u', '--update', action='store_true', dest='update', default=False, help='Update B3 database to latest version')
    p.add_argument('-v', '--version', action='version', default=False, version=b3.getB3versionString(), help='Show B3 version and exit')
    p.add_argument('-a', '--autorestart', action='store_true', dest='autorestart', default=False, help=argparse.SUPPRESS)

    (options, args) = p.parse_known_args()

    if not options.config and len(args) == 1:
        options.config = args[0]

    if options.setup:
        run_setup(config=options.config)

    if options.update:
        run_update(config=options.config)

    if options.restart:
        if options.config:
            run_autorestart(['--config', options.config] + args)
        else:
            run_autorestart([])
    else:
        try:
            run_gui(options)
        except Exception:
            run_console(options)

    
if __name__ == '__main__':
    main()