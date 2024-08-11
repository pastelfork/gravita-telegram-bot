# Gravita Telegram Bot

This repository contains a Telegram notification bot for users to monitor their vaults on Gravita Protocol across multiple chains.

## Prerequisites

- Websocket RPC endpoints for all chains Gravita is deployed on
- MongoDB connection string
- Telegram Bot API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/gravita-telegram-bot.git
cd gravita-telegram-bot
```
2. Create a virtual environment and activate it:
```bash
python -m venv venv source venv/bin/activate
```
3. Install the required packages:
```bash
pip install -r requirements.txt
```
4. Set up the environment variables:
```bash
cp .env.example .env
```
Edit the `.env` file and fill in your RPC endpoints, MongoDB connection string, and Telegram Bot API key.

## Usage

To run the bot, you need to execute two Python files:

1. Start the Telegram bot:
```bash
python main.py
```
2. In a separate terminal, run the blockchain event listener:
```python
python query.py
```


## Features

- Users can register their wallet addresses with the bot
- Real-time notifications for liquidations and redemptions against user's vessels
- Supports multiple chains: Mainnet, Arbitrum, Linea, Mantle, Optimism, Polygon zkEVM, and zkSync

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
