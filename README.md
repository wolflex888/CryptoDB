# CryptoDB
The propose of this project is to design a automated script to update the database with the most current cryptocurrency data and obtain data from database.

## Environment variable

The script was written that the paramter of the database is obtained from the bash environment

`export DATABASE_USRNAME= <database username>`

`export DATABASE_PWD= <database password>`

`export DATABASE_NAME = <database name>`

## Setup

The required package is in requirement.txt. Run the following command in the application root directory

`pip install -r requirement.txt`

Following the installation above, run the following script:

`python create_database.py`

It will create a database named capital and create 17 tables included in it.

## Update database

The script automatically get the maximum time stamp from the database and set it as the start of the time range, and current time as the end of the time range.

To update the database to the current date:

`python update_database.py -a <desired update asset>`

The desired crypto coin should be separated with comma only

`default asset is btc,bch,ltc,eth,etc`

The initial run takes approximately 192 seconds. It takes 18.92 seconds to download the data from the CoinMetrics API, and 182.51 seconds to insert the rows into the database.


## Query 

The available feature: date, txvolume, adjustedtxvolume, txcount, marketcap, price, exchangevolume, realizedcap, generatedcoins, fees, activeaddresses, averagedifficulty, paymentcount, mediantxvalue, medianfee, blocksize, blockcount

The current version of script only support querying a set of features listed above with one type of crypto currency.

`python query.py -a <one desired crypto coin> -f <set of feature separated by comma> -t <task> (only here for future work) -b <begin of time range> -e <end of time range> -h < bool, print usage >`

The script will parse the dictionary and return the data in the following format:

|Date(MM-DD-YYYY)|Feature1|
|-----|---------|


`===================================================`

|Date(MM-DD-YYYY)|Feature2|
|-----|---------|

`===================================================`

# To be continued..