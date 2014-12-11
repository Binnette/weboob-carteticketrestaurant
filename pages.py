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

from weboob.browser.elements import ListElement, ItemElement, method
from weboob.browser.filters.standard import CleanText, CleanDecimal, Date, DateGuesser
from weboob.browser.pages import HTMLPage, pagination
from weboob.capabilities.bank import Account, Transaction
from weboob.tools.date import LinearDateGuesser

class Login(HTMLPage):
    def get_errors(self):
        return CleanText('//div[@class="notification-summary"]/ul/li[@class="notification-summary-message-error"]')(self.doc)

class Home(HTMLPage):
    def get_accounts(self):
        account = Account()
        account.id = CleanText('//div[@class="carte"]/p/a[@class="basic-href"]')(self.doc)
        account.balance = CleanDecimal('//div[@class="solde"]/p/a/strong', replace_dots=True)(self.doc)
        account.label = CleanText('//div[@class="bl bl-produit"]/nav/ul/li/a/strong', children=False)(self.doc)
        yield account

class Transaction(HTMLPage):
    def get_form_next_transactions(self):
        return self.get_form('//div[@id="tab-debit"]//form', submit='//div[@id="updateDebit"]/div/input')

    def have_button_next(self):
        button_next = self.doc.xpath('//div/input[@type="submit"]')
        return len(button_next) > 0

    @method
    class get_chargements(ListElement):
        item_xpath = '//div[@id="tab-chargement"]//table[@class="table table-transaction"]/tbody/tr'

        class item(ItemElement):
            klass = Transaction
            condition = lambda self: len(self.el.xpath('./td')) >= 4

            obj_date = DateGuesser(CleanText('./td[1]/span'), LinearDateGuesser())
            obj_label = CleanText('./td[2]/h3')
            obj_raw = CleanText('./td[3]/span')
            obj_amount = CleanDecimal('./td[4]/span', replace_dots=True)
            obj_type = Account.TYPE_DEPOSIT
            obj_rdate = None
            obj_vdate = None
            obj_category = ""

    @method
    class get_debits(ListElement):
        item_xpath = '//table[@class="table table-transaction"]/tbody/tr'

        class item(ItemElement):
            klass = Transaction
            condition = lambda self: len(self.el.xpath('./td')) >= 4

            obj_date = DateGuesser(CleanText('./td[1]/span'), LinearDateGuesser())
            obj_label = CleanText('./td[2]/h3')
            obj_raw = CleanText('./td[3]/span')
            obj_amount = CleanDecimal('./td[4]/span', replace_dots=True)
            obj_type = Account.TYPE_CHECKING
            obj_rdate = None
            obj_vdate = None
            obj_category = ""