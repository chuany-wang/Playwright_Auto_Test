from common.init_sqlalchemy import Base
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey


class SiteCheckCacheStatu(Base):
    __tablename__ = 'site_check_cache_status'
    site_id = Column(Integer, ForeignKey("site_key_info.site_id"), primary_key=True, autoincrement=True,
                     comment='站点ID')
    site_host = Column(String(255), comment='站点URL')
    api_order_id = Column(String(255), comment='站点URL')
    db_order_id = Column(String(255), comment='功能名称')
    status = Column(String(255), comment='key')
    update_time = Column(DateTime)
