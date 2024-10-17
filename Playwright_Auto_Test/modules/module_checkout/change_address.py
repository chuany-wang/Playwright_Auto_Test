"""
-*- coding: utf-8 -*-
@Author: wangcy
@E-mail:
@Time:
@Explain:
"""

from modules.module_common import ModuleCommon, checkout_loc
from common.basic import basic_wait_for_element
from common.lo_logger import logger


class ModuleChanAddress(ModuleCommon):

    def __init__(self, driver, url, theme, host):
        super().__init__(driver, url, theme=theme, host=host)
        self.checkout_loc = checkout_loc(theme)

    def click_chanAddress(self):
        try:
            self.basic_click(**self.checkout_loc['ship_address'])
            logger.debug(f"{self.host}点击修改address ")
        except Exception as e:
            logger.error(f"{self.host}点击修改address出现异常:{e}")

    def clean_oldName(self):
        try:
            self.basic_js_clear(**self.checkout_loc['chan_name'])
            logger.debug(f"{self.host}清空原先的name")
        except Exception as e:
            logger.error(f"{self.host}清空原先的name出现异常:{e}")

    def input_newName(self):
        try:
            self.basic_input(**self.checkout_loc['chan_name'], text="Test New")
            logger.debug(f"{self.host}输入新的name ")
        except Exception as e:
            logger.error(f"{self.host}输入新的name 出现异常:{e}")

    def save_button(self):
        try:
            self.basic_scroll_to_ele(**self.checkout_loc['save_button_chan'])
            basic_wait_for_element(0.5)
            self.basic_click(**self.checkout_loc['save_button_chan'])
            logger.debug(f"{self.host}点击保存确定 ")
        except Exception as e:
            logger.error(f"{self.host}点击保存确定出现异常:{e}")

    def assert_chanAddress(self):
        try:
            res = self.basic_get_ele_text(**self.checkout_loc['assert_chanAddress'])
            logger.debug(f"{self.host}获取修改后的姓名 ")
            return res
        except Exception as e:
            logger.error(f"{self.host}获取修改后的姓名出现异常:{e}")
            return "fail"

    def case_change_address(self):
        basic_wait_for_element(2)
        self.click_chanAddress()
        basic_wait_for_element(1)
        self.clean_oldName()
        basic_wait_for_element(1)
        self.input_newName()
        basic_wait_for_element(1)
        self.save_button()
        basic_wait_for_element(1)
