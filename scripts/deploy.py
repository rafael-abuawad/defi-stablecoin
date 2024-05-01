from ape import project, accounts, chain
from eth_account import Account

OP_MAINNET = 10
OP_SEPOLIA_TESTNET = 11155420
ANVIL = 31337


class NetworkConfig:
    deployer: Account
    weth_usd_price_feed: str
    wbtc_usd_price_feed: str
    weth: str
    wbtc: str

    def __init__(self):
        chain_id = chain.chain_id
        if chain_id == OP_SEPOLIA_TESTNET:
            self.deployer = accounts.load("deployer")
            self.weth_usd_price_feed = "0x61Ec26aA57019C486B10502285c5A3D4A4750AD7"
            self.wbtc_usd_price_feed = "0x3015aa11f5c2D4Bd0f891E708C8927961b38cE7D"
            self.weth = "0x4200000000000000000000000000000000000006"
            self.wbtc = "0x2297aEbD383787A160DD0d9F71508148769342E3"

        elif chain_id == OP_MAINNET:
            self.deployer = accounts.load("deployer")
            self.weth_usd_price_feed = "0x13e3Ee699D1909E989722E753853AE30b17e08c5"
            self.wbtc_usd_price_feed = "0xD702DD976Fb76Fffc2D3963D037dfDae5b04E593"
            self.weth = "0x4200000000000000000000000000000000000006"
            self.wbtc = "0x2297aEbD383787A160DD0d9F71508148769342E3"

        else:  # Anvil / Locannet
            self.deployer = accounts.test_accounts[0]
            decimals = 8
            wbtc_usd_price = int(1000e8)
            weth_usd_price = int(2000e8)
            self.weth_usd_price_feed = project.MockV3Aggregator.deploy(
                decimals, weth_usd_price, sender=self.deployer
            )
            self.wbtc_usd_price_feed = project.MockV3Aggregator.deploy(
                decimals, wbtc_usd_price, sender=self.deployer
            )
            initial_balance = int(10_000e18)
            self.weth = project.MockERC20.deploy(
                "Wrapped ETH",
                "WETH",
                self.deployer,
                initial_balance,
                sender=self.deployer,
            )
            self.wbtc = project.MockERC20.deploy(
                "Wrapped BTC",
                "WBTC",
                self.deployer,
                initial_balance,
                sender=self.deployer,
            )


def main():
    network_config = NetworkConfig()
    deployer = network_config.deployer
    token_addresses = [network_config.weth, network_config.wbtc]
    price_feed_addresses = [
        network_config.weth_usd_price_feed,
        network_config.wbtc_usd_price_feed,
    ]

    dsc = project.DSC.deploy(sender=deployer)
    dsc_engine = project.DSCEngine.deploy(
        token_addresses, price_feed_addresses, dsc, sender=deployer
    )
    dsc.transferOwnership(dsc_engine, sender=deployer)
