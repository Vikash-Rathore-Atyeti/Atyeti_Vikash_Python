from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
 
Base = declarative_base()
 
class InfoLog(Base):
    __tablename__ = 'info_logs'
    id = Column(Integer, primary_key=True)
    log_file = Column(String(255), nullable=False)
    info_frequency = Column(Integer, nullable=False)