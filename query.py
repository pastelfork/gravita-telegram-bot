import os
import time
import asyncio
import websockets

from dotenv import load_dotenv

from web3 import Web3, AsyncWeb3, WebSocketProvider
from eth_abi import decode

from pymongo import MongoClient

from telegram import Bot

from chain_configs import chain_configs

load_dotenv()
MONGODB_CONNECTION_URI = os.getenv("MONGODB_CONNECTION_URI")
TELEGRAM_KEY = os.getenv("TELEGRAM_KEY")


TOPICS = {
    'vessel_created':
        "0xc4acb8f55d18541d201c0e84984eacc725592d1043776db306c00720b2a503ff",
    'vessel_liquidated':
        "0x39bd24c0cc7c11940a19ed0ec77cf1a6d4ea1149f82d15a064003a7cbda7966a",
    'redemption': 
        "0x08b6f1ce3f9ab2722e8ea40c31a3e3a806a41702c5994f29af43dc0c1f2837df",
    'vessel_updated':
        "0xd03b2126581644d5026a8e77091b71644f3f16efe9d9e5930c4d533301c731e8"
}

class Deployment:
    def __init__(self, chain):
        self.chain: str = chain
        self.rpc_url: str = chain_configs[chain]["rpc_url"]
        self.explorer_url_base: str = chain_configs[chain]["explorer_url_base"]

    async def notify_users(self, borrowers_list, event_type):

        # MongoDB setup
        mongodb_client = MongoClient(MONGODB_CONNECTION_URI)
        db = mongodb_client['telegram_db']
        wallet_data = db['wallet_data']

        for i in borrowers_list:

            # Query MongoDB for user_id
            borrower_user_id_query = wallet_data.find_one({"wallet_address": i['borrower']})
            
            # If borrower is not a registered telegram bot user, skip
            if not borrower_user_id_query:
                continue
            else:
                borrower_user_id = borrower_user_id_query['user_id']
                # Send message to user
                bot = Bot(token=TELEGRAM_KEY)
                async with bot:
                    # Customize message based on event type
                    if event_type == 'liquidation':
                        message = f'Your Gravita vessel on {i['chain_name'].upper()} has been liquidated.'
                    if event_type == 'redemption':
                        message = f'Your Gravita vessel on {i['chain_name'].upper()} has been redeemed against.\nYou now have {Web3.from_wei(i['new_collateral'], "ether")} collateral asset.'
                    
                    # Send the message
                    await bot.send_message(text=f'{message} Txn hash: {self.explorer_url_base}/tx/{i["txn_hash"]}', 
                                           chat_id=borrower_user_id)

    async def process_redemption_events(self):

        async for w3 in AsyncWeb3(WebSocketProvider(self.rpc_url)):
            try:
                # Subscribe to redemption topic
                redemption_filter_params = {
                    'address': chain_configs[self.chain]['contracts']['vessel_manager_ops'],
                    'topics': [
                        TOPICS['redemption']
                    ]
                }

                await w3.eth.subscribe('logs', redemption_filter_params)
                
                # process messages
                async for message in w3.socket.process_subscriptions():
                    
                    # Process redemption events
                    redemption_event = message['result']
                    print(f'redemption_event:\n {redemption_event}\n\n')

                    redemption_txn_hash = Web3.to_hex(redemption_event['transactionHash'])
                    redemption_txn_receipt = await w3.eth.get_transaction_receipt(redemption_txn_hash)
                    redemption_logs = redemption_txn_receipt.logs
                    vessel_updated_events = [event for event in redemption_logs if Web3.to_hex(event.topics[0]) == TOPICS['vessel_updated']]
                    redeemed_vessels: list[dict] = []
                    for update in vessel_updated_events:
                        decoded_data = decode(['uint256', 'uint256', 'uint256', 'uint256'], update.data)
                        borrower = decode(['address'], update.topics[2])[0]
                        borrower = str(Web3.to_checksum_address(borrower))
                        redeemed_vessels.append(
                            {
                                'chain_name': self.chain,
                                'borrower': borrower,
                                'new_debt': decoded_data[0],
                                'new_collateral': decoded_data[1],
                                'txn_hash': redemption_txn_hash
                            }
                        )
                    await self.notify_users(redeemed_vessels, 'redemption')

            # Reconnect if connection is closed
            except websockets.ConnectionClosed:
                continue


    async def process_liquidation_events(self):

        async for w3 in AsyncWeb3(WebSocketProvider(self.rpc_url)):
            try:
                # Subscribe to topics
                liquidation_filter_params = {
                    'address': chain_configs[self.chain]['contracts']['vessel_manager_ops'],
                    'topics': [
                        TOPICS['vessel_liquidated']
                    ]
                }

                await w3.eth.subscribe('logs', liquidation_filter_params)
                
                # process messages
                async for message in w3.socket.process_subscriptions():
                    liquidation_event = message['result']
                    liquidated_borrowers: list[dict] = []
                    print(f'liquidation_event:\n {liquidation_event}\n\n')
                    liquidation_txn_hash = Web3.to_hex(liquidation_event['transactionHash'])
                    borrower = decode(['address'], liquidation_event.topics[2])[0]
                    borrower = str(Web3.to_checksum_address(borrower))
                    liquidated_borrowers.append(
                        {
                            'chain_name': self.chain,
                            'borrower': borrower,
                            'txn_hash': liquidation_txn_hash
                        }
                    )

                    await self.notify_users(liquidated_borrowers, 'liquidation')

            # Reconnect if connection is closed
            except websockets.ConnectionClosed:
                continue

async def main():
    print("Starting main function...")
    # Create instances of the class
    deployments = [
        Deployment(chain='mainnet'),
        Deployment(chain='arbitrum'),
        Deployment(chain='linea'),
        Deployment(chain='mantle'),
        Deployment(chain='optimism'),
        Deployment(chain='polygonzkevm'),
        Deployment(chain='zksync')
    ]

    print(f"Created {len(deployments)} deployment instances")

    tasks = []
    for deployment in deployments:
        print(f"Adding tasks for {deployment.chain}")
        tasks.append(deployment.process_redemption_events())
        tasks.append(deployment.process_liquidation_events())

    print(f"Total tasks created: {len(tasks)}")
    print("Starting asyncio.gather...")
    await asyncio.gather(*tasks)
    print("asyncio.gather completed")
if __name__ == '__main__':
    asyncio.run(main())
    