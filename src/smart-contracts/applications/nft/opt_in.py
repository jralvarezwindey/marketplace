from pyteal import *
from pyteal_helpers import utils

def approval():
    # def has_rekeyed():
    #     return Assert(
    #         And(
    #             Global.group_size() == Int(2),
    #             Gtxn[].type_enum() == TxnType.Payment,
    #             Gtxn[0].sender() == Txn.sender(),
    #             Gtxn[0].receiver() == Txn.sender(),
    #             Gtxn[0].amount() == Int(0),
    #             Gtxn[0].rekey_to() == Global.current_application_address()
    #         )
    #     )

    delegated_address = Bytes("delegated_address")

    opt_in=Seq(
        App.localPut(Txn.sender(), delegated_address, Txn.application_args[0]),
        Approve()
    )

    nft_opt_in = Seq(
        # has_rekeyed(),
        InnerTxnBuilder.Begin(),
        Assert(App.localGet(Txn.accounts[1], Bytes("delegated_address")) == Txn.sender()),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.AssetTransfer,
            TxnField.xfer_asset: Txn.assets[0],
            TxnField.asset_sender: Txn.accounts[1],
            TxnField.asset_receiver: Txn.accounts[1],
            TxnField.asset_amount: Int(0),
        }),
        InnerTxnBuilder.Next(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.Payment,
            TxnField.sender: Txn.accounts[1],
            TxnField.receiver: Txn.accounts[1],
            TxnField.amount: Int(0),
            TxnField.rekey_to: Txn.accounts[1] 
        }),
        InnerTxnBuilder.Submit(),
        Approve()
    )
    return utils.events(init=Approve(), opt_in=opt_in, no_op=nft_opt_in)

def clear():
    return Approve()
