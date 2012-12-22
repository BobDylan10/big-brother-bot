#
# BigBrotherBot(B3) (www.bigbrotherbot.net)
# Copyright (C) 2005 Michael "ThorN" Thornton
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

#   CHANGELOG
#   18/10/2011 - 1.0.3 - Bravo17
#    Check slot number go up in order in getplayerlist to weed out data errors
#   22/12/2012 - 1.1 - Courgette
#    fix regex for parsing PB_SV_PList results for cases where a player has no power
#
__author__  = 'ThorN'
__version__ = '1.1'

import re

#--------------------------------------------------------------------------------------------------
class PunkBuster(object):
    console = None

#    : Player List: [Slot #] [GUID] [Address] [Status] [Power] [Auth Rate] [Recent SS] [O/S] [Name]
#    : 4  27b26543216546163546513465135135(-) 111.11.1.11:28960 OK   1 3.0 0 (W) "ShyRat"
#    : 5 387852749658574858598854913cdf11(-) 222.222.222.222:28960 OK   10.0 0 (W) "shatgun"
#    : 6 9732d328485274156125252141252ba1(-) 33.133.3.133:-28960 OK   1 5.0 0 (W) "FATTYBMBLATY"
    regPlayer = re.compile(r"""
^.*?:\s+
	(?P<slot>[0-9]+)\s+                     # slot
	(?P<pbid>[a-z0-9]+)\s?\([^>)]+\)\s      # PB id
	(?P<ip>[0-9.:]+):(?P<port>[0-9-]+)\s    # IP:port
	(?P<status>[a-z]+)\s+                   # status
	(?:(?P<power>[0-9]+)\s+)?               # power (may be missing)
	(?P<auth>[0-9.]+)\s                     # auth rate
	(?P<ss>[0-9]+)(\{[^}]+\})?\s+           # recent SS
	\((?P<os>[^)]+)\)\s+                    # O/S
	"?(?P<name>[^"]+)"?                     # name
$
""", re.IGNORECASE|re.VERBOSE)


    def __init__(self, console):
        self.console = console

    def send(self, command):
        return self.console.write(command)

    def badName(self, grace, filter):
        """
        PB_SV_BadName [grace_seconds] [text_filter]
        Adds a bad name to the list of bad names for the server to disallow in player names
        """
        return self.send('PB_SV_BadName "%s" "%s"' % (grace, filter))


    def badNameDel(self, slot):
        """
        PB_SV_BadNameDel [slot #]
        Deletes a bad name from the list of bad names 
        """
        return self.send('PB_SV_BadNameDel "%s"' % slot)

    def ban(self, client, reason='', private=''):
        """
        PB_SV_Ban [name or slot #] [displayed_reason] | [optional_private_reason]
        Removes a player from the game and permanently bans that player from the server based
        on the player's guid (based on the cdkey); the ban is logged and also written to the
        pbbans.dat file in the pb folder 
        """

        if client.cid and client.connected:
            return self.send('PB_SV_Ban "%s" "%s" "%s"' % (int(client.cid) + 1, reason, private))
        else:
            return self.banGUID(client, reason)

    def banGUID(self, client, reason=''):
        """
        PB_SV_BanGuid [guid] [player_name] [IP_Address] [reason]
        Adds a guid directly to PB's permanent ban list; if the player_name or IP_Address
        are not known, we recommend using "???" 
        """

        if not client.pbid:
            return False

        return self.send('PB_SV_BanGuid "%s" "%s" "%s" "%s"' % (client.pbid, client.name, client.ip, reason))

    def kick(self, client, minutes=1, reason='', private=''):
        """
        PB_SV_Kick [name or slot #] [minutes] [displayed_reason] | [optional_private_reason]
        Removes a player from the game and won't let the player rejoin until specified [minutes] 
        has passed or until the server is restarted, whichever comes first - kicks are not written
        to the pbbans.dat file but they are logged and will show up in the output from the pb_sv_banlist command 
        """

        if not client.cid or not client.connected:
            return False

        return self.send('PB_SV_Kick "%s" "%s" "%s" "%s"' % (int(client.cid) + 1, minutes, reason, private))

    def getSs(self, client):
        """
        Sends a request to all applicable connected players asking for a screen shot to be captured and sent to the PB Server; to specify a player name or substring (as opposed to slot #), surround the text with double-quote marks 
        """
        
        if not client.cid or not client.connected:
            return False

        return self.send('PB_SV_GetSs "%s"' % (int(client.cid) + 1))

    def pList(self):
        """
        PB_SV_PList
        Displays a list of connected players and their current status 
        """
        return self.send('PB_SV_PList')

    def unBan(self, slot):
        """
        PB_SV_UnBan [slot #]
        Unbans a player from the ban list stored in memory; use pb_sv_updbanfile to update the
        permanent ban file after using this command 
        """
        return self.send('PB_SV_UnBan "%s"' % slot)

    def unBanGUID(self, client):
        """
        PB_SV_UnBanGuid [guid]
        Unbans a guid from the ban list stored in memory; use pb_sv_updbanfile to update the
        permanent ban file after using this command 
        """

        if not client.pbid:
            return False

        result = self.send('PB_SV_UnBanGuid "%s"' % client.pbid)
        if result:
            self.send('pb_sv_updbanfile')
            return result

        return False

    def getPlayerList(self):
        data = self.pList()
        if not data:
            return {}

        players = {}
        lastslot = 0
        for line in data.split('\n'):
            m = re.match(self.regPlayer, line)
            if m:
                d = m.groupdict()
                if int(m.group('slot')) > lastslot:
                    d['guid'] = d['pbid']
                    lastslot = int(m.group('slot'))
                    players[str(lastslot - 1)] = d
                    
                else:
                    self.console.debug('Duplicate or Incorrect PB slot number - client ignored %s lastslot %s' % (m.group('slot'), lastslot))

        return players

    def __setattr__(self, key, value):
        self.__dict__[key] = value

        if key != 'console':
            self.send('PB_SV_%s %s' % (key.title(), value))

    def __getattr__(self, key):
        try:        
            return self.__dict__[key]
        except:
            return self.send('PB_SV_%s' % key.title())
