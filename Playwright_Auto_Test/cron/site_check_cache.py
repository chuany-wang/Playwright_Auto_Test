from common.lo_logger import logger
from common.commom_api import update_data
from common.ssh_db import get_all_site_data_from_db
from common.init_dingding import dingding


def check_cache(envir):
    sql = f"SELECT order_id,date_added FROM `oc_order` WHERE order_status_id = 17 ORDER BY date_added DESC LIMIT 1"
    list_db = []
    list_api = []
    compare_res = []
    logger.debug(f"开始从数据库中获取最新的订单数据")
    # 连接数据库获取最新的订单
    results = get_all_site_data_from_db(sql=sql, envir=envir)
    for result in results:
        res_dict = {"site_host": result[0], "db_order_id": str(result[1][0].get('order_id')) if result[1] else "Null"}
        list_db.append(res_dict)

    logger.debug(f"从数据库中获取最新的订单数据完成:{list_db}")

    # 获取接口中最新的订单
    logger.debug(f"开始从接口中获取最新的订单数据")
    order_api = update_data(data='order', envir=envir)
    for i in order_api:
        api_res = {"site_host": i.get('host'), "api_order_id": i.get('order_id') if i else "Null"}
        list_api.append(api_res)

    logger.debug(f"从接口中获取最新的订单数据完成:{list_api}")

    for i in list_db:
        for j in list_api:
            if i.get('site_host') == j.get('site_host'):
                if i.get('db_order_id') != j.get('api_order_id'):
                    fin = {"site_host": i.get('site_host'), "db_order_id": i.get('db_order_id'),
                           "api_order_id": j.get('api_order_id')}
                    compare_res.append(fin)
            else:
                pass
    title = '清除缓存测试'

    if len(compare_res) > 0:
        text = f"所有站点测试完成,异常数据:\n\n{compare_res}"
    else:
        text = f"所有站点缓存测试完成,接口与数据库返回的最新订单号一致，数据无异常"

    dingding(title=title, text=text, envir=envir)


if __name__ == '__main__':
    check_cache(envir=None)
