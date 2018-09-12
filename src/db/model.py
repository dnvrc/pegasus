from sqlalchemy import Column, types, func


class Model:
    id = Column(types.INTEGER, primary_key=True)
