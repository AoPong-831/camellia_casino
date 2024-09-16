#テーブルのカラム情報を定義するためのクラスを格納するファイル
from sqlalchemy import Column, Integer, String, Text, DateTime
from models.database import Base
from datetime import datetime

class Chip_database(Base):
    __tablename__ = "chip_database"
    id = Column(Integer, primary_key=True)
    name = Column(String(16), unique=True)
    birth = Column(String(4))
    chip = Column(Integer)
    money = Column(Integer)
    date = Column(DateTime, default=datetime.now())

    def __init__(self, name=None, birth=None, chip=0, money=0, date=None):
        self.name = name
        self.chip = chip
        self.birth = birth
        self.money = money
        self.date = date

    def __repr__(self):
        return '<Title %r>' % (self.title)