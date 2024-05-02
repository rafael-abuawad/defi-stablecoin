import pytest


@pytest.fixture(scope="function")
def deployer(accounts):
    return accounts[0]


@pytest.fixture(scope="function")
def user(accounts):
    return accounts[1]


@pytest.fixture(scope="function")
def weth_usd_price_feed(project, deployer):
    decimals = 8
    weth_usd_price = int(2000e8)
    return project.MockV3Aggregator.deploy(decimals, weth_usd_price, sender=deployer)


@pytest.fixture(scope="function")
def wbtc_usd_price_feed(project, deployer):
    decimals = 8
    wbtc_usd_price = int(1000e8)
    return project.MockV3Aggregator.deploy(decimals, wbtc_usd_price, sender=deployer)


@pytest.fixture(scope="function")
def weth(project, deployer):
    initial_balance = int(0)
    return project.MockERC20.deploy(
        "Wrapped ETH",
        "WETH",
        deployer,
        initial_balance,
        sender=deployer,
    )


@pytest.fixture(scope="function")
def wbtc(project, deployer):
    initial_balance = int(0)
    return project.MockERC20.deploy(
        "Wrapped BTC",
        "WBTC",
        deployer,
        initial_balance,
        sender=deployer,
    )


@pytest.fixture(scope="function")
def dsc(project, deployer):
    return project.DSC.deploy(sender=deployer)


@pytest.fixture(scope="function")
def dsc_engine(
    project, deployer, weth, wbtc, weth_usd_price_feed, wbtc_usd_price_feed, dsc
):
    token_addresses = [weth, wbtc]
    price_feed_addresses = [
        weth_usd_price_feed,
        wbtc_usd_price_feed,
    ]

    dsc_engine = project.DSCEngine.deploy(
        token_addresses, price_feed_addresses, dsc, sender=deployer
    )
    dsc.transferOwnership(dsc_engine, sender=deployer)
    return dsc_engine
