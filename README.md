
<p align="center">
	<a href="https://github.com/trunghieult1807/telegram-airdop" target="_blank"><img src="https://github.com/trunghieult1807/telegram-airdop/blob/60af117ab84592acc067558c6f2ccf2d0cd691a0/assets/logo.png?raw=true" height="100"></a>
</p>

<p align="center">
    <a href="https://www.python.org/downloads/release/python-3100/"><img src="https://img.shields.io/badge/python-3.10-blue.svg?style=plastic" alt="Python version"></a>
    <a href="https://github.com/trunghieult1807/telegram-airdop/blob/19ade5543c0c9be0d72055fd808915dcf82c939f/LICENSE"><img src="https://img.shields.io/github/license/trunghieult1807/telegram-airdop?style=plastic" alt="GitHub license"></a>
    <a href="https://github.com/trunghieult1807/telegram-airdop/issues"><img src="https://img.shields.io/github/issues/trunghieult1807/telegram-airdop?style=plastic" alt="GitHub issues"></a>
    <a href="https://github.com/trunghieult1807/telegram-airdop/pulls"><img src="https://img.shields.io/github/issues-pr/trunghieult1807/telegram-airdop?style=plastic" alt="GitHub pull requests"></a>
    <br /><a href="https://github.com/trunghieult1807/telegram-airdop/stargazers"><img src="https://img.shields.io/github/stars/trunghieult1807/telegram-airdop?style=social" alt="GitHub stars"></a>
    <a href="https://github.com/trunghieult1807/telegram-airdop/network/members"><img src="https://img.shields.io/github/forks/trunghieult1807/telegram-airdop?style=social" alt="GitHub forks"></a>
    <a href="https://github.com/trunghieult1807/telegram-airdop/watchers"><img src="https://img.shields.io/github/watchers/trunghieult1807/telegram-airdop?style=social" alt="GitHub watchers"></a>
</p>

[![Static Badge](https://img.shields.io/badge/Telegram-Bot%20Link-Link?style=for-the-badge&logo=Telegram&logoColor=white&logoSize=auto&color=blue)](https://t.me/BybitCoinsweeper_Bot?start=referredBy=5268227136)
[![Static Badge](https://img.shields.io/badge/Telegram-Channel-Link?style=for-the-badge&logo=Telegram&logoColor=white&logoSize=auto&color=blue)](https://t.me/EwwMD)

#  Bot for BybitCoinsweeper

![start-coinsweep](https://github.com/user-attachments/assets/935f66e9-0af7-4ac6-a97a-d61439a89aa0)


# 🔥🔥 PYTHON version must be 3.10 - 3.11.5 🔥🔥

## Features  
| Feature                                            	        |  Supported  |
|---------------------------------------------------------------|:-----------:|
| Multithreading                                                |     ✔️     |
| Proxy binding to session                                      |     ✔️     |
| Auto ref                                                      |     ✔️     |
| Auto play game                                                |     ✔️     |
| Support for pyrogram .session			                        |     ✔️     |

## Settings
| Settings                   | Description                                                                            |
|----------------------------|----------------------------------------------------------------------------------------|
| **API_ID / API_HASH**      | Platform data from which to run the Telegram session (default - android)               |       
| **REF_LINK**               | Put your ref link here                                                                 |
| **AUTO_PLAY**              | Auto play game (default: True)                                                         |
| **GAME_PLAY_EACH_ROUND**   | Random number of game play in one round (default: [2, 4])                              |
| **TIME_PLAY_EACH_GAME**    | Random time in seconds to play each game (default: [130, 180])                         |
| **USE_PROXY_FROM_FILE**    | Whether to use a proxy from the bot/config/proxies.txt file (default: False)           |


## Quick Start 📚

To fast install libraries and run bot - open `run.bat` on **Windows** or `run.sh` on **Linux**

## Prerequisites
Before you begin, make sure you have the following installed:
- [**Python**](https://www.python.org/downloads/release/python-3100/) **version 3.10**

## Obtaining API Keys
1. Go to [**my.telegram.org**](https://my.telegram.org/auth) and log in using your phone number.
2. Select `API development tools` and fill out the form to register a new application.
3. Record the `API_ID` and `API_HASH` provided after registering your application in the `.env` file.

## Installation
You can download the [**repository**](https://github.com/Cybertat1on/BybitCoinsweeper) by cloning it to your system and installing the necessary dependencies:
```shell
git clone https://github.com/Cybertat1on/BybitCoinsweeper.git
cd BybitCoinsweeper
```

Then you can do automatic installation by typing:

Windows:
```shell
run.bat
```

Linux:
```shell
run.sh
```

# Linux manual installation
```shell
sudo sh install.sh
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
cp .env-example .env
nano .env  # Here you must specify your API_ID and API_HASH, the rest is taken by default
python3 main.py
```

You can also use arguments for quick start, for example:
```shell
~/BybitCoinsweeper >>> python3 main.py --action (1/3)
# Or
~/BybitCoinsweeper >>> python3 main.py -a (1/3)

# 1 - Run clicker
# 2 - Creates a session
# 3 - Run clicker (Query)
```

# Windows manual installation
```shell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env-example .env
# Here you must specify your API_ID and API_HASH, the rest is taken by default
python main.py
```

You can also use arguments for quick start, for example:
```shell
~/BybitCoinsweeper >>> python main.py --action (1/3)
# Or
~/BybitCoinsweeper >>> python main.py -a (1/3)

# 1 - Run clicker
# 2 - Creates a session
# 3 - Run clicker (Query)
```
# Termux manual installation
```
> pkg update && pkg upgrade -y
> pkg install python rust git -y
> git clone https://github.com/trunghieult1807/telegram-airdop.git
> cd BybitCoinsweeper
> pip install -r requirements.txt
> python main.py
```

You can also use arguments for quick start, for example:
```termux
~/BybitCoinsweeper > python main.py --action (1/2)
# Or
~/BybitCoinsweeper > python main.py -a (1/2)

# 1 - Run clicker
# 2 - Creates a session 
```

***

