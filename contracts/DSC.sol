// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {ERC20Burnable} from "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

contract DSC is ERC20Burnable, Ownable {
    error DSC__MustBeMoreThanZero();
    error DSC__BurnAmountExceedsBalance();
    error DSC__NotZeroAddress();

    constructor() ERC20("Decentralized Stable Coin", "DSC") Ownable(msg.sender) {}

    function burn(uint256 amount) public override onlyOwner {
        if (amount <= 0) {
            revert DSC__MustBeMoreThanZero();
        }
        uint256 balance = balanceOf(msg.sender);
        if (balance < amount) {
            revert DSC__BurnAmountExceedsBalance();
        }
        super.burn(amount);
    }

    function mint(address to, uint256 amount) external onlyOwner returns (bool) {
        if (to == address(0)) {
            revert DSC__NotZeroAddress();
        }
        if (amount <= 0) {
            revert DSC__MustBeMoreThanZero();
        }
        _mint(to, amount);
        return true;
    }
}
