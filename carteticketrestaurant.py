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

from weboob.browser import LoginBrowser, need_login, URL
from .pages import Login, Home, Transaction

__all__ = ['CarteTicketRestaurantBrowser']

class CarteTicketRestaurantBrowser(LoginBrowser):
    BASEURL     = 'https://www.myedenred.fr'
    login       = URL('/Account/LogOn', Login)
    home        = URL('/Home', Home)
    transaction = URL('/Card/Transaction', Transaction)

    def do_login(self):
        if self.username and self.password:
            parameters = {}
            parameters['Email'] = self.username
            parameters['password'] = self.password
            response = self.login.open(data=parameters)
            
            #TODO: login.is_here() ne marche pas ! le problème vient peu-être de self.login.open ?
            if self.login.is_here():
                raise BrowserIncorrectPassword(self.page.get_error())
                
            return response
  
    @need_login
    def get_accounts_list(self):
        self.home.stay_or_go()
        return self.page.get_accounts()
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

from .module import CarteTicketRestaurantModule

__all__ = ['CarteTicketRestaurantModule']
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
from weboob.capabilities.base import find_object
from weboob.capabilities.bank import CapBank, AccountNotFound
from weboob.tools.backend import Module, BackendConfig
from weboob.tools.value import Value, ValueBackendPassword

from .browser import CarteTicketRestaurantBrowser

__all__ = ['CarteTicketRestaurantModule']

class CarteTicketRestaurantModule(Module, CapBank):
    NAME = 'carteticketrestaurant'
    DESCRIPTION = u'Carte Ticket Restaurant'
    MAINTAINER = u'Binnette'
    EMAIL = 'binnette@gmail.com'
    LICENSE = 'AGPLv3+'
    VERSION = '1.1'

    BROWSER = CarteTicketRestaurantBrowser
    
    CONFIG = BackendConfig(Value('email', label='Email', regexp='[^@]+@[^@]+\.[^@]+'),
                           ValueBackendPassword('password', label='Mot de passe'))

    def create_default_browser(self):
        return self.create_browser(self.config['email'].get(),
                                   self.config['password'].get())

    def iter_accounts(self):
        return self.browser.get_accounts_list()

    def get_account(self, _id):
        return find_object(self.browser.get_accounts_list(), id=_id, error=AccountNotFound)

    def iter_history(self, account):
        """
        Iter history of transactions on a specific account.

        :param account: account to get history
        :type account: :class:`Account`
        :rtype: iter[:class:`Transaction`]
        :raises: :class:`AccountNotFound`
        """
        #TODO
        log = getLogger("Binnette")
        log.debug("iter_history")
        raise NotImplementedError()
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

from decimal import Decimal
from weboob.browser.pages import HTMLPage
from weboob.capabilities.bank import Account

class Login(HTMLPage):
    def get_error(self):
        #TODO
        return "BinnetteException"

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

from weboob.tools.test import BackendTest

class CarteTicketRestaurantTest(BackendTest):
    MODULE = 'carteticketrestaurant'

    def test_CarteTicketRestaurant(self):
        raise NotImplementedError()
