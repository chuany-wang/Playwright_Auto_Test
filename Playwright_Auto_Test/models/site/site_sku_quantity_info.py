from common.init_sqlalchemy import Base
from sqlalchemy import Column, String, Integer, DateTime


class SiteSkuQuantity(Base):
    __tablename__ = 'site_sku_quantity_info'
    site_id = Column(Integer, primary_key=True, autoincrement=True, comment='站点ID')
    site_host = Column(String(255), comment='站点URL')
    site_sku = Column(String(255), comment='pc端主题')
    product_id = Column(Integer, comment='产品ID')
    quantity = Column(String(255), comment='产品数量')
    keyword = Column(String(255), comment='产品seo')
    update_time = Column(DateTime)
