from common.init_sqlalchemy import Base
from sqlalchemy import Column, String, Integer, Text


#
#
class SiteFunc(Base):
    __tablename__ = 'site_func_info'
    func_id = Column(Integer, primary_key=True, autoincrement=True, comment='功能ID')
    func_name = Column(String(255), comment='功能名称')
    func_key = Column(Text, comment='key')
