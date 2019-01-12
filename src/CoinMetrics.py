#basic modules
import requests
import datetime
import json
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

#modules from requests specifically
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

#customized modules
from coinDB.model import *
from coinDB.config import *
from coinDB.db import *

class CoinMetrics:
    URL_BASE = "https://coinmetrics.io/api/v1/"
    def __init__(self, api_base_url = URL_BASE):
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
        self.avail_asset = ["btc", "bch", "ltc", "eth", "etc"]

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
            print(f)
            # f=f.replace("(usd)", "")
            d[f] = self.get_asset_data_for_time_range(asset=asset, data_type=f, begin=begin, end=end)
        return d
    def get_all_asset_data_for_time_range(self, asset=["btc", "bch", "ltc", "eth", "etc"], begin=0, end=0):
        d = {}
        print("asset: ", asset)
        for a in asset:
            d[a] = self.get_assets_everything(asset=a, begin=begin, end=end)
        return d
    def update_database(self):
        print("update sequence initiated.")
        print("obtaining data..")
        self.coin = self.get_all_asset_data_for_time_range(begin=self.prev_time, end=self.current_time)
        for coin_abb in self.coin:
            print(COIN_CODE[coin_abb])
if __name__ == "__main__":
    cm = CoinMetrics()
    cm.update_database()

