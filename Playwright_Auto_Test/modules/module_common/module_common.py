# -*- coding: utf-8 -*-
import time

# @Author: wangcy
# @File:
# @Time :
# @Email:


from common.lo_logger import logger
from common.init_redis import re_db
from common.read_data import read_loc
from playwright.async_api import Page
from common.basic import Basic, format_current_datetime


class ModuleCommon(Basic):
    def __init__(self, page: Page, url: str, theme: str, host: str):
        super().__init__(page)
        self.page = page
        self.url = url
        self.host = host
        self.theme = theme
        self.common_loc = read_loc(theme, "common_loc.yaml")

    async def open_site(self):
        await self.page.goto(self.url)
        await self.reset_storage()
        await self.basic_set_cookie(self.host)
        await self.page.reload()

    async def reset_storage(self):
        current_timestamp = format_current_datetime('timestamp')
        script_cookie = f'window.localStorage.setItem("agree_use_cookie","{current_timestamp}")'
        await self.basic_script_running(script_cookie)
        script_sub = f'window.localStorage.setItem("user-show-sub-layer","{current_timestamp}")'
        await self.basic_script_running(script_sub)

    def assert_url(self):
        ass_url = self.page.url
        return ass_url

    async def username_input(self):
        await self.page.fill(**self.common_loc['inputEmail_login'])

    async def password_input(self):
        await self.page.fill(**self.common_loc['inputPassword_login'])

    async def submit_button(self):
        await self.page.click(**self.common_loc['loginButton_login'])

    async def common_login_step(self):
        await self.open_site()
        await self.username_input()
        await self.password_input()
        await self.submit_button()

    async def allure_report(self, module, title):
        await self.basic_attach_allure_report(module=module, title=title)

    """---------------------------------------**** 首页搜索 ****---------------------------------------------"""

    async def home_search(self):
        try:
            if self.theme != 'kte-m':
                await self.page.click(**self.common_loc['search_home'])
            await self.page.click(**self.common_loc['search_home'])
            logger.debug(f"{self.host} 点击首页搜索按钮")
        except Exception as e:
            logger.error(f"{self.host} 点击首页搜索按钮出现异常:{e}")

    async def input_search(self, host):
        try:
            await self.page.fill(**self.common_loc['search_input'], value=re_db.get_list(host).get('sku'))
            logger.debug(f"{self.host} 输入商品SKU,进行搜索")
        except Exception as e:
            logger.error(f"{self.host} 输入商品SKU,进行搜索出现异常:{e}")

    async def click_search_button(self):
        try:
            await self.page.click(**self.common_loc['search_icon'])
            logger.debug(f"{self.host} 点击搜索按钮")
        except Exception as e:
            logger.error(f"{self.host} 点击搜索按钮,进行搜索出现异常:{e}")

    async def green_click_search_button(self):
        try:
            await self.page.click(**self.common_loc['green_search_button'])
            logger.debug(f"{self.host} 点击搜索按钮")
        except Exception as e:
            logger.error(f"{self.host} 点击搜索按钮,进行搜索出现异常:{e}")

    async def search_pro(self, host):
        """
        m5 主题与手机端方法共享
        """
        await self.open_site()
        await self.home_search()
        await self.input_search(host=host)
        await self.click_search_button()

    async def green_search_pro(self, host):
        await self.open_site()
        await self.input_search(host=host)
        await self.green_click_search_button()

    """---------------------------------------**** 选择商品进行购买 ****------------------------------------------------"""

    async def click_pro_info(self):
        try:
            await self.page.click(**self.common_loc['pro_info'])
            logger.debug(f"{self.host} 点击商品标题,进入商品详情页")
        except Exception as e:
            logger.error(f"{self.host} 点击商品标题,进入商品详情页,出现异常:{e}")

    async def click_buy_now(self):
        try:
            await self.page.click(**self.common_loc['buy_now'])
            logger.debug(f"{self.host} 点击BuyNow按钮")
        except Exception as e:
            logger.error(f"{self.host} 点击BuyNow按钮出现异常:{e}")

    """-------------------------------------**** 选择商品加入购物车****--------------------------------------------------"""

    async def add_cart(self):
        try:
            await self.page.click(**self.common_loc['add_cart'])
            logger.debug(f"{self.host} 添加商品到购物车")
        except Exception as e:
            logger.error(f"{self.host} 添加商品到购物车结账出现异常:{e}")

    async def view_cart(self):
        """
        only for kte PC
        :return:
        """
        try:
            await self.page.wait_for_selector(**self.common_loc['wait_slide_cart'])
            await self.page.click(**self.common_loc['view_cart'])
            logger.debug(f"{self.host} PC端商品详情页进入到购物车")
        except Exception as e:
            logger.error(f"{self.host} PC端商品详情页进入到购物车出现异常:{e}")

    async def checkout_cart(self):
        try:
            await self.page.click(**self.common_loc['checkout_cart'])
            logger.debug(f"{self.host} 购物车内点击checkout")
        except Exception as e:
            logger.error(f"{self.host} 购物车内点击checkout出现异常:{e}")

    """----------------------------------------**** 编辑客户信息****---------------------------------------------------"""

    async def input_email(self):
        try:
            await self.page.fill(**self.common_loc['inputEmail'])
            logger.debug(f"{self.host} 输入邮箱")
        except Exception as e:
            logger.error(f"{self.host}: 输入邮箱出现异常{e}")

    async def select_country(self):
        try:
            if self.theme == 'kte':
                await self.basic_click(**self.common_loc['openCountry'])
                await self.basic_click(**self.common_loc['selectCountry'])
            else:
                await self.basic_select(**self.common_loc['selectCountry'])
            logger.debug(f"{self.host}: 选择客户国家")
        except Exception as e:
            logger.error(f"{self.host}: 选择客户国家出现异常: {e}")

    async def input_firstname(self):
        try:
            await self.page.fill(**self.common_loc['inputFirstName'])
            logger.debug(f"{self.host}: 输入客户名")
        except Exception as e:
            logger.error(f"{self.host}: 输入客户名出现异常{e}")

    async def input_lastname(self):
        try:
            await self.page.fill(**self.common_loc['inputLastName'])
            logger.debug(f"{self.host}: 输入客户姓")
        except Exception as e:
            logger.error(f"{self.host}: 输入客户姓出现异常{e}")

    async def input_address(self):

        try:
            await self.page.fill(**self.common_loc['inputAddress'])
            logger.debug(f"{self.host}: 输入客户地址")
        except Exception as e:
            logger.error(f"{self.host}: 输入客户地址 出现异常{e}")

    async def input_shipping_city(self):
        try:
            await self.page.fill(**self.common_loc['inputShipCity'])
            logger.debug(f"{self.host}: 输入客户付款城市")
        except Exception as e:
            logger.error(f"{self.host}: 输入客户付款城市 出现异常{e}")

    async def input_zipcode(self):
        try:
            await self.page.fill(**self.common_loc['inputZipCode'])
            logger.debug(f"{self.host}输入客户邮编")
        except Exception as e:
            logger.error(f"{self.host}输入客户邮编 出现异常{e}")

    async def select_states(self):
        try:
            if self.theme == 'kte':
                await self.basic_click(**self.common_loc['openState'])
                await self.basic_click(**self.common_loc['selectState'])
            else:
                await self.basic_select(**self.common_loc['selectState'])
            logger.debug(f"{self.host}: 选择客户States")
        except Exception as e:
            logger.error(f"{self.host}: 选择客户States出现异常: {e}")

    async def input_phone(self):
        try:
            await self.page.fill(**self.common_loc['inputPhone'])
            logger.debug(f"{self.host}: 输入客户手机号")
        except Exception as e:
            logger.error(f"{self.host}: 输入客户手机号{e}")

    async def click_save_button(self):
        try:
            await self.page.click(**self.common_loc['saveButton'])
            logger.debug(f"{self.host}: 点击save&Continue 按钮")
        except Exception as e:
            logger.error(f"{self.host}: 点击save&Continue 按钮{e}")

    async def continue_button_pc(self):
        try:
            await self.page.click(**self.common_loc['continuePayButton'])
            logger.debug(f"{self.host}点击'continuePayButton' 按钮 ")
        except Exception as e:
            logger.error(f"{self.host}:点击'continuePayButton'按钮出现异常:{e}")

    async def input_cust_info(self):
        await self.input_email()
        await self.select_country()
        await self.input_firstname()
        await self.input_lastname()
        await self.input_address()
        await self.input_shipping_city()
        await self.input_zipcode()
        await self.basic_load(1)
        await self.select_states()
        await self.input_phone()
        await self.click_save_button()

    """-------------------------------------------- **** 购物通用流程 ****  -----------------------------------------"""

    async def common_buy_step(self):

        # 1. go to pro page
        await self.open_site()

        # 2. click buy now
        await self.click_buy_now()

        # 3. input customer info
        await self.input_cust_info()

        if self.theme in ["green", "mahardhi05custom"]:
            await self.continue_button_pc()
