import json
import sys
from config import REPORT_DATA_DIR
from common.lo_logger import logger
from common.read_data import read_conf
from common.basic import format_current_datetime
from dingtalkchatbot.chatbot import DingtalkChatbot

current_os = sys.platform.lower()


def dingding(envir, title: str, text: str, is_at_all: bool = False) -> None:
    MSG = read_conf('MSG')
    if envir == 'pro':
        dingding_config = MSG.get('DINGDING_TEST')
    elif envir == 'dev':
        dingding_config = MSG.get('DINGDING_TEST')
    else:
        dingding_config = MSG.get('DINGDING_TEST')

    DINGDING_WEBHOOK = dingding_config.get('webhook')
    DINGDING_SECRET = dingding_config.get('secret')

    ding = DingtalkChatbot(webhook=DINGDING_WEBHOOK, secret=DINGDING_SECRET)
    ding.send_markdown(title=title, text=text, is_at_all=is_at_all)
    logger.info("测试报告发送完成")


def send_report(envir) -> None:
    logger.info("用例运行完成，开始发送报告")
    case_rate = None
    # allure报告结果json路径
    file_name = REPORT_DATA_DIR
    with open(file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
    case_json = data['statistic']
    case_all = case_json['total']  # 测试用例总数
    case_fail = case_json['failed']  # 失败用例数量
    case_pass = case_json['passed']  # 成功用例数量
    case_skipped = case_json['skipped']  # 跳过用例数量
    case_broken = case_json['broken']  # 非预期结果用例数量
    time_json = data['time']
    duration_time = time_json['duration']  # 用例持续时间

    duration = format_current_datetime(date_style='duration', duration_ms=duration_time)

    if case_all >= 0:
        # 计算出来当前失败率
        case_rate = round((case_pass / case_all) * 100, 2)
    else:
        logger.debug('未获取到执行结果')

    if envir == 'pro':
        report_url = 'http://47.251.13.160:12306/'
    elif envir == 'dev':
        report_url = 'http://222.209.91.242:12306/'
    else:
        report_url = 'http://127.0.0.1:12306/'

    title = '自动化测试结果'

    text = f'### **自动化测试完成**\n\n' \
           f' 本次测试执行时间{duration}\n\n' \
           f' <font color="##FFFF00">用例通过率：{case_rate}% </font>\n\n' \
           f' <font color="#228B22">执行用例数：{case_all}个</font>  \n\n' \
           f' <font color="#008000">成功用例数：{case_pass}个</font>  \n\n' \
           f' <font color="#008000">跳过用例数：{case_skipped}个</font>  \n\n' \
           f' <font color="#dd0000">失败用例数：{case_fail}个</font>  \n\n' \
           f' <font color="#dd0000">非预期结果用例数：{case_broken}个</font>  \n\n' \
           f' 测试报告地址：{report_url} '

    dingding(envir=envir, title=title, text=text)


if __name__ == '__main__':
    dingding(envir='test', title='xxxx', text='yyyy')
