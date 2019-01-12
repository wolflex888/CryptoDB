import os
# coin type abbreviation
ABBRIVIATION = {
    "Bitcoin": "btc",
    "Bitcoin Cash": "bch",
    "Litecoin": "ltc",
    "Ethereum": "eth",
    "Ethereum Classic": "etc"
}

# data base parameters
DATABASE_USRNAME = os.environ['DATABASE_USRNAME']
DATABASE_PWD = os.environ['DATABASE_PWD']
DATABASE_NAME = os.environ['DATABASE_NAME']

# coin type code
COIN_CODE = {
    "btc": 0,
    "bch": 1,
    "ltc": 2,
    "eth": 3,
    "etc": 4
}