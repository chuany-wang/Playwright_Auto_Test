from common.init_sqlalchemy import db
from sqlalchemy import func
from common.lo_logger import logger
from common.commom_api import update_data
from models.site.site_func_status import SiteFuncStatus
from models.site.site_key_info import SiteKey
from datetime import datetime
from models.site.site_func_info import SiteFunc
from sqlalchemy import text


def update_func_status():
    count = db.query(func.count(SiteFuncStatus.site_id)).scalar()
    db.query(SiteFuncStatus).delete()
    logger.info(f"清空站点模块状态历史数据{count}条")
    db.execute(text("ALTER TABLE site_func_status AUTO_INCREMENT = 1"))
    data_status = update_data(data='status', envir=None)
    statu = []
    for status in data_status:
        site_host = status.get('site_host')
        site = db.query(SiteKey).filter_by(site_host=site_host).first()
        func_key = status.get('func_name')
        site_func = db.query(SiteFunc).filter_by(func_key=func_key).first()
        func_status = status.get('func_statu')
        statu.append(
            SiteFuncStatus(site_id=site.site_id, site_host=site_host, func_name=site_func.func_name,
                           func_id=site_func.func_id,
                           func_status=func_status, update_time=datetime.now()))

    db.add_all(statu)
    db.commit()
    logger.info(f"已更新所有站点模块功能状态{len(statu)}条")


if __name__ == '__main__':
    update_func_status()
