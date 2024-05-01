import ape


def test_get_usd_value(weth, dsc_engine):
    eth_amount = int(15e18)
    expected_usd = int(30_000e18)
    actual_usd = dsc_engine.getUsdValue(weth, eth_amount)
    assert expected_usd == actual_usd


def test_reverts_if_collateral_is_zero(deployer, user, weth, dsc_engine):
    amount_collateral = int(10e18)
    weth.mint(user, amount_collateral, sender=deployer)
    weth.approve(dsc_engine, amount_collateral, sender=user)

    with ape.reverts():
        dsc_engine.depositCollateral(weth, 0, sender=user)
