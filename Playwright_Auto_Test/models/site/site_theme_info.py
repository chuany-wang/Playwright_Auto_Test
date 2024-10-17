from common.init_sqlalchemy import Base
from sqlalchemy import Column, String, Integer, DateTime


class SiteTheme(Base):
    __tablename__ = 'site_theme_info'
    site_id = Column(Integer, primary_key=True, autoincrement=True, comment='站点ID')
    site_host = Column(String(255), comment='站点URL')
    pc_theme = Column(String(255), comment='pc端主题')
    mobile_theme = Column(String(255), comment='手机端端主题')
    update_time = Column(DateTime)
