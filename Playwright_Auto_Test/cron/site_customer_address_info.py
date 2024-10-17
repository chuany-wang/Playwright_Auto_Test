from common.init_sqlalchemy import db
from common.ssh_db import get_all_site_data_from_db
from models.site.site_customer_address_info import SiteCustomerAddInfo
from models.site.site_key_info import SiteKey
from datetime import datetime
from common.basic import logger
from sqlalchemy import func


def check_site_country():
    sql = ("SELECT os.`value` AS country_id, oz.zone_id, res.address_id "
           "FROM oc_zone AS oz "
           "JOIN oc_setting AS os ON oz.country_id = os.value "
           "JOIN (SELECT oa.address_id FROM oc_customer AS ocu JOIN oc_address AS oa ON ocu.customer_id = oa.customer_id "
           "WHERE email = 'cncest.test@gmail.com' ORDER BY address_id DESC  LIMIT 1 ) AS res  "
           "WHERE oz.status = 1  AND oz.country_id = os.value  AND os.`key` = 'config_country_id' LIMIT 1")
    list_db = []
    results = get_all_site_data_from_db(sql=sql)
    for result in results:
        res_dict = {"site_host": result[0],
                    "country_id": result[1][0].get('country_id'),
                    "zone_id": result[1][0].get('zone_id'),
                    "address_id": result[1][0].get('address_id')
                    }
        list_db.append(res_dict)
    return list_db


def update_address():
    count = db.query(func.count(SiteCustomerAddInfo.site_id)).scalar()
    db.query(SiteCustomerAddInfo).delete()
    logger.info(f"清空站点国家地区数据{count}条")
    data_country = check_site_country()
    country_task = []
    for cou in data_country:
        site_host = cou.get('site_host')
        site = db.query(SiteKey).filter_by(site_host=site_host).first()
        country_id = cou.get('country_id')
        zone_id = cou.get('zone_id')
        address_id = cou.get('address_id')
        update_time = datetime.now()
        country_task.append(
            SiteCustomerAddInfo(
                site_id=site.site_id,
                site_host=site_host,
                country_id=country_id,
                zone_id=zone_id,
                address_id=address_id,
                update_time=update_time)
        )
        db.add_all(country_task)
        db.commit()
    logger.info(f"已更新站点国家地区数据数据{len(country_task)}条")


if __name__ == '__main__':
    update_address()
