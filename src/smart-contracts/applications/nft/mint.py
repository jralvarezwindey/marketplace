from pyteal import *
from pyteal_helpers import utils


def approval():
    def set_nft_field(field: str, arg_index: Int):
        return If(Txn.application_args.length() >= arg_index + Int(1)).Then(
            If(Len(Txn.application_args[arg_index]) > Int(0)).Then(
                InnerTxnBuilder.SetField(TxnField[field], Txn.application_args[arg_index])
            )
        )

    mint = Seq(
        Assert(
            Txn.application_args.length() >= Int(5),
        ),
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.AssetConfig,
            TxnField.config_asset_name: Txn.application_args[0],
            TxnField.config_asset_unit_name: Txn.application_args[1],
            TxnField.config_asset_total: Btoi(Txn.application_args[2]),
            TxnField.config_asset_decimals: Btoi(Txn.application_args[3]),
            TxnField.config_asset_default_frozen: Btoi(Txn.application_args[4])
        }),
        set_nft_field("config_asset_manager", Int(5)),
        set_nft_field("config_asset_reserve", Int(6)),
        set_nft_field("config_asset_freeze", Int(7)),
        set_nft_field("config_asset_clawback", Int(8)),
        set_nft_field("config_asset_url", Int(9)),
        set_nft_field("config_asset_metadata_hash", Int(10)),
        InnerTxnBuilder.Submit(),
        Approve()
    )

    return utils.events(init=Approve(), no_op=mint)

def clear():
    return Approve()
