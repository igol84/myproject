import pytest
from pydantic import ValidationError

from util.currency import Currency


class Test_01_Currency:
    def setup(self):
        self.cur = Currency(code='uah', rate=27.5, sign='₴')

    def test_01_initial(self):
        assert str(self.cur) == "Currency(code='UAH', rate=27.5, sign='₴')"
        assert self.cur.code == 'UAH'
        assert self.cur.rate == 27.5
        assert self.cur.sign == '₴'

    def test_02_edit_code(self):
        self.cur.code = 'USD'
        assert str(self.cur) == "Currency(code='USD', rate=27.5, sign='₴')"

    def test_03_edit_rate(self):
        self.cur.rate = 28
        assert str(self.cur) == "Currency(code='UAH', rate=28, sign='₴')"
        self.cur.rate = 28.5
        assert str(self.cur) == "Currency(code='UAH', rate=28.5, sign='₴')"

    def test_04_edit_sign(self):
        self.cur.sign = '¥'
        assert str(self.cur) == "Currency(code='UAH', rate=27.5, sign='¥')"

    def test_contract_raises(self):
        with pytest.raises(ValidationError):
            Currency(code='UA', rate=27.5, sign='₴')
        with pytest.raises(ValidationError):
            Currency(code='UAH', rate=27.5, sign='₴3')
