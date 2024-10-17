from common.init_sqlalchemy import Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey


class SiteFuncStatus(Base):
    __tablename__ = 'site_func_status'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='功能ID')
    site_id = Column(Integer, ForeignKey("site_key_info.site_id"), comment='站点ID')
    site_host = Column(String(255), comment='站点URL')
    func_id = Column(Integer, ForeignKey("site_func_info.func_id"), comment='功能ID')
    func_name = Column(String(255), comment='功能名称')
    func_status = Column(String(255), comment='key')
    update_time = Column(DateTime)
