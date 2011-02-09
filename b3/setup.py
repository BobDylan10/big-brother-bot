#!/usr/bin/env python
#
# BigBrotherBot(B3) (www.bigbrotherbot.net)
# Copyright (C) 2009 Mark "xlr8or" Weirath
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
# CHANGELOG:
# 2010/03/21 - 0.2.1 - Courgette
#    * fix bug on config path which showed up only when run as a .exe
# 2010/03/27 - 0.2.2 - xlr8or
#    * minor improvements, added port to db-conn, default value for yes/no in add_plugin()
# 2010/04/17 - 0.3 -Courgette
#    * remove plugin priority related code to follow with parser.py v1.16 changes
# 2010/04/27 - 0.4 - Bakes
#    * added proper BC2 support to the setup wizard.
#    * changed censor and spamcontrol plugins to be added before admin.
#      this means that people who spam or swear in admin commands are
#      warned, rather than the event just being handled in the admin
#      plugin and veto'd elsewhere.
# 2010/10/11 - 0.5 - xlr8or
#    * added MOH support
# 2010/11/07 - 0.5.1 - GrosBedo
#    * edited default messages settings
# 2010/11/07 - 0.5.2 - GrosBedo
#    * added default values of lines_per_second and delay
#    * added more infos about the http access for gamelog
#

__author__  = 'xlr8or'
__version__ = '0.5.2'

import platform, urllib2, shutil, os, sys, time, zipfile
import functions
from distutils import version
from lib.elementtree.SimpleXMLWriter import XMLWriter
from urlparse import urlsplit
from cStringIO import StringIO



