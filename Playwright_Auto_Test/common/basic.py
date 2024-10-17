import os
import shutil
import sys
import time
import allure
from urllib.parse import urlparse
from common.lo_logger import logger
from playwright.async_api import Page
from common.read_data import read_conf
from datetime import datetime, timedelta
from config import SCREENSHOT_DIR, ALLURE_DIR, JSON_DIR


def get_system():
    result = sys.platform.lower()
    return result


def get_domain_and_path(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    path = parsed_url.path
    if "www" in domain:
        m_domain = domain.replace("www", "m")
    else:
        m_domain = "m" + domain

    return domain, m_domain, path


def format_current_datetime(date_style, duration_ms=None):
    current_datetime = datetime.now()

    if date_style == 'time':
        return current_datetime.strftime('%Y_%m_%d')

    elif date_style == 'date':
        return current_datetime.strftime('%Y%m%d')

    elif date_style == 'timestamp':
        return str(int(time.time() * 1000))

    elif date_style == 'duration' and duration_ms:
        # 转换为 timedelta 对象
        duration_td = timedelta(milliseconds=duration_ms)

        # 计算小时、分钟和秒
        hours = duration_td.seconds // 3600
        minutes = (duration_td.seconds % 3600) // 60
        seconds = duration_td.seconds % 60

        # 格式化输出
        formatted_duration = f"{hours}:{minutes:02d}:{seconds:02d}"

        return formatted_duration

    return None


class Basic:
    def __init__(self, page: Page):
        self.page = page

    async def basic_screen_shot(self, name) -> str or None:
        currentTime = format_current_datetime(date_style="timestamp")
        filename = name + "_" + currentTime + ".png"
        filepath = os.path.join(SCREENSHOT_DIR, filename)
        await self.page.screenshot(path=filepath)
        logger.debug(f"截图成功已经存储在: {filepath}")
        return filepath

    async def basic_attach_allure_report(self, module, title):
        filepath = await self.basic_screen_shot(module)
        with open(filepath, mode='rb') as f:
            file = f.read()
        allure.attach(file, f'{title}', allure.attachment_type.PNG)

    async def basic_wait_click(self, selector):
        ele = await self.page.wait_for_selector(selector=selector)
        await ele.click()

    async def basic_script_click(self, selector):
        ele = self.page.locator(selector=selector)
        await ele.evaluate('node => node.click();')

    async def basic_wait_fill(self, selector):
        await self.page.wait_for_selector(selector=selector).fill()

    async def basic_select(self, selector, index):
        await self.page.select_option(selector=selector, index=index)

    async def basic_frame_wait(self, frame, selector):
        ele = frame.locator(selector)
        await ele.wait_for(state='visible')

    async def basic_frame_select(self, frame, selector, index):
        await frame.locator(selector).select_option(index=index)

    async def basic_frame_click(self, frame, selector):
        await frame.locator(selector).click()

    async def basic_frame_fill(self, frame, selector, value):
        await frame.locator(selector).fill(str(value))

    async def basic_attribute(self, selector, name):
        res = await self.page.locator(selector).get_attribute(name=name)
        return res

    async def basic_frame_attribute(self, frame, selector, name):
        ele = frame.locator(selector)
        await ele.wait_for(state='visible')
        res = await ele.get_attribute(name=name)
        return res

    async def basic_click(self, selector, child=None):
        if child:
            await self.page.locator(selector).nth(int(child)).click()
        else:
            await self.page.locator(selector).click()

    async def basic_script_running(self, script):
        await self.page.evaluate(script)

    async def basic_load(self, second: int):
        await self.page.wait_for_timeout(second * 1000)

    async def basic_drag_drop(self, selector, target):
        await self.page.locator(selector).drag_to(target)

    async def basic_set_cookie(self, host):
        domain, m_domain, path = get_domain_and_path(host)
        cookies = [
            {"name": "gcm_access_storage_key", "value": "ad_storage_policy:true", "domain": f"{domain}",
             "path": f"{path}"},
            {"name": "switch_language_popup", "value": "1", "domain": f"{domain}", "path": f"{path}"},
            {"name": "gcm_access_storage_key", "value": "ad_storage_policy:true", "domain": f"{m_domain}",
             "path": f"{path}"},
            {"name": "switch_language_popup", "value": "1", "domain": f"{m_domain}", "path": f"{path}"}
        ]
        await self.page.context.add_cookies(cookies)


class RemoveReport:
    """
    删除已存在的报告
    """

    def mkdir(self, path: str) -> None:
        """
        当存储报告的文件夹不存在的时候，创建文件夹
        :param path:
        :return:
        """
        report_folder = os.path.exists(path)
        if not report_folder:
            os.mkdir(path)
        else:
            pass

    def clean_report(self, filepath: str) -> None:
        """
        :param filepath:历史报告所存储的路径
        :return:
        """
        rem_report_list = os.listdir(filepath)
        if rem_report_list:
            for f in rem_report_list:
                report_path = os.path.join(filepath, f)
                if f == '.gitignore':
                    pass
                elif os.path.isfile(report_path):
                    if not report_path.endswith(".xml"):
                        os.remove(report_path)
                else:
                    os.path.isdir(report_path)
                    shutil.rmtree(report_path)

    def run_rem_report(self) -> None:
        """
        执行删除历史测试报告
        :return:
        """
        is_clean_report = read_conf('CURRENCY').get('IS_CLEAN_REPORT')
        if is_clean_report:
            dir_list = [ALLURE_DIR, JSON_DIR]
            for _dir in dir_list:
                self.mkdir(_dir)
                self.clean_report(_dir)
