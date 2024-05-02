from ape import project
import ape



def test_reverts_if_token_length_doesnt_match_price_feeds(deployer, weth, wbtc, weth_usd_price_feed, dsc):
    token_addresses = [weth, wbtc]
    price_feed_addresses = [weth_usd_price_feed]
    with ape.reverts():
        project.DSCEngine.deploy(token_addresses, price_feed_addresses, dsc, sender=deployer)


def test_get_usd_value(weth, dsc_engine):
    eth_amount = int(15e18)
    expected_usd = int(30_000e18)
    actual_usd = dsc_engine.getUsdValue(weth, eth_amount)
    assert expected_usd == actual_usd


def test_get_token_amount_from_usd(weth, dsc_engine):
    usd_amount = int(100e18)
    expected_weth = int(0.05e18)
    actual_weth = dsc_engine.getTokenAmountFromUsd(weth, usd_amount)
    assert expected_weth == actual_weth


def test_reverts_with_unapproved_collateral(deployer, user, weth, dsc_engine):
    amount_collateral = int(10e18)
    weth.mint(user, amount_collateral, sender=deployer)
    with ape.reverts():
        dsc_engine.depositCollateral(weth, amount_collateral, sender=user)


def test_reverts_if_collateral_is_zero(deployer, user, weth, dsc_engine):
    amount_collateral = int(10e18)
    weth.mint(user, amount_collateral, sender=deployer)
    weth.approve(dsc_engine, amount_collateral, sender=user)

    with ape.reverts():
        dsc_engine.depositCollateral(weth, 0, sender=user)


def test_can_deposit_collateral_and_get_account_info(deployer, user, weth, dsc_engine):
    amount_collateral = int(10e18)
    weth.mint(user, amount_collateral, sender=deployer)
    weth.approve(dsc_engine, amount_collateral, sender=user)
    dsc_engine.depositCollateral(weth, amount_collateral, sender=user)

    (total_dsc_minted, collateral_value_in_usd) = dsc_engine.getAccountInformation(user)
    expected_dsc_minted = 0
    expected_collateral_in_usd = int(amount_collateral * 2000)
    expected_deposited_amount = dsc_engine.getTokenAmountFromUsd(weth, collateral_value_in_usd)
    assert total_dsc_minted == expected_dsc_minted
    assert collateral_value_in_usd == expected_collateral_in_usd
    assert amount_collateral == expected_deposited_amount

