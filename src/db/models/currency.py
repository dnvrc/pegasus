from src.db import Base, database_session
from src.db.model import Model

from sqlalchemy import Column, types, func

from dotmap import DotMap as DMObject


class _CurrencyModel(Base, Model):
    __tablename__ = 'currencies'
    name = Column(types.VARCHAR)
    slug = Column(types.VARCHAR)
    type = Column(types.VARCHAR)


Currency = DMObject(Model=_CurrencyModel)
