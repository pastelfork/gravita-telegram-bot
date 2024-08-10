import os
from dotenv import load_dotenv

load_dotenv()

chain_configs = {
    "mainnet": {
        "rpc_url": os.environ["MAINNET_RPC"],
        "chain_id": 1,
        "explorer_url_base": "https://etherscan.io",
        "contracts": {
            "pricefeed": "0x89F1ecCF2644902344db02788A790551Bb070351",
            "sorted_vessel": "0xF31D88232F36098096d1eB69f0de48B53a1d18Ce",
            "vessel_manager": "0xdB5DAcB1DFbe16326C3656a88017f0cB4ece0977",
            "vessel_manager_ops": "0xc49B737fa56f9142974a54F6C66055468eC631d0",
            "borrower_ops": "0x2bCA0300c2aa65de6F19c2d241B54a445C9990E2",
        },
        "collaterals": {
            "wstETH": "0x7f39c581f595b53c5cb19bd0b3f8da6c935e2ca0",
            "rETH": "0xae78736cd615f374d3085123a210448e74fc6393",
            "weETH": "0xcd5fe23c85820f7b72d0926fc9b05b43e359b7ee",
            "sfrxETH": "0xac3e018457b222d93114458476f3e3416abbe38f",
            "WETH": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
            "swETH": "0xf951e335afb289353dc249e82926178eac7ded78",
            "osETH": "0xf1c9acdc66974dfb6decb12aa385b9cd01190e38",
        },
        "ltv_thresholds": {
            "wstETH": 85,
            "rETH": 85,
            "weETH": 80,
            "sfrxETH": 80,
            "WETH": 90,
            "swETH": 80,
            "osETH": 80,
        },
    },
    "arbitrum": {
        "rpc_url": os.environ["ARBITRUM_RPC"],
        "chain_id": 42161,
        "explorer_url_base": "https://arbiscan.io",
        "contracts": {
            "pricefeed": "0xF0e0915D233C616CB727E0b2Ca29ff0cbD51B66A",
            "sorted_vessel": "0xc49B737fa56f9142974a54F6C66055468eC631d0",
            "vessel_manager": "0x6AdAA3eBa85c77e8566b73AEfb4C2f39Df4046Ca",
            "vessel_manager_ops": "0x15f74458aE0bFdAA1a96CA1aa779D715Cc1Eefe4",
            "borrower_ops": "0x89F1ecCF2644902344db02788A790551Bb070351",
        },
        "collaterals": {
            "wstETH": "0x5979d7b546e38e414f7e9822514be443a4800529",
            "rETH": "0xEC70Dcb4A1EFa46b8F2D97C310C9c4790ba5ffA8",
            "weETH": "0x35751007a407ca6feffe80b3cb397736d2cf4dbe",
            "sfrxETH": "0x95ab45875cffdba1e5f451b950bc2e42c0053f39",
            "WETH": "0x82af49447d8a07e3bd95bd0d56f35241523fbab1",
        },
        "ltv_thresholds": {
            "wstETH": 85,
            "rETH": 85,
            "weETH": 80,
            "sfrxETH": 80,
            "WETH": 90,
        },
    },
    "linea": {
        "rpc_url": os.environ["LINEA_RPC"],
        "chain_id": 59144,
        "explorer_url_base": "https://lineascan.build",
        "contracts": {
            "pricefeed": "0xAD1B9867BEFD148c9476B9Dd1e7C749bFcefbB2e",
            "sorted_vessel": "0xF0e0915D233C616CB727E0b2Ca29ff0cbD51B66A",
            "vessel_manager": "0xdC44093198ee130f92DeFed22791aa8d8df7fBfA",
            "vessel_manager_ops": "0x53525a62e55B6002792B993a2C27Af70d12443e4",
            "borrower_ops": "0x40E0e274A42D9b1a9D4B64dC6c46D21228d45C20",
        },
        "collaterals": {
            "wstETH": "0xb5bedd42000b71fdde22d3ee8a79bd49a568fc8f",
            "weETH": "0x1bf74c010e6320bab11e2e5a532b5ac15e0b8aa6",
            "WETH": "0xe5d7c2a44ffddf6b295a15c148167daaaf5cf34f",
        },
        "ltv_thresholds": {"wstETH": 85, "weETH": 80, "WETH": 90},
    },
    "mantle": {
        "rpc_url": os.environ["MANTLE_RPC"],
        "chain_id": 5000,
        "explorer_url_base": "https://explorer.mantle.xyz",
        "contracts": {
            "pricefeed": "0x53525a62e55B6002792B993a2C27Af70d12443e4",
            "sorted_vessel": "0x15f74458aE0bFdAA1a96CA1aa779D715Cc1Eefe4",
            "vessel_manager": "0x5C3B45c9F9C6e3d37De94BC03318622D3DD3f525",
            "vessel_manager_ops": "0x10308774e482e16671d8DCc847AC6b701f516611",
            "borrower_ops": "0xdB5DAcB1DFbe16326C3656a88017f0cB4ece0977",
        },
        "collaterals": {
            "mETH": "0xcDA86A272531e8640cD7F1a92c01839911B90bb0",
            "WETH": "0xdEAddEaDdeadDEadDEADDEAddEADDEAddead1111",
        },
        "ltv_thresholds": {"mETH": 80, "WETH": 90},
    },
    "optimism": {
        "rpc_url": os.environ["OPTIMISM_RPC"],
        "chain_id": 10,
        "explorer_url_base": "https://optimistic.etherscan.io",
        "contracts": {
            "pricefeed": "0x15f74458aE0bFdAA1a96CA1aa779D715Cc1Eefe4",
            "sorted_vessel": "0x0D2c4aE1859c4F8BFd47755d52cE844B26cb2a09",
            "vessel_manager": "0x40E0e274A42D9b1a9D4B64dC6c46D21228d45C20",
            "vessel_manager_ops": "0x5Bd5b45f6565762928A79779F6C2DD43c15c92EE",
            "borrower_ops": "0x82e34E39126190e622EBb2801e047D587AC94c5D",
        },
        "collaterals": {
            "wstETH": "0x1f32b1c2345538c0c6f582fcb022739c4a194ebb",
            "weETH": "0x9bcef72be871e61ed4fbbc7630889bee758eb81d",
            "WETH": "0x4200000000000000000000000000000000000006",
        },
        "ltv_thresholds": {"wstETH": 85, "weETH": 80, "WETH": 90},
    },
    "polygonzkevm": {
        "rpc_url": os.environ["POLYGONZKEVM_RPC"],
        "chain_id": 1101,
        "explorer_url_base": "https://zkevm.polygonscan.com",
        "contracts": {
            "pricefeed": "0x5C3B45c9F9C6e3d37De94BC03318622D3DD3f525",
            "sorted_vessel": "0x40E0e274A42D9b1a9D4B64dC6c46D21228d45C20",
            "vessel_manager": "0x57a1953bF194A1EF73396e442Ac7Dc761dCd23cc",
            "vessel_manager_ops": "0x9D8bB5496332cbeeD59f1211f28dB8b5Eb214B6D",
            "borrower_ops": "0xC818f878F27D0273Fb53B71d281C82921F0aF15c",
        },
        "collaterals": {
            "rETH": "0xb23C20EFcE6e24Acca0Cef9B7B7aA196b84EC942",
            "WETH": "0x4F9A0e7FD2Bf6067db6994CF12E4495Df938E6e9",
        },
        "ltv_thresholds": {"rETH": 85, "WETH": 90},
    },
    "zksync": {
        "rpc_url": os.environ["ZKSYNC_RPC"],
        "chain_id": 324,
        "explorer_url_base": "https://explorer.zksync.io",
        "contracts": {
            "pricefeed": "0x086D0981204b3e603Bf8b70D42680DA10b4dDa31",
            "sorted_vessel": "0x48dF3880Be9dFAAC56960325FA9a32B31fd351EA",
            "vessel_manager": "0x8D9CDd9372740933702d606EaD3BB55dFfDC6303",
            "vessel_manager_ops": "0x03569d4c117f94e72e9f63B06F406c5bc7caddE9",
            "borrower_ops": "0xd085Fd2338Cefb9cBD212F74d479072C1E7A25bf",
        },
        "collaterals": {
            "wstETH": "0x703b52f2b28febcb60e1372858af5b18849fe867",
            "WETH": "0x5aea5775959fbc2557cc8789bc1bf90a239d9a91",
        },
        "ltv_thresholds": {"wstETH": 85, "WETH": 90},
    },
}