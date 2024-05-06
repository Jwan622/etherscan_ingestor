from sqlalchemy import Column, Integer, String, Index, BigInteger, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    address = Column(String(64), unique=True, nullable=False)
    transactions_sent = relationship("Transaction", foreign_keys="Transaction.from_address_id")
    transactions_received = relationship("Transaction", foreign_keys="Transaction.to_address_id")
    Index('idx_address', 'address', unique=True)


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    block_number = Column(BigInteger)
    time_stamp = Column(DateTime(timezone=True))
    hash = Column(String(66))
    from_address_id = Column(Integer, ForeignKey('addresses.id'))
    to_address_id = Column(Integer, ForeignKey('addresses.id'))
    value = Column(Numeric(precision=64, scale=0))
    gas = Column(Integer)
    gas_used = Column(Integer)
    is_error = Column(Integer)
    Index('idx_timestamp', 'time_stamp')
