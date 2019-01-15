import sys
import getopt
import time
import datetime
import re

from sqlalchemy import func

from src.coinDB.model import *
from src.coinDB.config import *
from src.coinDB.db import *

def usage():
    print("usage: python query.py")
    print("========================================================")
    print("-h: print this message")
    print("-a: asset name, abbreviation of the crypto currency")
    print()
    print("    Available crypto coin:")
    print("    Bitcoin: btc")
    print("    Etherium: eth")
    print("    Etherium Classic: etc")
    print("    Litecoin: ltc")
    print("    Bitcoin Cash: bch")
    print()
    print("-f: the target feature for the query. Multiple feature should be separated by comma(,)")
    print()
    print("    Available features:")
    print("    date, txvolume, adjustedtxvolume")
    print("    txcount, marketcap, price, exchangevolume")
    print("    realizedcap, generatedcoins, fees, activeaddresses")
    print("    averagedifficulty, paymentcount, mediantxvalue, medianfee, blocksize, blockcount")
    print()
    print("-b: begin of time range (MM-DD-YYYY)")
    print("-e: end of time range (MM-DD-YYYY)")
    print("========================================================")

    sys.exit(0)
def parse(result={}):
    for key in result:
        print("time_stamp\t%s"%(key))
        for element in result[key]:
            print("%s\t%s"%(datetime.datetime.fromtimestamp(element[0]).strftime("%m-%d-%Y"), element[1]))
        print("=================================================================================")

def check_date(date=None):
    if re.match(r"[0-9][0-9]-[0-9][0-9]-[0-9][0-9][0-9][0-9]", date):
        return True
    else:
        return False

class DB:
    def __init__(self, assets=None, time_begin=None, time_end=None, feature=None):

        self.begin = time_begin
        self.end = time_end
        self.coin_code = COIN_CODE[assets]
        DBSession = sessionmaker(bind=ENGINE)
        self.DBsession = DBSession()
        self.feature = feature
        self.feature_dict = {"activeaddress": active_address,
                        "adjustedtxvolume": adjusted_tx_volume,
                        "averagedifficulty": avg_difficulty,
                        "blockcount": block_count,
                        "blocksize": block_size,
                        "exchangevolume": exchange_volume,
                        "fees": fees,
                        "generatedcoins": generated_coins,
                        "marketcap": market_cap,
                        "medianfee": median_fee,
                        "mediantxvalue": median_tx_value,
                        "paymentcount": payment_count,
                        "price": price,
                        "realizedcap": realized_cap,
                        "txcount": tx_count,
                        "txvolume": tx_volume}
    def query(self):
        result = {}

        for curr_feature in self.feature:
            result[curr_feature] = []
            tmp_obj = self.feature_dict[curr_feature]
            for a, b in self.DBsession.query(coin_date, tmp_obj)\
                        .filter(coin_date.coin_type==self.coin_code)\
                        .filter(coin_date.entry_id==tmp_obj.entry_id)\
                        .filter(coin_date.unix_date > self.begin)\
                        .filter(coin_date.unix_date < self.end)\
                        .all():
                result[curr_feature].append([a.unix_date, b.value])

        return result


if __name__ == "__main__":  
    opts,args = getopt.getopt(sys.argv[1:], "a:f:t:b:e:h", ["help", "output=", "feature", "asset", "task", "begin", "end"])  
    asset, feature, task, begin, end = None, None, None, None, None
    for opt, content in opts:
        if opt in ["-a", "--asset"]:
            asset = content
        elif opt in ["-f", "--feature"]:
            feature = content.split(",")
        elif opt in ["-t", "--task"]:
            task = content
        elif opt in ["-b", "--begin"]:
            begin = content
        elif opt in ["-e", "--end"]:
            end = content
        elif opt in ["-h", "--help"]:
            usage()
            sys.exit(1)
    
    if asset is None:
        print()
        print("[Error]argument \"-a\" is reauired")
        print()
        usage()
        sys.exit(1)
    elif feature is None:
        print()
        print("[Error]argument \"-f\" is reauired")
        print()
        usage()
        sys.exit(1)
    elif task is None:
        print()
        print("[Error]argument \"-t\" is reauired")
        print()
        usage()
        sys.exit(1)
    elif begin is None:
        print()
        print("[Error]argument \"-b\" is reauired")
        print()
        usage()
        sys.exit(1)
    elif end is None:
        print()
        print("[Error]argument \"-e\" is reauired")
        print()
        usage()
        sys.exit(1)
    if check_date(begin):
        begin = time.mktime(datetime.datetime.strptime(begin, "%m-%d-%Y").timetuple())
    else:
        print()
        print("[Error]argument \"-b\" needs to follow the formate: MM-DD-YYYY")
        print()
        usage()
        sys.exit(1)
    
    if check_date(end):
        end = time.mktime(datetime.datetime.strptime(end, "%m-%d-%Y").timetuple())
    else:
        print()
        print("[Error]argument \"-e\" needs to follow the formate: MM-DD-YYYY")
        print()
        usage()
        sys.exit(1)
    

    qq = DB(assets=asset, time_begin=begin, time_end=end, feature=feature)
    result = qq.query()
    parse(result)