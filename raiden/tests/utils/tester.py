# -*- coding: utf8 -*-
from ethereum import tester
from ethereum.utils import decode_hex, privtoaddr, sha3

from raiden.channel import Channel, ChannelEndState
from raiden.blockchain.abi import (
    CHANNEL_MANAGER_ABI,
    NETTING_CHANNEL_ABI,
    HUMAN_TOKEN_ABI,
    REGISTRY_ABI,
)

# using an invalid key as the proxies default_key to force the user to set
# `sender`. The reason for this is that too many tests were mixing the wrong
# key, the alternative was to instantiate a proxy per key, which was adding to
# much code-bloat, using an invalid key we effectvelly disable the "feature" of
# the ABIContract to use a default key, making all the calls explicit, this is
# intentional!
INVALID_KEY = sha3('7')


def create_tokenproxy(tester_state, tester_token_address, tester_events):
    translator = tester.ContractTranslator(HUMAN_TOKEN_ABI)
    token_abi = tester.ABIContract(
        tester_state,
        translator,
        tester_token_address,
        log_listener=tester_events.append,
        default_key=INVALID_KEY,
    )
    return token_abi


def create_registryproxy(tester_state, tester_registry_address, tester_events):
    translator = tester.ContractTranslator(REGISTRY_ABI)
    registry_abi = tester.ABIContract(
        tester_state,
        translator,
        tester_registry_address,
        log_listener=tester_events.append,
        default_key=INVALID_KEY,
    )
    return registry_abi


def create_channelmanager_proxy(tester_state, tester_channelmanager_address, tester_events):
    translator = tester.ContractTranslator(CHANNEL_MANAGER_ABI)
    channel_manager_abi = tester.ABIContract(
        tester_state,
        translator,
        tester_channelmanager_address,
        log_listener=tester_events.append,
        default_key=INVALID_KEY,
    )
    return channel_manager_abi


def create_nettingchannel_proxy(tester_state, tester_nettingchannel_address, tester_events):
    translator = tester.ContractTranslator(NETTING_CHANNEL_ABI)
    netting_channel_abi = tester.ABIContract(
        tester_state,
        translator,
        tester_nettingchannel_address,
        log_listener=tester_events.append,
        default_key=INVALID_KEY,
    )
    return netting_channel_abi


def channel_from_nettingcontract(our_address, netting_contract, external_state, reveal_timeout):
    """ Create a `channel.Channel` for the `nettnig_contract`.

    Use this to make sure that both implementation (the smart contract and the
    python code) work in tandem.
    """
    asset_address_hex = netting_contract.assetAddress()
    settle_timeout = netting_contract.settleTimeout()
    address1_hex, balance1, address2_hex, balance2 = netting_contract.addressAndBalance()

    asset_address = decode_hex(asset_address_hex)
    address1 = decode_hex(address1_hex)
    address2 = decode_hex(address2_hex)

    if our_address == address1:
        our_balance = balance1
        partner_address = address2
        partner_balance = balance2
    else:
        our_balance = balance2
        partner_address = address1
        partner_balance = balance1

    our_state = ChannelEndState(
        our_address,
        our_balance,
    )
    partner_state = ChannelEndState(
        partner_address,
        partner_balance,
    )

    channel = Channel(
        our_state,
        partner_state,
        external_state,

        asset_address,
        reveal_timeout,
        settle_timeout,
    )

    return channel


def new_channelmanager(our_key, tester_state, tester_registry, tester_asset):
    channel_manager_address = tester_registry.addAsset(
        tester_token.address,
        sender=privatekey0,
    )
    tester_state.mine(number_of_blocks=1)


def new_nettingcontract(our_key, partner_key, tester_state,
                        tester_events, channelmanager, settle_timeout):

    netting_channel_address0_hex = channelmanager.newChannel(
        privtoaddr(partner_key),
        settle_timeout,
        sender=our_key,
    )
    tester_state.mine(number_of_blocks=1)

    nettingchannel_translator = tester.ContractTranslator(NETTING_CHANNEL_ABI)

    nettingchannel = tester.ABIContract(
        tester_state,
        nettingchannel_translator,
        netting_channel_address0_hex,
        log_listener=tester_events.append,
        default_key=INVALID_KEY,
    )

    return new_net
    return nettingchannel