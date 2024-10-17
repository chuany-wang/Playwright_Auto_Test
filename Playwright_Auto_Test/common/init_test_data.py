"""
-*- coding: utf-8 -*-
@Author: wangcy
@E-mail:
@Time:
@Explain:
"""

from sqlalchemy import and_
from common.lo_logger import logger
from common.init_redis import re_db
from common.init_sqlalchemy import db
from models.site.site_func_info import SiteFunc
from models.site.site_theme_info import SiteTheme
from models.site.site_func_status import SiteFuncStatus
from models.site.site_sku_quantity_info import SiteSkuQuantity


def clear_cache():
    """清空缓存内容"""
    if re_db.flush_all():
        logger.info("清除缓存成功")
    else:
        logger.error("清除缓存失败")


def get_site_themes(envir, site_host):
    # 获取站点的主题信息
    if envir == "pro":
        return db.query(SiteTheme).filter(
            and_(~SiteTheme.site_host.like('%preview%'), ~SiteTheme.site_host.like('%test%'))
        ).all()
    elif envir == "dev":
        return db.query(SiteTheme).filter(SiteTheme.site_host.like('%preview%')).all()
    else:
        if site_host:
            return db.query(SiteTheme).filter_by(site_host=site_host).all()
        else:
            return db.query(SiteTheme).all()


def get_func_list(func_name):
    """获取功能列表"""
    if func_name:
        return db.query(SiteFunc).filter_by(func_name=func_name).all()
    else:
        return db.query(SiteFunc).all()


def get_site_func_status(func_id):
    """获取功能状态为1的站点host"""
    return db.query(SiteFuncStatus.site_host).filter(
        and_(SiteFuncStatus.func_id == func_id, SiteFuncStatus.func_status == 1)
    ).all()


def get_sku_quantities(envir, site_host):
    """获取站点产品数据"""
    if envir == "pro":
        return db.query(SiteSkuQuantity).filter(
            and_(~SiteSkuQuantity.site_host.like('%preview%'), ~SiteSkuQuantity.site_host.like('%test%'))
        ).all()
    elif envir == "dev":
        return db.query(SiteSkuQuantity).filter(SiteSkuQuantity.site_host.like('%preview%')).all()
    else:
        if site_host:
            return db.query(SiteSkuQuantity).filter_by(site_host=site_host).all()
        else:
            return db.query(SiteSkuQuantity).all()


def cache_site_data(key, value):
    """缓存站点数据"""
    if re_db.set_list(key=key, value=value, expiration=3600):
        logger.info(f"{key}相关数据写入缓存成功")
    else:
        logger.error(f"{key}相关数据写入缓存失败")


def init_data(envir=None, site_host=None, func_name=None):
    # 前置: 清空之前的缓存内容
    clear_cache()

    # 第0步: 获取站点所有的主题信息
    host_themes = get_site_themes(envir, site_host)
    theme_list = [{"site_host": theme.site_host, "pc_theme": theme.pc_theme,
                   "mobile_theme": theme.mobile_theme if theme.mobile_theme else 0} for theme in host_themes]

    # 第一步: 遍历所有的func_key
    func_list = get_func_list(func_name)
    list_func = [{'func_id': func.func_id, 'func_key': func.func_key} for func in func_list]

    # 第二步: 取站点func状态为1的站点host，使用func_id取，当func_id=8时取所有站点
    for func in list_func:
        func_id = func.get('func_id')
        func_key = func.get('func_key')

        if str(func_id) == "8":
            cache_site_data("common", theme_list)
        else:
            func_status_hosts = get_site_func_status(func_id)
            list_host_match = [the for the in theme_list if
                               any(fuc_sta.site_host == the.get('site_host') for fuc_sta in func_status_hosts)]

            if list_host_match:
                cache_site_data(func_key, list_host_match)
            else:
                logger.info(f"{func_key}无测试数据")

    # 第三步: 设置 cookies that seo & sku
    sku_quantities = get_sku_quantities(envir, site_host)
    dict_sku_quan = {quan.site_host: {'sku': quan.site_sku, 'keyword': quan.keyword} for quan in sku_quantities}

    if re_db.set_multiple(key_value_dict=dict_sku_quan, expiration=3600):
        logger.info(f"站点产品数据写入缓存成功")
    else:
        logger.error(f"站点产品数据写入缓存失败")


if __name__ == '__main__':
    # init_data(envir='test', site_host='https://www.cncest.com/uk/')
    # init_data(envir='test', site_host='https://test.cncest.com/uk/')
    init_data(envir='test', site_host='https://www.ririsircarlight.com/')
    # init_data(envir='test', site_host='https://www.kitneed.com/de/')
    # init_data(envir='test', site_host='https://www.cncest.com.es/')
    # init_data(envir='test', site_host='https://preview.cncest.com/')
    # init_data(envir='test')
