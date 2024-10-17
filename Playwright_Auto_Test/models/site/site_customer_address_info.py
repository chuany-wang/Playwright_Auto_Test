from common.init_sqlalchemy import Base
from sqlalchemy import Column, String, Integer, DateTime


class SiteCustomerAddInfo(Base):
    __tablename__ = 'site_customer_address_info'
    site_id = Column(Integer, primary_key=True, comment='站点ID')
    site_host = Column(String(255), comment='站点URL')
    country_id = Column(String(255), comment='国家ID')
    zone_id = Column(String(255), comment='ZoneID')
    address_id = Column(String(255), comment='AddressID')
    update_time = Column(DateTime)
