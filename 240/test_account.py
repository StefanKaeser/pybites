import pytest
from account import Account


@pytest.fixture(scope="function")
def account_stefan_default():
    account_stefan_default = Account(owner="stefan")
    return account_stefan_default


@pytest.fixture(scope="function")
def account_julia_22():
    account_julia_22 = Account(owner="julia", amount=22)
    return account_julia_22


def test_init(account_stefan_default, account_julia_22):
    assert account_stefan_default.owner == "stefan"
    assert account_stefan_default.amount == 0
    assert account_stefan_default._transactions == []

    assert account_julia_22.amount == 22


def test_repr(account_stefan_default):
    assert account_stefan_default.__repr__() == "Account('stefan', 0)"


def test_str(account_stefan_default):
    assert (
        account_stefan_default.__str__() == "Account of stefan with starting amount: 0"
    )


def test_add_transaction(account_stefan_default):
    with pytest.raises(ValueError, match="please use int for amount"):
        account_stefan_default.add_transaction(1.1)
    account_stefan_default.add_transaction(2)
    assert account_stefan_default._transactions == [2]
    account_stefan_default.add_transaction(3)
    assert account_stefan_default._transactions == [2, 3]


def test_balance(account_stefan_default, account_julia_22):
    assert account_stefan_default.balance == 0

    account_stefan_default.add_transaction(2)
    assert account_stefan_default.balance == 2
    account_stefan_default.add_transaction(3)
    assert account_stefan_default.balance == 5

    assert account_julia_22.balance == 22

    account_julia_22.add_transaction(10)
    assert account_julia_22.balance == 32

    with pytest.raises(AttributeError, match="can't set attribute"):
        account_julia_22.balance = 1000


def test_len(account_stefan_default):
    assert len(account_stefan_default) == 0

    for n in range(100):
        account_stefan_default.add_transaction(1)

    assert len(account_stefan_default) == 100


def test_getitem(account_stefan_default):
    with pytest.raises(IndexError, match="list index out of range"):
        account_stefan_default[0]

    account_stefan_default.add_transaction(1)
    assert account_stefan_default[0] == 1


def test_eq(account_stefan_default, account_julia_22):
    assert (account_stefan_default == account_julia_22) == False

    account_stefan_default.add_transaction(22)
    assert (account_stefan_default == account_julia_22) == True


def test_lt(account_stefan_default, account_julia_22):
    assert (account_stefan_default < account_julia_22) == True
    assert (account_julia_22 < account_stefan_default) == False

    account_stefan_default.add_transaction(22)
    assert (account_stefan_default < account_julia_22) == False


def test_total_ordering(account_stefan_default, account_julia_22):
    assert account_stefan_default <= account_julia_22
    assert account_julia_22 > account_stefan_default
    assert account_julia_22 >= account_stefan_default


def test_add(account_stefan_default, account_julia_22):
    account_shared = account_stefan_default + account_julia_22
    assert account_shared.owner == "stefan&julia"
    assert account_shared.amount == 22
    assert (
        account_shared._transactions
        == account_stefan_default._transactions + account_julia_22._transactions
    )

    account_stefan_default.add_transaction(10)
    account_julia_22.add_transaction(15)
    account_shared = account_julia_22 + account_stefan_default
    assert account_shared.owner == "julia&stefan"
    assert account_shared.amount == 22
    assert (
        account_shared._transactions
        == account_julia_22._transactions + account_stefan_default._transactions
    )
