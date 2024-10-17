from sqlalchemy import func
from datetime import datetime
from common.lo_logger import logger
from common.init_sqlalchemy import db
from models.site.site_key_info import SiteKey
from common.ssh_db import get_all_site_data_from_db
from models.site.site_sku_quantity_info import SiteSkuQuantity


def check_quantity():
    sql = ("SELECT op.sku,op.quantity,op.product_id,osu.keyword "
           "FROM oc_product AS op "
           "JOIN oc_product_description AS opd ON op.product_id = opd.product_id "
           "JOIN oc_language AS ol ON opd.language_id = ol.language_id "
           "JOIN oc_setting AS os ON ol.CODE = os.`value` AND os.`key` = 'config_language' "
           "JOIN oc_seo_url AS osu ON opd.language_id = osu.language_id "
           "WHERE op.STATUS = 1 AND osu.`query` = CONCAT('product_id=', op.product_id) ORDER BY op.quantity DESC LIMIT 1")

    list_db = []
    results = get_all_site_data_from_db(sql=sql)
    for result in results:
        if result[1]:
            res_dict = {"site_host": result[0],
                        "site_sku": result[1][0].get('sku'),
                        "quantity": result[1][0].get('quantity'),
                        "keyword": result[1][0].get('keyword'),
                        "product_id": result[1][0].get('product_id')
                        }
            list_db.append(res_dict)
        else:
            logger.error(f"{result[0]} 站点获取产品数据有误，及时处理")
    return list_db


def update_quantity():
    count = db.query(func.count(SiteSkuQuantity.site_id)).scalar()
    db.query(SiteSkuQuantity).delete()
    logger.info(f"清空站点商品库存历史数据{count}条")
    data_sku = check_quantity()
    sku_task = []
    for sku in data_sku:
        site_host = sku.get('site_host')
        site = db.query(SiteKey).filter_by(site_host=site_host).first()
        site_sku = sku.get('site_sku')
        quantity = sku.get('quantity')
        keyword = sku.get('keyword')
        product_id = sku.get('product_id')
        update_time = datetime.now()
        sku_task.append(
            SiteSkuQuantity(
                site_id=site.site_id,
                site_host=site_host,
                site_sku=site_sku,
                product_id=product_id,
                quantity=quantity,
                keyword=keyword,
                update_time=update_time)
        )
    db.add_all(sku_task)
    db.commit()
    logger.info(f"已更新所有站点库存历史数据{len(sku_task)}条")


if __name__ == '__main__':
    update_quantity()
