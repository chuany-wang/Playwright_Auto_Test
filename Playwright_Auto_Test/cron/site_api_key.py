from datetime import datetime
from common.lo_logger import logger
from common.init_sqlalchemy import db
from models.site.site_key_info import SiteKey
from common.ssh_db import get_all_site_data_from_db


def check_api_key():
    sql = 'SELECT `key` FROM `oc_api` LIMIT 1'

    list_db = []
    results = get_all_site_data_from_db(sql=sql)
    for result in results:
        res_dict = {"site_host": result[0],
                    "site_key": result[1][0].get('key')
                    }
        list_db.append(res_dict)
    return list_db


def update_api_key():
    data_key = check_api_key()
    key_task = []
    for da in data_key:
        site_host = da.get('site_host')
        site_key = da.get('site_key')
        update_time = datetime.now()
        existing_key = db.query(SiteKey).filter_by(site_host=site_host).first()
        if existing_key != site_key:
            existing_key.site_key = site_key
            existing_key.update_time = update_time
        else:
            key_task.append(
                SiteKey(
                    site_host=site_host,
                    site_key=site_key,
                    update_time=update_time
                )
            )
    db.add_all(key_task)
    db.commit()
    logger.info(f"已更新所有站点api key数据{len(key_task) + db.query(SiteKey).count()}条")


if __name__ == '__main__':
    update_api_key()
