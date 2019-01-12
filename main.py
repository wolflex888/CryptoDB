from src.util.CoinMetrics import CoinMetrics
from src.util.config import *
from src.database.model import *
import time


cm = CoinMetrics()
# assets = CoinMetrics().get_asset_data_for_time_range(asset=ABBRIVIATION['Litecoin'], data_type="medianfee", begin=0, end=1515282300)
assets = CoinMetrics().get_assets_everything(asset=ABBRIVIATION['Litecoin'], begin=0, end=1515282300)
# features = CoinMetrics().get_available_data_type_for_asset(asset=ABBRIVIATION['Litecoin'])
print(assets)

    





if __name__ == "__main__":
    cm=CoinMetrics()
    cm.update_database()