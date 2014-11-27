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
from weboob.browser import LoginBrowser, need_login, URL
from weboob.exceptions import BrowserIncorrectPassword
from .pages import Login, Home, Transaction

__all__ = ['CarteTicketRestaurantBrowser']

class CarteTicketRestaurantBrowser(LoginBrowser):
    BASEURL     = 'https://www.myedenred.fr'
    login       = URL('/Account/LogOn', Login)
    home        = URL('/Home', Home)
    transaction = URL('/Card/Transaction', Transaction)

    def do_login(self):
        response = self.login.open(data={'email': self.username, 'password': self.password})
        errors = response.get_errors()

        if errors:
            raise BrowserIncorrectPassword(errors)

        return response
  
    @need_login
    def get_accounts_list(self):
        self.home.stay_or_go()
        return self.page.get_accounts()
