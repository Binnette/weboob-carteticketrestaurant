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
