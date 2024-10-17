from common.init_sqlalchemy import db
from models.site.site_theme_info import SiteTheme
from models.site.site_key_info import SiteKey
from datetime import datetime
from common.basic import logger
from common.commom_api import update_data
from sqlalchemy import func


def update_theme():
    data_theme = update_data(data='theme', envir=None)
    count = db.query(func.count(SiteTheme.site_id)).scalar()
    db.query(SiteTheme).delete()
    logger.info(f"清空站点主题历史数据{count}条")
    themes = []
    for theme in data_theme:
        site_host = theme.get('host')
        site = db.query(SiteKey).filter_by(site_host=site_host).first()
        pc_themes = theme.get('pc_themes')
        mobile_status = theme.get('mobile_status')
        if mobile_status == "1":
            mobile_themes = theme.get('mobile_themes')
        else:
            mobile_themes = None
        themes.append(SiteTheme(site_id=site.site_id, site_host=site_host, pc_theme=pc_themes,
                                mobile_theme=mobile_themes, update_time=datetime.now()))

    db.add_all(themes)
    db.commit()
    logger.info(f"已更新所有站点主题历史数据{len(themes)}条")


if __name__ == '__main__':
    update_theme()
