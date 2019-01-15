from .db import Base
from sqlalchemy import Column, Integer, String, JSON, Boolean, Enum, ForeignKey, Float, Date, DECIMAL, BigInteger, Numeric
from sqlalchemy.orm import relationship

# data of different cryptocoin includes the following column:
# date (unix time stamp integer), txVolumen (Float), adjustedTxVolumne(USD) (Float), txCount (Integer), marketcap (Float), price (Float)
# exchange Volume(integer), realized cap(float),  generated Coins(integer), fees(float), activeAddresses(integer), medianTxValue(float)
# medianFee (float), averageDifficulty(float), paymentCount(integer), blockSize(integer), BlockCount(integer)

class coin_date(Base):
    __tablename__ = "coin_date"
    coin_type = Column(Integer, unique = False, nullable = False)
    unix_date = Column(Integer, unique = False, nullable = False)
    entry_id = Column(Integer, unique = True, primary_key=True, autoincrement=True)
    #relationships
    tax_volume_r = relationship('tx_volume', backref='coin_date', lazy=True)
    adjusted_tax_volume_r = relationship('adjusted_tx_volume', backref='coin_date', lazy=True)
    tx_count_r = relationship('tx_count', backref="coin_date", lazy=True)
    market_cap_r = relationship('market_cap', backref="coin_date", lazy=True)
    price_r = relationship('price', backref="coin_date", lazy=True)
    exchange_volume_r = relationship('exchange_volume', backref='coin_date', lazy=True)
    realized_cap_r = relationship('realized_cap', backref="coin_date", lazy=True)
    generated_coins_r = relationship('generated_coins', backref="coin_date", lazy=True)
    fees_r = relationship('fees', backref='coin_date', lazy=True)
    active_address_r = relationship('active_address', backref='coin_date', lazy=True)
    median_tx_value_r = relationship('median_tx_value', backref='coin_date', lazy=True)
    median_fee_r = relationship('median_fee', backref='coin_date', lazy=True)
    avg_difficulty_r = relationship('avg_difficulty', backref='coin_date', lazy=True)
    payment_count_r = relationship('payment_count', backref='coin_date', lazy=True)
    block_size_r = relationship('block_size', backref='coin_date', lazy=True)
    block_count_r = relationship('block_count', backref='coin_date', lazy=True)

class tx_volume(Base): #float
    __tablename__="tx_volume"
    entry_id = Column(Integer, ForeignKey('coin_date.entry_id'), primary_key = True)
    value = Column(DECIMAL(23,6), nullable=False)

class adjusted_tx_volume(Base): #float
    __tablename__="adjusted_tx_volume"
    entry_id = Column(Integer, ForeignKey('coin_date.entry_id'), primary_key=True)
    value = Column(DECIMAL(23,6), nullable=False)

class tx_count(Base): #Integer
    __tablename__="tx_count"
    entry_id = Column(Integer, ForeignKey('coin_date.entry_id'), primary_key=True)
    value = Column(BigInteger, nullable=False)

class market_cap(Base): #float
    __tablename__="market_cap"
    entry_id = Column(Integer, ForeignKey('coin_date.entry_id'), primary_key=True)
    value = Column(DECIMAL(23,6), nullable=False)

class price(Base): #float
    __tablename__="price"
    entry_id = Column(Integer, ForeignKey('coin_date.entry_id'), primary_key=True)
    value = Column(DECIMAL(23,6), nullable=False)

class exchange_volume(Base): #integer
    __tablename__="exchange_volume"
    entry_id = Column(Integer, ForeignKey('coin_date.entry_id'), primary_key=True)
    value = Column(BigInteger, nullable=False)

class realized_cap(Base): #float
    __tablename__="realized_cap"
    entry_id = Column(Integer, ForeignKey('coin_date.entry_id'), primary_key=True)
    value = Column(DECIMAL(23,6), nullable=False)

class generated_coins(Base): #integer
    __tablename__="generated_coins"
    entry_id = Column(Integer, ForeignKey('coin_date.entry_id'), primary_key=True)
    value = Column(BigInteger, nullable=False)

class fees(Base): #float
    __tablename__="fees"
    entry_id = Column(Integer, ForeignKey('coin_date.entry_id'), primary_key=True)
    value = Column(DECIMAL(23,6), nullable=False)

class active_address(Base): #integer
    __tablename__="active_address"
    entry_id = Column(Integer, ForeignKey('coin_date.entry_id'), primary_key=True)
    value = Column(BigInteger, nullable=False)

class median_tx_value(Base): #float
    __tablename__="median_tx_value"
    entry_id = Column(Integer, ForeignKey('coin_date.entry_id'), primary_key=True)
    value = Column(DECIMAL(23,6), nullable=False)

class median_fee(Base): #float
    __tablename__="median_fee"
    entry_id = Column(Integer, ForeignKey('coin_date.entry_id'), primary_key=True)
    value = Column(DECIMAL(23,6), nullable=False)

class avg_difficulty(Base): #float
    __tablename__="avg_difficulty"
    entry_id = Column(Integer, ForeignKey('coin_date.entry_id'), primary_key=True)
    value = Column(DECIMAL(23,6), nullable=False)

class payment_count(Base): #integer
    __tablename__="payment_count"
    entry_id = Column(Integer, ForeignKey('coin_date.entry_id'), primary_key=True)
    value = Column(BigInteger, nullable=False)

class block_size(Base): #integer
    __tablename__="block_size"
    entry_id = Column(Integer, ForeignKey('coin_date.entry_id'), primary_key=True)
    value = Column(BigInteger, nullable=False)

class block_count(Base): #integer
    __tablename__="block_count"
    entry_id = Column(Integer, ForeignKey('coin_date.entry_id'), primary_key=True)
    value = Column(BigInteger, nullable=False)