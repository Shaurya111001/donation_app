import { TezosToolkit } from "@taquito/taquito"; 
import { TempleWallet } from "@temple-wallet/dapp";

import * as config from "./config.json"
export const setup = async () => {
    const Tezos = new TezosToolkit(config.rpc);
    return Tezos;
}

export const connectWallet = async () => {
    const available = await TempleWallet.isAvailable();
    if(!available) {
        throw new Error("Thanos Wallet not Connected");
    }
    const wallet = new TempleWallet(config.name);
    await wallet.connect( "carthagenet");
    return wallet;
}