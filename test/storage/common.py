#
# BigBrotherBot(B3) (www.bigbrotherbot.net)
# Copyright (C) 2011 Courgette
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
from b3.clients import Client, Alias, IpAlias, Penalty, ClientKick, Group
from mock import Mock
import b3

class StorageAPITest(object):
    storage = None
        
    def test_setClient(self):
        c1 = Client(ip="1.2.3.4", connections=2, guid="abcdefghijkl", pbid="123546abcdef", name="some dude", greeting="hi!")
        c1_id = self.storage.setClient(c1)
        self.assertEqual(1, c1_id)
        c2 = self.storage.getClient(Client(id=c1_id))
        self.assertIsInstance(c2, Client)
        self.assertEqual("1.2.3.4", c2.ip)
        self.assertEqual(2, c2.connections)
        self.assertEqual("abcdefghijkl", c2.guid)
        self.assertEqual("123546abcdef", c2.pbid)
        self.assertEqual("some dude", c2.name)
        self.assertEqual("hi!", c2.greeting)

    def test_getClient_id(self):
        c1 = Client(ip="1.2.3.4", connections=3, guid="mlkjmlkjqsdf", pbid="123546abcdef", name="some dude", greeting="hi!")
        c1_id = self.storage.setClient(c1)
        self.assertEqual(1, c1_id)
        c2 = self.storage.getClient(Client(id=c1_id))
        self.assertIsInstance(c2, Client)

    def test_getClient_guid(self):
        c1 = Client(ip="1.2.3.4", connections=3, guid="mlkjmlkjqsdf", pbid="123546abcdef", name="some dude", greeting="hi!")
        c1_id = self.storage.setClient(c1)
        self.assertEqual(1, c1_id)
        c2 = self.storage.getClient(Client(guid="mlkjmlkjqsdf"))
        self.assertIsInstance(c2, Client)

    def test_getClientsMatching(self):
        self.storage.setClient(Client(ip="1.2.3.4", connections=2, guid="mlkjmlkjqsdf", pbid="123546abcdef", name="bill"))
        self.storage.setClient(Client(ip="4.2.3.5", connections=3, guid="azerazerazer", pbid="wxcvwxvcxwcv", name="john"))
        self.storage.setClient(Client(ip="4.2.3.5", connections=45, guid="rtyrtyrty", pbid="rtyrtyrrtyr", name="jack"))

        result = self.storage.getClientsMatching({'guid': "xxxxxxxxxx"})
        self.assertEqual(0, len(result))

        result = self.storage.getClientsMatching({'ip': "1.2.3.4"})
        self.assertEqual(1, len(result))
        self.assertEqual('bill', result[0].name)

        result = self.storage.getClientsMatching({'ip': "4.2.3.5"})
        self.assertEqual(2, len(result))

        result = self.storage.getClientsMatching({'pbid': "rtyrtyrrtyr"})
        self.assertEqual(1, len(result))
        self.assertEqual('jack', result[0].name)

        result = self.storage.getClientsMatching({'name': "jack"})
        self.assertEqual(1, len(result))
        self.assertEqual('jack', result[0].name)

        result = self.storage.getClientsMatching({'ip': "4.2.3.5", 'name': 'jack'})
        self.assertEqual(1, len(result))
        self.assertEqual('jack', result[0].name)

        result = self.storage.getClientsMatching({'ip': "4.2.3.5", 'connections >': 10})
        self.assertEqual(1, len(result))
        self.assertEqual('jack', result[0].name)



    def test_setClientAlias(self):
        alias_id1 = self.storage.setClientAlias(Alias(alias='bill', clientId=1))
        self.assertIsNotNone(alias_id1)
        alias_id2 = self.storage.setClientAlias(Alias(alias='joe', clientId=1))
        self.assertEqual(alias_id1 + 1, alias_id2)

    def test_getClientAlias(self):
        alias = Alias(alias='bill', timeAdd=12, timeEdit=654, numUsed=7, clientId=54)
        alias_id = self.storage.setClientAlias(alias)
        alias = self.storage.getClientAlias(Alias(id=alias_id))
        self.assertIsInstance(alias, Alias)
        self.assertEqual(alias.alias, 'bill')
        self.assertEqual(alias.timeAdd, 12)
        self.assertEqual(alias.timeEdit, 654)
        self.assertEqual(alias.numUsed, 7)
        self.assertEqual(alias.clientId, 54)

    def test_getClientAliases(self):
        client = Mock()
        client.id = 15
        self.storage.setClientAlias(Alias(alias='bill', clientId=client.id))
        self.storage.setClientAlias(Alias(alias='joe', clientId=client.id))
        self.storage.setClientAlias(Alias(alias='jack', clientId=0))
        aliases = self.storage.getClientAliases(client)
        self.assertIsInstance(aliases, list)
        self.assertEqual(len(aliases), 2)
        bucket = []
        for i in aliases:
            self.assertIsInstance(i, Alias)
            self.assertEqual(i.clientId, client.id)
            self.assertNotEqual(i.id, None)
            self.assertNotEqual(i.alias, None)
            self.assertNotEqual(i.timeAdd, None)
            self.assertNotEqual(i.timeEdit, None)
            self.assertNotEqual(i.numUsed, None)
            bucket.append(i.alias)
        self.assertIn('bill', bucket)
        self.assertIn('joe', bucket)
        self.assertNotIn('jack', bucket)


    def test_setClientIpAddresse(self):
        ipalias_id1 = self.storage.setClientIpAddresse(IpAlias(ip='1.2.3.4', clientId=1))
        self.assertIsNotNone(ipalias_id1)
        ipalias_id2 = self.storage.setClientIpAddresse(IpAlias(ip='127.0.0.1', clientId=1))
        self.assertEqual(ipalias_id1 + 1, ipalias_id2)

    def test_getClientIpAddress(self):
        ipalias = IpAlias(ip='88.44.55.22', timeAdd=12, timeEdit=654, numUsed=7, clientId=54)
        ipalias_id = self.storage.setClientIpAddresse(ipalias)
        ipalias = self.storage.getClientIpAddress(IpAlias(id=ipalias_id))
        self.assertIsInstance(ipalias, IpAlias)
        self.assertEqual(ipalias.ip, '88.44.55.22')
        self.assertEqual(ipalias.timeAdd, 12)
        self.assertEqual(ipalias.timeEdit, 654)
        self.assertEqual(ipalias.numUsed, 7)
        self.assertEqual(ipalias.clientId, 54)

    def test_getClientIpAddresses(self):
        client = Mock()
        client.id = 15
        self.storage.setClientIpAddresse(IpAlias(ip='44.44.44.44', clientId=client.id))
        self.storage.setClientIpAddresse(IpAlias(ip='55.55.55.55', clientId=client.id))
        self.storage.setClientIpAddresse(IpAlias(ip='66.66.66.66', clientId=0))
        ipaliases = self.storage.getClientIpAddresses(client)
        self.assertIsInstance(ipaliases, list)
        self.assertEqual(len(ipaliases), 2)
        ips = []
        for i in ipaliases:
            self.assertIsInstance(i, IpAlias)
            self.assertEqual(i.clientId, client.id)
            self.assertNotEqual(i.id, None)
            self.assertNotEqual(i.ip, None)
            self.assertNotEqual(i.timeAdd, None)
            self.assertNotEqual(i.timeEdit, None)
            self.assertNotEqual(i.numUsed, None)
            ips.append(i.ip)
        self.assertIn('44.44.44.44', ips)
        self.assertIn('55.55.55.55', ips)
        self.assertNotIn('66.66.66.66', ips)




    def test_setClientPenalty(self):
        id1 = self.storage.setClientPenalty(Penalty(type='Ban', clientId=1, adminId=0))
        self.assertIsNotNone(id1)
        id2 = self.storage.setClientPenalty(Penalty(type='Kick', clientId=1, adminId=0))
        self.assertEqual(id1 + 1, id2)

    def test_getClientPenalty(self):
        tmp = Penalty(type='Kick', 
                      clientId=54,
                      inactive=1,
                      adminId=4,
                      reason='respect the rules',
                      keyword='rules',
                      data='foo',
                      timeAdd=123,
                      timeEdit=1234,
                      timeExpire=654,
                      duration=87,
                      )
        tmp_id = self.storage.setClientPenalty(tmp)
        penalty = self.storage.getClientPenalty(Penalty(type="Kick", id=tmp_id))
        self.assertIsInstance(penalty, Penalty)
        self.assertEqual(penalty.type, 'Kick')
        self.assertEqual(penalty.clientId, 54)
        self.assertEqual(penalty.inactive, 1)
        self.assertEqual(penalty.adminId, 4)
        self.assertEqual(penalty.reason, 'respect the rules')
        self.assertEqual(penalty.keyword, 'rules')
        self.assertEqual(penalty.data, 'foo')
        self.assertEqual(penalty.timeAdd, 123)
        self.assertEqual(penalty.timeEdit, 1234)
        self.assertEqual(penalty.timeExpire, 654)
        self.assertEqual(penalty.duration, 87)

    def test_getClientPenalties(self):
        c1 = Mock()
        c1.id = 15
        c2 = Mock()
        c2.id = 18
        Penalty(clientId=c1.id, adminId=0, inactive=1, type='Ban', timeExpire=-1, data='pA').save(b3.console)
        Penalty(clientId=c1.id, adminId=0, inactive=0, type='Ban', timeExpire=b3.console.time()+10, data='pB').save(b3.console)
        Penalty(clientId=c1.id, adminId=0, inactive=0, type='Warning', timeExpire=b3.console.time()+10, data='pC').save(b3.console)
        Penalty(clientId=c1.id, adminId=0, inactive=0, type='Kick', timeExpire=b3.console.time()-10, data='pD').save(b3.console)
        Penalty(clientId=c1.id, adminId=0, inactive=0, type='Ban', timeExpire=b3.console.time()-10, data='pE').save(b3.console)
        Penalty(clientId=c2.id, adminId=0, inactive=0, type='Warning', timeExpire=-1, data='pF').save(b3.console)
        Penalty(clientId=c2.id, adminId=0, inactive=0, type='TempBan', timeExpire=-1, data='pG').save(b3.console)

        def assertPenalties(client, types, penalties_in=[], penalties_notin=[]):
            penalties = self.storage.getClientPenalties(client=client, type=types)
            self.assertIsInstance(penalties, list)
            bucket = []
            for i in penalties:
                self.assertIsInstance(i, Penalty)
                self.assertEqual(i.clientId, client.id)
                bucket.append(i.data)
            for i in penalties_in:
                self.assertIn(i, bucket)
            for i in penalties_notin:
                self.assertNotIn(i, bucket)

        assertPenalties(client=c1, types=('Ban', 'TempBan', 'Kick', 'Warning', 'Notice'), 
                        penalties_in=('pB','pC'), penalties_notin=('pA','pD','pE','pF','pG'))
        assertPenalties(client=c2, types=('Ban', 'TempBan', 'Kick', 'Warning', 'Notice'), 
                        penalties_in=('pF','pG'), penalties_notin=('pA','pB','pC','pD','pE'))


    def test_getClientLastPenalty(self):
        client = Mock()
        client.id = 15
        self.storage.setClientPenalty(Penalty(clientId=client.id, adminId=0, timeAdd=2, timeExpire=-1, type='Ban', data='pA'))
        self.storage.setClientPenalty(Penalty(clientId=client.id, adminId=0, timeAdd=4, timeExpire=-1, type='Kick',data='pB'))
        self.storage.setClientPenalty(Penalty(clientId=client.id, adminId=0, timeAdd=1, timeExpire=-1, type='Notice', data='pC'))
        self.storage.setClientPenalty(Penalty(clientId=client.id, adminId=0, timeAdd=3, timeExpire=-1, type='Ban', data='pD'))
        self.storage.setClientPenalty(Penalty(clientId=client.id, adminId=0, timeAdd=6, timeExpire=-1, type='Kick', data='pE'))
        self.storage.setClientPenalty(Penalty(clientId=client.id, adminId=0, timeAdd=5, timeExpire=-1, type='Ban', data='pF'))
        penalty = self.storage.getClientLastPenalty(client=client)
        self.assertIsInstance(penalty, Penalty)
        self.assertEqual(penalty.data, 'pF')
        penalty = self.storage.getClientLastPenalty(client=client, type=('Ban', 'Kick'))
        self.assertIsInstance(penalty, Penalty)
        self.assertEqual(penalty.data, 'pE')
        penalty = self.storage.getClientLastPenalty(client=client, type=('Ban', 'Kick','Notice'))
        self.assertIsInstance(penalty, Penalty)
        self.assertEqual(penalty.data, 'pE')

    def test_getClientFirstPenalty(self):
        client = Mock()
        client.id = 15
        self.storage.setClientPenalty(Penalty(clientId=client.id, adminId=0, timeAdd=2, timeExpire=-1, type='Ban', data='pA'))
        self.storage.setClientPenalty(Penalty(clientId=client.id, adminId=0, timeAdd=4, timeExpire=-1, type='Kick', data='pB'))
        self.storage.setClientPenalty(Penalty(clientId=client.id, adminId=0, timeAdd=1, timeExpire=-1, type='Notice', data='pC'))
        self.storage.setClientPenalty(Penalty(clientId=client.id, adminId=0, timeAdd=3, timeExpire=-1, type='Ban', data='pD'))
        self.storage.setClientPenalty(Penalty(clientId=client.id, adminId=0, timeAdd=6, timeExpire=-1, type='Kick', data='pE'))
        self.storage.setClientPenalty(Penalty(clientId=client.id, adminId=0, timeAdd=5, timeExpire=-1, type='Ban', data='pF'))
        penalty = self.storage.getClientFirstPenalty(client=client)
        self.assertIsInstance(penalty, Penalty)
        self.assertEqual(penalty.data, 'pA')
        penalty = self.storage.getClientFirstPenalty(client=client, type=('Ban', 'Kick'))
        self.assertIsInstance(penalty, Penalty)
        self.assertEqual(penalty.data, 'pA')
        penalty = self.storage.getClientFirstPenalty(client=client, type=('Ban', 'Kick','Notice'))
        self.assertIsInstance(penalty, Penalty)
        self.assertEqual(penalty.data, 'pC')


    def test_disableClientPenalties(self):
        c1 = Mock()
        c1.id = 15
        c2 = Mock()
        c2.id = 18
        Penalty(clientId=c1.id, adminId=0, timeExpire=-1, type='Ban', inactive=1, data='pA').save(b3.console)
        Penalty(clientId=c1.id, adminId=0, timeExpire=-1, type='Ban', inactive=0, data='pB').save(b3.console)
        Penalty(clientId=c1.id, adminId=0, timeExpire=-1, type='Warning', inactive=0, data='pC').save(b3.console)
        Penalty(clientId=c1.id, adminId=0, timeExpire=-1, type='Kick', inactive=0, data='pD').save(b3.console)
        Penalty(clientId=c2.id, adminId=0, timeExpire=-1, type='Notice', inactive=0, data='pE').save(b3.console)
        Penalty(clientId=c2.id, adminId=0, timeExpire=-1, type='Warning', inactive=0, data='pF').save(b3.console)
        Penalty(clientId=c1.id, adminId=0, timeExpire=-1, type='TempBan', inactive=0, data='pG').save(b3.console)

        def assertPenalties(client, types='Ban', penalties_in=[], penalties_notin=[]):
            penalties = self.storage.getClientPenalties(client=client, type=types)
            self.assertIsInstance(penalties, list)
            bucket = []
            for i in penalties:
                self.assertIsInstance(i, Penalty)
                self.assertEqual(i.clientId, client.id)
                bucket.append(i.data)
            for i in penalties_in:
                self.assertIn(i, bucket)
            for i in penalties_notin:
                self.assertNotIn(i, bucket)

        assertPenalties(client=c1, types=('Ban', 'TempBan', 'Kick', 'Warning', 'Notice'), 
                        penalties_in=('pB','pC','pD','pG'), penalties_notin=('pA','pE','pF'))
        assertPenalties(client=c2, types=('Ban', 'TempBan', 'Kick', 'Warning', 'Notice'), 
                        penalties_in=('pE','pF'), penalties_notin=('pA','pB','pC','pD','pG'))

        self.storage.disableClientPenalties(client=c1)
        assertPenalties(client=c1, types=('Ban', 'TempBan', 'Kick', 'Warning', 'Notice'), 
                        penalties_in=('pC','pD','pG'), penalties_notin=('pA','pB','pE','pF'))
        assertPenalties(client=c2, types=('Ban', 'TempBan', 'Kick', 'Warning', 'Notice'), 
                        penalties_in=('pE','pF'), penalties_notin=('pA','pB','pC','pD','pG'))

        self.storage.disableClientPenalties(client=c1, type=('Kick','Notice'))
        assertPenalties(client=c1, types=('Ban', 'TempBan', 'Kick', 'Warning', 'Notice'), 
                        penalties_in=('pC','pG'), penalties_notin=('pA','pB','pD','pE','pF'))
        assertPenalties(client=c2, types=('Ban', 'TempBan', 'Kick', 'Warning', 'Notice'), 
                        penalties_in=('pE','pF'), penalties_notin=('pA','pB','pC','pD','pG'))

    def test_numPenalties(self):
        c1 = Mock()
        c1.id = 15
        c2 = Mock()
        c2.id = 18
        Penalty(clientId=c1.id, adminId=0, timeExpire=-1, type='Ban', inactive=1, data='pA').save(b3.console)
        Penalty(clientId=c1.id, adminId=0, timeExpire=-1, type='Ban', inactive=0, data='pB').save(b3.console)
        Penalty(clientId=c1.id, adminId=0, timeExpire=-1, type='Warning', inactive=0, data='pC').save(b3.console)
        Penalty(clientId=c1.id, adminId=0, timeExpire=-1, type='Kick', inactive=0, data='pD').save(b3.console)
        Penalty(clientId=c2.id, adminId=0, timeExpire=-1, type='Notice', inactive=0, data='pE').save(b3.console)
        Penalty(clientId=c2.id, adminId=0, timeExpire=-1, type='Warning', inactive=0, data='pF').save(b3.console)
        Penalty(clientId=c1.id, adminId=0, timeExpire=-1, type='TempBan', inactive=0, data='pG').save(b3.console)
        self.assertEqual(1, self.storage.numPenalties(client=c1))
        self.assertEqual(4, self.storage.numPenalties(client=c1, type=('Ban', 'TempBan', 'Kick', 'Warning', 'Notice')))
        self.assertEqual(0, self.storage.numPenalties(client=c2))
        self.assertEqual(2, self.storage.numPenalties(client=c2, type=('Ban', 'TempBan', 'Kick', 'Warning', 'Notice')))



    def test_getGroups(self):
        groups = self.storage.getGroups()
        self.assertEqual(8, len(groups))
        for g in groups:
            self.assertIsInstance(g, Group)

    def test_getGroup(self):
        g = self.storage.getGroup(Group(keyword='superadmin'))
        self.assertIsInstance(g, Group)



    def test_getCounts(self):
        self.assertEqual({'kicks': 0, 'tempbans': 0, 'clients': 0, 'bans': 0, 'warnings': 0}, self.storage.getCounts())
        client_id = self.storage.setClient(Client(guid="aaaaaaaaa"))
        self.assertIsInstance(client_id, int)
        self.assertEqual({'kicks': 0, 'tempbans': 0, 'clients': 1, 'bans': 0, 'warnings': 0}, self.storage.getCounts())
        client_id = self.storage.setClient(Client(guid="bbbbbbbbbb"))
        self.assertIsInstance(client_id, int)
        self.assertEqual({'kicks': 0, 'tempbans': 0, 'clients': 2, 'bans': 0, 'warnings': 0}, self.storage.getCounts())
        raise NotImplementedError