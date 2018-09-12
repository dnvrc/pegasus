from src.db import Base, database_session
from src.db.model import Model

from sqlalchemy import Column, ForeignKey, types, func
from sqlalchemy.orm import relationship

from dotmap import DotMap as DMObject


class _ShareModel(Base, Model):
    __tablename__ = 'shares'
    currency_id = Column(types.INTEGER)
    currency_slug = Column(types.VARCHAR)
    marketcap = Column(types.BIGINT)
    price_usd = Column(types.DECIMAL)
    sent_in_usd = Column(types.DECIMAL)
    sent_by_address = Column(types.BIGINT)
    active_addresses = Column(types.BIGINT)
    block_size = Column(types.DECIMAL)
    block_time = Column(types.DECIMAL)
    difficulty = Column(types.DECIMAL)
    network_hashrate = Column(types.DECIMAL)
    transactions = Column(types.BIGINT)
    mining_profitability = Column(types.DECIMAL)
    median_transaction_fee = Column(types.DECIMAL)
    median_transaction_value = Column(types.DECIMAL)
    average_transaction_fee = Column(types.DECIMAL)
    average_transaction_value = Column(types.DECIMAL)
    social_tweets = Column(types.INTEGER)
    date = Column(types.DATETIME)

Share = DMObject(Model=_ShareModel)
