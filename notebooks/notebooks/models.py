from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def db_connect():
    return create_engine('sqlite:///test_notebooks.db')


def create_table(engine):
    Base.metadata.create_all(engine)


class Computers(Base):
    __tablename__ = 'computers'

    id = Column(Integer, primary_key=True, autoincrement=True, comment="Идентификатор компьютера")
    url = Column(String(300), nullable=False, unique=False, comment="ссылка на страницу товара")
    visited_at = Column(DateTime, nullable=False, unique=False,  comment="время посещения страницы")
    name = Column(String(300), nullable=True, unique=False, comment="наименование товара")
    cpu_hhz = Column(Float, nullable=True, unique=False, comment="частота процессора, ГГЦ")
    ram_gb = Column(Integer, nullable=True, unique=False, comment="объем ОЗУ, Гб")
    ssd_gb = Column(Integer, nullable=True, unique=False, comment="Объем SSD, Гб")
    price_rub = Column(Integer, nullable=True, unique=False, comment="цена товара")
    rank = Column(Float, nullable=True, unique=False, comment="вычисляемый рейтинг")

    def __repr__(self):
        return "[id={0}, url={1}, visited_at={2}, name={3},cpu_hhz={4}," \
               " ram_gb={5},ssd_gb={6},price={7},rank={8}]".format(
            self.id,
            self.url,
            self.visited_at,
            self.name,
            self.cpu_hhz,
            self.ram_gb,
            self.ssd_gb,
            self.price,
            self.rank)
