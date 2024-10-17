from common.init_sqlalchemy import Base
from sqlalchemy import Column, String, Integer, Text, DateTime


class SiteKey(Base):
    __tablename__ = 'site_key_info'
    site_id = Column(Integer, primary_key=True, autoincrement=True, comment='站点ID')
    site_host = Column(String(255), comment='站点URL')
    site_key = Column(Text, comment='key')
    update_time = Column(DateTime)
