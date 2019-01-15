from src.CoinMetrics import CoinMetrics
import time
import getopt
import query
import sys


def update_database(asset=None):
    cm = CoinMetrics(asset=asset)
    cm.update_database()

def usage():
    print("usage: python update_database.py")
    print("========================================================")
    print("-h: print this message")
    print("-a: asset name, abbreviation of the crypto currency")
    print("    Bitcoin: btc")
    print("    Etherium: eth")
    print("    Etherium Classic: etc")
    print("    Litecoin: ltc")
    print("    Bitcoin Cash: bch")
    print("    Desired asset should be separated by comma: btc,ltc,bch,eth,etc")
    print("========================================================")





if __name__ == "__main__":
    opts,args = getopt.getopt(sys.argv[1:], "a:h", ["help", "asset"])  
    asset= None
    for opt, content in opts:
        if opt in ["-a", "--asset"]:
            asset = content.split(",")
        elif opt in ["-h", "--help"]:
            usage()
    update_database(asset=asset)