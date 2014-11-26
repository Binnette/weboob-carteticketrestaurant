# -*- coding: utf-8 -*-

# Copyright(C) 2014      Binnette
#
# This file is part of weboob.
#
# weboob is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# weboob is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with weboob. If not, see <http://www.gnu.org/licenses/>.

from weboob.tools.log import getLogger
from decimal import Decimal
from weboob.browser.pages import HTMLPage
from weboob.capabilities.bank import Account

class Login(HTMLPage):
    def get_error(self):
        notification = self.doc.xpath('//div[@class="notification-summary"]/ul/li[@class="notification-summary-message-error"]')
        errors = ""
        for err in notification:
            errors += err.text
        return errors

class Home(HTMLPage):
    def get_accounts(self):
        id = None
        balance = None
        carte = self.doc.xpath('//div[@class="carte"]/p/a[@class="basic-href"]')
        solde = self.doc.xpath('//div[@class="solde"]/p/a/strong')

        if len(carte) == 1:
            id = carte.pop().text

        if len(solde) == 1:
            balance = solde.pop().text
            balance = balance.replace(",", ".")
            balance = balance.replace(unichr(8364), "") #unichr(8364) => €

        if id is not None and balance is not None:
            account = Account()
            account.id = id
            account.label = unicode("Carte Ticket Restaurant")
            account.balance = Decimal(balance)  
            yield account;

class Transaction(HTMLPage):
    pass
