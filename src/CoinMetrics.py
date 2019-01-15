#basic modules
import requests
import datetime
import json
import time
import sys

#sqlalchemy essentials
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

#modules from requests specifically
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

#customized modules
from src.coinDB.model import *
from src.coinDB.config import *
from src.coinDB.db import *

    #######################################################
    ## ==== run time parameter for database update ===== ##
    ##     18.92251205444336 seconds to download data    ##
    ##    182.5061640739441 seconds to update database   ##
    ## ================================================= ##
    #######################################################

class CoinMetrics:
    URL_BASE = "https://coinmetrics.io/api/v1/"
    def __init__(self, api_base_url = URL_BASE, asset = ["btc", "bch", "ltc", "eth", "etc"]):
        self.api_base_url = api_base_url
        self.timeout = 120 # time limit
        self.current_time = int(time.time())
        self.APIsession = requests.Session()
        DBSession = sessionmaker(bind=ENGINE)
        self.DBsession = DBSession() 
        retries = Retry(total=5, backoff_factor = 0.5, status_forcelist = [502, 503, 504])
        self.APIsession.mount("http://", HTTPAdapter(max_retries=retries))
        self.prev_time = self.DBsession.query(func.max(coin_date.unix_date)).scalar()
        if self.prev_time is None:
            self.prev_time = 0
        if asset is None:
            self.avail_asset = ["btc", "bch", "ltc", "eth", "etc"]
        else:
            self.avail_asset = asset
        


    def __request(self, url):
        try:
            response = self.APIsession.get(url, timeout = self.timeout)
            response.raise_for_status()
            content=json.loads(response.content.decode('utf-8'))
            if 'error' in content:
                raise ValueError(content['error'])
            else:
                return content
        except Exception as e:
            raise

    def get_supported_asset(self):
        url = '{}get_supported_assets'.format(self.api_base_url)
        return self.__request(url)
    
    
    def get_available_data_type_for_asset(self, asset):
        url = '{}get_available_data_types_for_asset/{}'.format(self.api_base_url, asset)
        return self.__request(url)

    def get_asset_data_for_time_range(self, asset, data_type, begin, end):
        url = '{}get_asset_data_for_time_range/{}/{}/{}/{}'.format(self.api_base_url, asset, data_type, begin, end)

        return self.__request(url)
    def get_assets_everything(self, asset, begin, end) :
        feature = self.get_available_data_type_for_asset(asset=asset)
        d = {}
        # print(feature['result'])
        for f in feature["result"]:
            # print(f)
            # f=f.replace("(usd)", "")
            tmp_array = self.get_asset_data_for_time_range(asset=asset, data_type=f, begin=begin, end=end)
            for response in tmp_array["result"]:
                # dictionary structure : dictionary[timestamp][feature] = value
                if response[1] is None:
                    continue
                if response[0] in d:
                    d[response[0]][f] = response[1]
                else:
                    d[response[0]] = {}
                    d[response[0]][f] = response[1]
        return d
    def get_all_asset_data_for_time_range(self, asset=None, begin=0, end=0):
        d = {}
        # print("asset: ", asset)
        asset = self.avail_asset
        if asset is None:
            raise ValueError("Desired cryptocoin type not specified")
        for a in asset:
            print("grabbing asset: {}".format(a))
            d[a] = self.get_assets_everything(asset=a, begin=begin, end=end)
        return d
    def insert_database(self, value=None, entry_id=None, feature=None):
        if value is None or entry_id is None or feature is None:
            print(feature, value, entry_id)
            raise ValueError("missing essential value for database update. feature: {}, value: {}, entry_id: {}".format(feature, value, entry_id))
        if feature == "activeaddresses":
            new_row = active_address(entry_id=entry_id, value=value)
            self.DBsession.add(new_row)
            self.DBsession.commit()
        elif feature == "adjustedtxvolume(usd)":
            new_row = adjusted_tx_volume(entry_id=entry_id, value=value)
            self.DBsession.add(new_row)
            self.DBsession.commit()
        elif feature == "averagedifficulty":
            new_row = avg_difficulty(entry_id=entry_id, value=value)
            self.DBsession.add(new_row)
            self.DBsession.commit()
        elif feature == "blockcount":
            new_row = block_count(entry_id=entry_id, value=value)
            self.DBsession.add(new_row)
            self.DBsession.commit()
        elif feature == "blocksize":
            new_row = block_size(entry_id=entry_id, value=value)
            self.DBsession.add(new_row)
            self.DBsession.commit()
        elif feature == "exchangevolume(usd)":
            new_row = exchange_volume(entry_id=entry_id, value=value)
            self.DBsession.add(new_row)
            self.DBsession.commit()
        elif feature == "fees":
            new_row = fees(entry_id=entry_id, value=value)
            self.DBsession.add(new_row)
            self.DBsession.commit()
        elif feature == "generatedcoins":
            new_row = generated_coins(entry_id=entry_id, value=value)
            self.DBsession.add(new_row)
            self.DBsession.commit()
        elif feature == "marketcap(usd)":
            new_row = market_cap(entry_id=entry_id, value=value)
            self.DBsession.add(new_row)
            self.DBsession.commit()
        elif feature == "medianfee":
            new_row = median_fee(entry_id=entry_id, value=value)
            self.DBsession.add(new_row)
            self.DBsession.commit()
        elif feature == "mediantxvalue(usd)":
            new_row = median_tx_value(entry_id=entry_id, value=value)
            self.DBsession.add(new_row)
            self.DBsession.commit()
        elif feature == "paymentcount":
            new_row = payment_count(entry_id=entry_id, value=value)
            self.DBsession.add(new_row)
            self.DBsession.commit()
        elif feature == "price(usd)":
            new_row = price(entry_id=entry_id, value=value)
            self.DBsession.add(new_row)
            self.DBsession.commit()
        elif feature == "realizedcap(usd)":
            new_row = realized_cap(entry_id=entry_id, value=value)
            self.DBsession.add(new_row)
            self.DBsession.commit()
        elif feature == "txcount":
            new_row = tx_count(entry_id=entry_id, value=value)
            self.DBsession.add(new_row)
            self.DBsession.commit()
        elif feature == "txvolume(usd)":
            new_row = tx_volume(entry_id=entry_id, value=value)
            self.DBsession.add(new_row)
            self.DBsession.commit()
        else:
            raise ValueError("unexpected feature to insert into database: %s"%(feature))
            
    def update_database(self):
        print("update sequence initiated.")
        print("targeted crypto coin: %s"%(self.avail_asset))
        print("downloading data..")
        start_time = time.time()
        self.coin = self.get_all_asset_data_for_time_range(begin=self.prev_time, end=self.current_time)
        time_used = time.time() - start_time
        print("completed. time used to download data: ", time_used)
        print("inserting new data..")
        start_time = time.time()
        for coin_abb in self.coin:
            print("processing %s...."%(coin_abb))
            current_coin_code = COIN_CODE[coin_abb]
            for timestamp in self.coin[coin_abb]:
                new_row = coin_date(coin_type=current_coin_code, unix_date=timestamp)
                self.DBsession.add(new_row)
                self.DBsession.commit()
                # self.DBsession.refresh(new_row)
                current_entry_id = new_row.entry_id
                # print(current_entry_id)
                for feature in self.coin[coin_abb][timestamp]:
                    self.insert_database(value=self.coin[coin_abb][timestamp][feature], \
                                        entry_id=current_entry_id, \
                                        feature = feature)
        time_used = time.time() - start_time
        print("completed. time used to update data: ", time_used)
if __name__ == "__main__":
    print("this script is not meant to be executed directly. Exiting..")
    sys.exit(1)
    
    # d = cm.get_available_data_type_for_asset(asset="btc")
    # d = cm.get_assets_everything(asset="btc", begin=0, end=int(time.time()))
    # print(d)
