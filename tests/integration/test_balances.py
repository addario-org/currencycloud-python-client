import pytest
from betamax import Betamax
from mock import patch
import requests_mock
import re

from currencycloud import Client, Config
from currencycloud.resources import *


class TestBalances:
    def setup_method(self, method):
        login_id = 'development@currencycloud.com'
        api_key = 'deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef'
        environment = Config.ENV_DEMO

        self.client = Client(login_id, api_key, environment)

    def test_balances_can_get_for_a_currency(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('balances/for_currency')

            balance = self.client.balances.for_currency("GBP")

            assert balance is not None
            assert isinstance(balance, Balance)

            assert balance.currency == "GBP"

    def test_balances_can_find(self):
        with Betamax(self.client.config.session) as betamax:
            betamax.use_cassette('balances/find')

            balances = self.client.balances.find(per_page=1)

            assert balances
            assert len(balances) == 1

            balance = balances[0]
            assert isinstance(balance, Balance)
