"""
-*- coding: utf-8 -*-
@Author: wangcy
@E-mail:
@Time:
@Explain:
"""

import allure
import pytest
from common.lo_logger import logger
from cases.conftest import process_url
from modules.module_account.module_account import Account


@allure.feature('个人中心用例')
class TestAboutUs:

    @pytest.mark.asyncio
    @pytest.mark.AboutUsPh
    @allure.story('AboutUs手机端测试用例')
    async def test_about_us_ph(self, page_phone, common_params):

        host = common_params.get('site_host')
        mobile_theme = common_params.get('mobile_theme')
        url = process_url(site_host=host, test_type=1002)

        if mobile_theme == 'kte-m':

            obj = Account(page=page_phone, url=url, theme=mobile_theme, host=host)
            logger.info(f"正在测试站点 {host} 的手机端AboutUs功能")

            # 1. go to common_login_step
            await obj.common_login_step()

            # 2. click AboutUs
            await obj.click_about_us()

            # 3. assert
            assert_res = await obj.assert_about_us()
            if 'register' not in assert_res:
                await obj.allure_report(module="AboutUs_手机端", title=f"{host}的AboutUs测试")
            pytest.assume('register' in assert_res)

        elif not mobile_theme:
            logger.info(f"站点{host} 未开启手机端，不执行测试")

    @pytest.mark.asyncio
    @pytest.mark.AboutUsPc
    @allure.story('AboutUsPC端测试用例')
    async def test_about_us_pc(self, create_page, common_params):

        pc_theme = common_params.get('pc_theme')
        host = common_params.get('site_host')
        url = process_url(site_host=host, test_type=1002)

        if pc_theme == 'kte':

            obj = Account(page=create_page, url=url, theme=pc_theme, host=host)
            logger.info(f"正在测试站点 {host} 的PC端AboutUs功能")

            # 1. go to common_login_step
            await obj.common_login_step()

            # 2. click AboutUs
            await obj.click_about_us()

            # 3. assert
            assert_res = await obj.assert_about_us()
            if 'register' not in assert_res:
                await obj.allure_report(module="AboutUs_PC端", title=f"{host}的AboutUs测试")

            pytest.assume('register' in assert_res)

        else:
            logger.info(f"站点{host} PC端主题不是 Kte，不执行测试")
