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

from weboob.browser.filters.standard import CleanText, CleanDecimal
from weboob.browser.pages import HTMLPage
from weboob.capabilities.bank import Account

class Login(HTMLPage):
    def get_error(self):
        return CleanText('//div[@class="notification-summary"]/ul/li[@class="notification-summary-message-error"]')(self.doc)

class Home(HTMLPage):
    def get_accounts(self):
        euro = 8364 # symbol €
        account = Account()
        account.id = CleanText('//div[@class="carte"]/p/a[@class="basic-href"]')(self.doc)
        account.balance = CleanDecimal(CleanText('//div[@class="solde"]/p/a/strong', symbols=unichr(euro)), replace_dots=True)(self.doc)
        account.label = CleanText('//div[@class="bl bl-produit"]/nav/ul/li/a/strong', children=False)(self.doc)
        yield account

class Transaction(HTMLPage):
    pass
