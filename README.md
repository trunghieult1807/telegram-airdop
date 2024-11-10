<p align="center">
	<a href="https://github.com/trunghieult1807/telegram-airdop" target="_blank"><img src="https://github.com/trunghieult1807/telegram-airdop/blob/60af117ab84592acc067558c6f2ccf2d0cd691a0/assets/logo.png?raw=true" height="100"></a>
</p>

<p align="center">
    <a href="https://www.python.org/downloads/release/python-3100/"><img src="https://img.shields.io/badge/python-3.11-blue.svg?style=plastic" alt="Python version"></a>
    <a href="https://github.com/trunghieult1807/telegram-airdop/blob/19ade5543c0c9be0d72055fd808915dcf82c939f/LICENSE"><img src="https://img.shields.io/github/license/trunghieult1807/telegram-airdop?style=plastic" alt="GitHub license"></a>
    <a href="https://github.com/trunghieult1807/telegram-airdop/issues"><img src="https://img.shields.io/github/issues/trunghieult1807/telegram-airdop?style=plastic" alt="GitHub issues"></a>
    <a href="https://github.com/trunghieult1807/telegram-airdop/pulls"><img src="https://img.shields.io/github/issues-pr/trunghieult1807/telegram-airdop?style=plastic" alt="GitHub pull requests"></a>
    <br /><a href="https://github.com/trunghieult1807/telegram-airdop/stargazers"><img src="https://img.shields.io/github/stars/trunghieult1807/telegram-airdop?style=social" alt="GitHub stars"></a>
    <a href="https://github.com/trunghieult1807/telegram-airdop/network/members"><img src="https://img.shields.io/github/forks/trunghieult1807/telegram-airdop?style=social" alt="GitHub forks"></a>
    <a href="https://github.com/trunghieult1807/telegram-airdop/watchers"><img src="https://img.shields.io/github/watchers/trunghieult1807/telegram-airdop?style=social" alt="GitHub watchers"></a>
</p>

[![Static Badge](https://img.shields.io/badge/Telegram-Channel-Link?style=for-the-badge&logo=Telegram&logoColor=white&logoSize=auto&color=blue)](https://t.me/EwwMD)

# 🔥🔥 PYTHON version must be `>=3.11` 🔥🔥

## Quick Start 📚

- To fast install libraries and run bot - open `run.bat` on **Windows** or `run.sh` on **Linux**
- **[Optional]**: If you use antiban detection, run [ANTIBAN SETUP](docs/ANTIBAN.md)

# Prerequisites

Before you begin, make sure you have the following installed:

- [**Python**](https://www.python.org/downloads/release/python-3110/) **version 3.11**

## Obtaining API Keys

1. Go to [**my.telegram.org**](https://my.telegram.org/auth) and log in using your phone number.
2. Select `API development tools` and fill out the form to register a new application.
3. Record the `API_ID` and `API_HASH` provided after registering your application in the `.env` file.

# Installation

You can download this [**repository**](https://github.com/trunghieult1807/telegram-airdop) and install by following methods:

## Docker installation **(RECOMMENDED)**

```shell
make build
make up
```

## Linux manual installation

```shell
sudo sh install.sh
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
cp .env-example .env
nano .env  # Here you must specify your API_ID and API_HASH, the rest is taken by default
python3 main.py
```

## Windows manual installation

```shell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env-example .env
# Here you must specify your API_ID and API_HASH, the rest is taken by default
python main.py
```

# Configure bots

See the supported features and settings

## [Blum](docs/BLUM.md)

| Feature                       | Supported |
| ----------------------------- | :-------: |
| Multithreading                |    ✔️     |
| Proxy binding to session      |    ✔️     |
| Auto ref                      |    ✔️     |
| Auto task complete            |    ✔️     |
| Auto play game                |    ✔️     |
| Support for pyrogram .session |    ✔️     |

## [Coinsweeper](docs/COINSWEEPER.md)

| Feature                       | Supported |
| ----------------------------- | :-------: |
| Multithreading                |    ✔️     |
| Proxy binding to session      |    ✔️     |
| Auto ref                      |    ✔️     |
| Auto play game                |    ✔️     |
| Support for pyrogram .session |    ✔️     |

## [OKX Racer](docs/OKX_RACER.md)

| Feature                       | Supported |
| ----------------------------- | :-------: |
| Multithreading                |    ✔️     |
| Proxy binding to session      |    ✔️     |
| Auto ref                      |    ✔️     |
| Auto task complete            |    ✔️     |
| Support for pyrogram .session |    ✔️     |
| Auto farming                  |    ✔️     |
| Auto boost                    |    ✔️     |
| Auto check in                 |    ✔️     |

## [Tomarket](docs/TOMARKET.md)

| Feature                       | Supported |
| ----------------------------- | :-------: |
| Multithreading                |    ✔️     |
| Proxy binding to session      |    ✔️     |
| Auto ref                      |    ✔️     |
| Auto task complete            |    ✔️     |
| Auto play game                |    ✔️     |
| Support for pyrogram .session |    ✔️     |
| Auto farming                  |    ✔️     |
| Automatic quest completion    |    ✔️     |
| Auto Daily Reward             |    ✔️     |
| Auto Claim Stars              |    ✔️     |
| Auto Claim Combo              |    ✔️     |
| Auto Rank Upgrade             |    ✔️     |

## If you use antiban detection, run [ANTIBAN SETUP](docs/ANTIBAN.md)
