from common.init_sqlalchemy import Base
from sqlalchemy import Column, String, Integer,  ForeignKey


class SiteDatabase(Base):
    __tablename__ = 'site_database_info'
    site_id = Column(Integer, ForeignKey("site_key_info.site_id"), primary_key=True, autoincrement=True,
                     comment='站点ID')
    site_host = Column(String(255), comment='站点URL')
    pro_db = Column(String(255), comment='生产站点数据库')
    pro_host = Column(String(255), comment='生产站点数据库ip')
    user = Column(String(255), comment='用户名')
    password = Column(String(255), comment='密码')
