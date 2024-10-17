import re
import json
from common.lo_logger import logger
from common.init_dingding import dingding
from common.commom_api import update_data


def check_version(envir, ver: str):
    res = update_data(envir=envir, data='version')
    logger.info(f"接口返回的数据为{res}")
    mismatched_hosts = []

    for i in res:
        json_i = json.loads(i)
        version = json_i.get('iterative_version')
        host = re.search(r'https.*?index.php', json_i.get('dropdown_menu'))[0].replace('index.php', "")

        if version != ver:
            mismatched_hosts.append({'host': host, 'api_version': version})

    logger.debug(f"接口获取各站点的版本号不同的为{mismatched_hosts}")

    title = "### **版本检查已完成**"
    if len(mismatched_hosts) > 0:
        text = f'{title}\n\n' + "\n\n".join([
            f'<b>{host["host"]}</b>接口获取的版本为{host["api_version"]},与发版号{ver}不一致,请检查</font>'
            for host in mismatched_hosts])
    else:
        text = f'{title}\n\n<b>各站点的版本号为{ver},发版成功</font></b>'

    dingding(title=title, text=text, envir=envir)


if __name__ == '__main__':
    check_version(ver="v2.8", envir=None)