class Setup:
    _pver = sys.version.split()[0]
    _indentation = "    "
    _config = "b3/conf/b3.xml"
    _buffer = ''
    _equaLength = 15
    _PBSupportedParsers = ['cod','cod2','cod4','cod5'] #bfbc2 and moh need to be added later when parsers correctly implemented pb. 
    _frostBite = ['bfbc2', 'moh']
 
    def __init__(self, config=None):
        if config:
            self._config = config
        elif self.getB3Path() != "":
            self._config = self.getB3Path() + "\\conf\\b3.xml"
        print self._config
        self.introduction()
        self.clearscreen()
        self._outputFile = self.raw_default("Location and name of the configfile", self._config)
        #Creating Backup
        self.backupFile(self._outputFile)
        self.runSetup()
        raise SystemExit('Restart B3 or reconfigure B3 using option: -s')

    def runSetup(self):
        global xml
        xml = XMLWriter(self._outputFile)

        # write appropriate header
        xml.declaration()
        xml.comment("\n This file is generated by the B3 setup Procedure.\n\
 If you want to regenerate this file and make sure the format is\n\
 correct, you can invoke the setup procedure with the\n\
 command : b3_run -s b3.xml\n\n\
 This is B3 main config file (the one you specify when you run B3 with the\n\
 command : b3_run -c b3.xml)\n\n\
 For any change made in this config file, you have to restart the bot.\n\
 Whenever you can specify a file/directory path, the following shortcuts\n\
 can be used :\n\
  @b3 : the folder where B3 code is installed in\n\
  @conf : the folder containing this config file\n")

        # first level
        configuration = xml.start("configuration")
        xml.data("\n\t")

        # B3 settings
        self.add_buffer('--B3 SETTINGS---------------------------------------------------\n')
        xml.start("settings", name="b3")
        self.add_set("parser", "cod", "Define your game: cod/cod2/cod4/cod5/cod6/iourt41/etpro/wop/smg/bfbc2/moh")
        self.add_set("database", "mysql://b3:password@localhost/b3", "Your database info: [mysql]://[db-user]:[db-password]@[db-server[:port]]/[db-name]")

        self.add_buffer('Testing and Setting Up Database...\n')
        self.executeSql('@b3/sql/b3.sql')

        self.add_set("bot_name", "b3", "Name of the bot")
        self.add_set("bot_prefix", "^0(^2b3^0)^7:", "Ingame messages are prefixed with this code, you can use colorcodes")
        self.add_set("time_format", "%I:%M%p %Z %m/%d/%y")
        self.add_set("time_zone", "CST", "The timezone your bot is in")
        self.add_set("log_level", "9", "How much detail in the logfile: 9 = verbose, 10 = debug, 21 = bot, 22 = console")
        self.add_set("logfile", "b3.log", "Name of the logfile the bot will generate")
        xml.data("\n\t")
        xml.end()
        xml.data("\n\t")
        
        # BFBC2 specific settings
        if self._set_parser == 'bfbc2':
            self.add_buffer('\n--BFBC2 SPECIFIC SETTINGS---------------------------------------\n')
            xml.start("settings", name="bfbc2")
            self.add_set("max_say_line_length", "100", "how long do you want the lines to be restricted to in the chat zone. (maximum length is 100)")
            xml.data("\n\t")
            xml.end()
            xml.data("\n\t")

        # MOH specific settings
        if self._set_parser == 'moh':
            self.add_buffer('\n--MOH SPECIFIC SETTINGS-----------------------------------------\n')
            xml.start("settings", name="moh")
            self.add_set("max_say_line_length", "100", "how long do you want the lines to be restricted to in the chat zone. (maximum length is 100)")
            xml.data("\n\t")
            xml.end()
            xml.data("\n\t")

        # server settings
        self.add_buffer('\n--GAME SERVER SETTINGS------------------------------------------\n')
        xml.start("settings", name="server")
        # Frostbite specific
        if self._set_parser in self._frostBite:
            self.add_set("public_ip", "11.22.33.44", "The IP address of your gameserver")
            self.add_set("port", "", "The port people use to connect to your gameserver")
            self.add_set("rcon_ip", "11.22.33.44", "The IP that the bot uses to send RCON commands. Usually the same as the public_ip")
            self.add_set("rcon_port", "", "The port that the bot uses to send RCON commands. NOT the same as the normal port.")
            self.add_set("rcon_password", "", "The RCON password of your gameserver.")
            self.add_set("timeout", "3", "RCON timeout", silent=True)
        # Q3Aa specific
        else:   
            self.add_set("rcon_password", "", "The RCON pass of your gameserver")
            self.add_set("port", "27960", "The port the server is running on")
            # determine if ftp functionality is available
            if version.LooseVersion(self._pver) < version.LooseVersion('2.6.0'):
                self.add_buffer('\n  NOTE for game_log:\n  You are running python '+self._pver+', ftp functionality\n  is not available prior to python version 2.6.0\n')
            else:
                self.add_buffer('\n  NOTE for game_log:\n  You are running python '+self._pver+', the gamelog may also be\n  ftp-ed or http-ed in.\nDefine game_log like this:\n  ftp://[ftp-user]:[ftp-password]@[ftp-server]/path/to/games_mp.log\nOr for web access (you can use htaccess to secure):\n http://serverhost/path/to/games_mp.log\n')
            self.add_set("game_log", "games_mp.log", "The gameserver generates a logfile, put the path and name here")
            self.add_set("public_ip", "127.0.0.1", "The public IP your gameserver is residing on")
            self.add_set("rcon_ip", "127.0.0.1", "The IP the bot can use to send RCON commands to (127.0.0.1 when on the same box)")

        # determine if PunkBuster is supported
        if self._set_parser in self._PBSupportedParsers:
            self.add_set("punkbuster", "on", "Is the gameserver running PunkBuster Anticheat: on/off")
        else:
            self.add_set("punkbuster", "off", "Is the gameserver running PunkBuster Anticheat: on/off", silent=True)

        # configure default performances parameters
        self.add_set("delay", "0.33", "Delay between each log reading. Set a higher value to consume less disk ressources or bandwidth if you remotely connect (ftp or http remote log access)", silent=True)
        self.add_set("lines_per_second", "50", "Number of lines to process per second. Set a lower value to consume less CPU ressources", silent=True)
        xml.data("\n\t")
        xml.end()
        xml.data("\n\t")

        # autodoc settings
        self.add_buffer('\n--AUTODOC-------------------------------------------------------\n')
        xml.start("settings", name="autodoc")
        xml.data("\n\t\t")
        xml.comment("Autodoc will generate a user documentation for all B3 commands") 
        xml.data("\t\t")
        xml.comment("by default, a html documentation is created in your conf folder")
        self.add_set("type", "html", "html, htmltable or xml")
        self.add_set("maxlevel", "100", "if you want to exclude commands reserved for higher levels")
        self.add_set("destination", "test_doc.html", "Destination can be a file or a ftp url")
        xml.data("\n\t")
        xml.end()
        xml.data("\n\t")

        # messages settings
        self.add_buffer('\n--MESSAGES------------------------------------------------------\n')
        xml.start("settings", name="messages")
        self.add_set("kicked_by", "$clientname^7 was kicked by $adminname^7 $reason")
        self.add_set("kicked", "$clientname^7 was kicked $reason")
        self.add_set("banned_by", "$clientname^7 was banned by $adminname^7 $reason")
        self.add_set("banned", "$clientname^7 was banned $reason")
        self.add_set("temp_banned_by", "$clientname^7 was temp banned by $adminname^7 for $banduration^7 $reason")
        self.add_set("temp_banned", "$clientname^7 was temp banned for $banduration^7 $reason")
        self.add_set("unbanned_by", "$clientname^7 was un-banned by $adminname^7 $reason")
        self.add_set("unbanned", "$clientname^7 was un-banned $reason")
        xml.data("\n\t")
        xml.end()
        xml.data("\n\t")

        # plugins settings
        self.add_buffer('\n--PLUGIN CONFIG PATH--------------------------------------------\n')
        xml.start("settings", name="plugins")
        self.add_set("external_dir", "@b3/extplugins")
        xml.data("\n\t")
        xml.end()
        xml.data("\n\t")

        # plugins
        self.add_buffer('\n--INSTALLING PLUGINS--------------------------------------------\n')
        xml.start("plugins")
        xml.comment("plugin order is important. Plugins that add new in-game commands all depend on the admin plugin. Make sure to have the admin plugin before them.")
        self.add_plugin("censor", "@conf/plugin_censor.xml")
        self.add_plugin("spamcontrol", "@conf/plugin_spamcontrol.xml")
        self.add_plugin("admin", "@conf/plugin_admin.xml", explanation="the admin plugin is compulsory.", prompt=False)
        self.add_plugin("tk", "@conf/plugin_tk.xml")
        self.add_plugin("stats", "@conf/plugin_stats.xml")
        self.add_plugin("pingwatch", "@conf/plugin_pingwatch.xml")
        self.add_plugin("adv", "@conf/plugin_adv.xml")
        self.add_plugin("status", "@conf/plugin_status.xml")
        self.add_plugin("welcome", "@conf/plugin_welcome.xml")
        if self._set_punkbuster == "on":
            self.add_plugin("punkbuster", "@conf/plugin_punkbuster.xml")
            xml.data("\n\t\t")
        else:
            xml.data("\n\t\t")
            xml.comment("The punkbuster plugin was not installed since punkbuster is not supported or disabled.")
            xml.data("\t\t")

        # ext plugins
        xml.comment("The next plugins are external, 3rd party plugins and should reside in the external_dir. Example:")
        xml.data("\t\t")
        xml.comment("plugin config=\"@b3/extplugins/conf/newplugin.xml\" name=\"newplugin\"")
        result = self.add_plugin("xlrstats", self._set_external_dir+"/conf/xlrstats.xml", default="no")
        if result:
            self.executeSql('@b3/sql/xlrstats.sql')

        #self.add_plugin("registered", self._set_external_dir+"/conf/plugin_registered.xml", "Trying to download Registered", "http://www.bigbrotherbot.net/forums/downloads/?sa=downfile&id=22")
        #self.add_plugin("countryfilter", self._set_external_dir+"/conf/countryfilter.xml", "Trying to download Countryfilter", "http://github.com/xlr8or/b3-plugin-countryfilter/zipball/master")

        # final comments
        xml.data("\n\t\t")
        xml.comment("You can add new/custom plugins to this list using the same form as above.")
        xml.data("\t")
        xml.end()

        xml.data("\n")
        xml.close(configuration)
        self.add_buffer('\n--FINISHED CONFIGURATION----------------------------------------\n')

    def add_explanation(self, etext):
        _prechar = "> "
        print _prechar+etext

    def add_buffer(self, addition, autowrite=True):
        self._buffer += addition
        if autowrite:
            self.writebuffer()

    def writebuffer(self):
        self.clearscreen()
        print self._buffer

    def equaLize(self, _string):
        return (self._equaLength-len(str(_string)))*" "

    def add_set(self, sname, sdflt, explanation="", silent=False):
        """
        A routine to add a setting with a textnode to the config
        Usage: self.add_set(name, default value optional-explanation)
        """
        xml.data("\n\t\t")
        if explanation != "":
            self.add_explanation(explanation)
            xml.comment(explanation)
            xml.data("\t\t")
        if not silent:
            _value = self.raw_default(sname, sdflt)
        else:
            _value = sdflt
        xml.element("set", _value, name=sname)
        #store values into a variable for later use ie. enabling the punkbuster plugin.
        exec("self._set_"+str(sname)+" = \""+str(_value)+"\"")
        if not silent:
            self.add_buffer(str(sname)+self.equaLize(sname)+": "+str(_value)+"\n")

    def add_plugin(self, sname, sconfig, explanation=None, default="yes", downlURL=None, prompt=True):
        """
        A routine to add a plugin to the config
        Usage: self.add_plugin(pluginname, default-configfile, optional-explanation, optional-downloadlocation, optional-prompt)
        """
        if prompt:
            _q = "Install "+sname+" plugin? (yes/no)"
            _test = self.raw_default(_q, default)
            if _test != "yes":
                return False

        if downlURL:
            self.download(downlURL)

        if explanation:
            self.add_explanation(explanation)
        _config = self.raw_default("config", sconfig)
        xml.data("\n\t\t")
        xml.element("plugin", name=sname, config=_config)
        self.add_buffer("plugin: "+str(sname)+", config: "+str(_config)+"\n")
        return True

    def raw_default(self, prompt, dflt=None):
        if dflt: 
            prompt = "%s [%s]" % (prompt, dflt)
        else:
            prompt = "%s" % (prompt)
        res = raw_input(prompt+self.equaLize(prompt)+": ")
        if not res and dflt:
            res = dflt
        if res == "":
            print "ERROR: No value was entered! Give it another try!"
            res = self.raw_default(prompt, dflt)
        self.testExit(res)
        return res         

    def clearscreen(self):
        if platform.system() in ('Windows', 'Microsoft'):
            os.system('cls')
        else:
            os.system('clear')

    def backupFile(self, _file):
        print "\n--BACKUP/CREATE CONFIGFILE--------------------------------------\n"
        print "    Trying to backup the original "+_file+"..."
        if not os.path.exists(_file):
            print "\n    No backup needed.\n    A file with this location/name does not yet exist,\n    I'm about to generate a new config file!\n"
            self.testExit()
        else:
            try:
                _stamp = time.strftime("-%d_%b_%Y_%H.%M.%S", time.gmtime())
                _fname = _file+_stamp+".xml"
                shutil.copy(_file, _fname)
                print "    Backup success, "+_file+" copied to : %s" % _fname
                print "    If you need to abort setup, you can restore by renaming the backup file."
                self.testExit()
            except OSError, why:
                print "\n    Error : %s\n" % str(why)
                self.testExit()

    def introduction(self):
        try:
            _uname = platform.uname()[1]+", "
        except:
            _uname = "admin, "
        self.clearscreen()
        print "    WELCOME "+_uname+"TO THE B3 SETUP PROCEDURE"
        print "----------------------------------------------------------------"
        print "We're about to generate a main configuration file for "
        print "BigBrotherBot. This procedure is initiated when:\n"
        print " 1. you run B3 with the option --setup or -s"
        print " 2. the config you're trying to run does not exist"
        print "    ("+self._config+")"
        print " 3. you did not modify the distributed b3.xml prior to"
        print "    starting B3."
        self.testExit()
        print "We will prompt you for each setting. We'll also provide default"
        print "values inside [] if applicable. When you want to accept a"
        print "default value you will only need to press Enter."
        print ""
        print "If you make an error at any stage, you can abort the setup"
        print "procedure by typing \'abort\' at the prompt. You can start"
        print "over by running B3 with the setup option: python b3_run.py -s"
        self.testExit()
        print "First you will be prompted for a location and name for this"
        print "configuration file. This is for multiple server setups, or"
        print "if you want to run B3 from a different setup file for your own."
        print "reasons. In a basic single instance install you will not have to"
        print "change this location and/or name. If a configuration file exists"
        print "we will make a backup first and tag it with date and time, so"
        print "you can always revert to a previous version of the config file."
        print ""
        print "This procedure is new, bugs may be reported on our forums at"
        print "www.bigbrotherbot.net"
        self.testExit(_question='[Enter] to continue to generate the configfile...')

    def testExit(self, _key='', _question='[Enter] to continue, \'abort\' to abort Setup: ', _exitmessage='Setup aborted, run python b3_run.py -s to restart the procedure.'):
        if _key == '':
            _key = raw_input('\n'+_question)
        if _key != 'abort':
            print "\n"
            return
        else:
            raise SystemExit(_exitmessage)

    def connectToDatabase(self):
        _db = None
        _dsnDict = functions.splitDSN(self._set_database)
        if _dsnDict['protocol'] == 'mysql':
            try:
                import MySQLdb
                _db = MySQLdb.connect(host=_dsnDict['host'], port=_dsnDict['port'], user=_dsnDict['user'], passwd=_dsnDict['password'], db=_dsnDict['path'][1:])
            except ImportError:
                self.add_buffer("You need to install python-mysqldb. Look for 'dependencies' in B3 documentation.\n")
                raise SystemExit()
            except Exception:
                _db.close()
                pass
        else:
            self.add_buffer("%s protocol is not supported. Use mysql instead\n" % _dsnDict['protocol'])
            self.testExit(_question='Do you still want to continue? [Enter] to continue, \'abort\' to abort Setup: ')
        return _db

    def executeSql(self, file):
        """This method executes an external sql file on the current database"""
        self.db = self.connectToDatabase()
        if self.db:
            self.add_buffer('Connected to the database. Installing the tables when they don\'t exist.\n')
            sqlFile = self.getAbsolutePath(file)
            if os.path.exists(sqlFile):
                f = open(sqlFile, 'r')
                sql_text = f.read()
                f.close()
                sql_statements = sql_text.split(';')
                for s in sql_statements:
                    try:
                        self.db.query(s)
                    except:
                        pass
            else:
                raise Exception('sqlFile does not exist: %s' %sqlFile)
            self.db.close()
        else:
            self.add_buffer('Connection to the database failed. Check the documentation how to add the database tables manually.\n')
            self.testExit(_question='Do you still want to continue? [Enter] to continue, \'abort\' to abort Setup: ')
        return None

    def getB3Path(self):
        if functions.main_is_frozen():
            # which happens when running from the py2exe build
            return os.path.dirname(sys.executable)
        return ""

    def getAbsolutePath(self, path):
        """Return an absolute path name and expand the user prefix (~)"""
        if path[0:4] == '@b3/':
            path = os.path.join(self.getB3Path(), path[4:])
        return os.path.normpath(os.path.expanduser(path))

    def url2name(self, url):
        return os.path.basename(urlsplit(url)[2])
    
    def download(self, url, localFileName = None):
        absPath = self.getAbsolutePath(self._set_external_dir)
        localName = self.url2name(url)
        req = urllib2.Request(url)
        try:
            r = urllib2.urlopen(req)
        except Exception, msg:
            print('Download failed: %s' % msg)
        if r.info().has_key('Content-Disposition'):
            # If the response has Content-Disposition, we take file name from it
            localName = r.info()['Content-Disposition'].split('filename=')[1]
            if localName[0] == '"' or localName[0] == "'":
                localName = localName[1:-1]
        elif r.url != url: 
            # if we were redirected, the real file name we take from the final URL
            localName = self.url2name(r.url)
        if localFileName: 
            # we can force to save the file as specified name
            localName = localFileName
        packageLocation = absPath+"/packages/"
        localName = absPath+"/packages/"+localName
        if not os.path.isdir( packageLocation ):
            os.mkdir( packageLocation )
        f = open(localName, 'wb')
        f.write(r.read())
        f.close()
        self.extract(localName, absPath)
        #self.extract(localName, packageLocation)
    
    def extract(self, filename, dir):
        zf = zipfile.ZipFile( filename )
        namelist = zf.namelist()
        dirlist = filter( lambda x: x.endswith( '/' ), namelist )
        filelist = filter( lambda x: not x.endswith( '/' ), namelist )
        # make base
        pushd = os.getcwd()
        if not os.path.isdir( dir ):
            os.mkdir( dir )
        os.chdir( dir )
        # create directory structure
        dirlist.sort()
        for dirs in dirlist:
            dirs = dirs.split( '/' )
            prefix = ''
            for dir in dirs:
                dirname = os.path.join( prefix, dir )
                if dir and not os.path.isdir( dirname ):
                    os.mkdir( dirname )
                prefix = dirname
        # extract files
        for fn in filelist:
            try:
                out = open( fn, 'wb' )
                buffer = StringIO( zf.read( fn ))
                buflen = 2 ** 20
                datum = buffer.read( buflen )
                while datum:
                    out.write( datum )
                    datum = buffer.read( buflen )
                out.close()
            finally:
                print fn
        os.chdir( pushd )



if __name__ == '__main__':
    #from b3.fake import fakeConsole
    #from b3.fake import joe
    #from b3.fake import simon
    
    Setup('test.xml')
