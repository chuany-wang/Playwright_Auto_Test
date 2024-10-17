# -*- coding: utf-8 -*-
# @Author: wangcy
# @File:
# @Time :
# @Email:

import pytest
from common.lo_logger import logger
from common.init_redis import re_db
from common.basic import get_system
from playwright.async_api import async_playwright

def get_params(key):
    result = re_db.get_list(key=key)
    return result


@pytest.fixture(scope="function")
async def create_page():
    async with async_playwright() as p:
        logger.info("page session fixture starting....")
        system = get_system()
        if system == 'win32':
            browser = await p.chromium.launch(headless=False, args=['--start-maximized'], timeout=5_000)
        else:
            browser = await p.chromium.launch(headless=True, args=['--start-maximized'], timeout=5_000)
        context = await browser.new_context(no_viewport=True)
        page_pc = await context.new_page()
        yield page_pc
        logger.info("page session fixture closing.......")
        await browser.close()


@pytest.fixture(scope="function")
async def page_phone():
    async with async_playwright() as ph:
        logger.info("page session fixture starting....")
        iphone_14 = ph.devices['iPhone 14 Pro Max']
        system = get_system()
        if system == 'win32':
            browser = await ph.chromium.launch(headless=False, args=['--start-maximized'], timeout=5_000)
        else:
            browser = await ph.chromium.launch(headless=True, args=['--start-maximized'], timeout=5_000)
        context = await browser.new_context(**iphone_14)
        page_ph = await context.new_page()
        yield page_ph
        logger.info("page session fixture closing.......")
        await browser.close()


def process_url(site_host, test_type):
    """
    :param site_host: 站点域名
    :param test_type: 1001 商品详情页， 1002 登录页面, 1003 注册页面
    :return:
    """
    if test_type == 1001:
        # pay or cart, go to pro page
        keyword = re_db.get_list(site_host).get('keyword')
        url = site_host + 'product/' + keyword

    elif test_type == 1002:
        # like module_account, got to common_login_step page
        url = site_host + 'index.php?route=account/login'

    elif test_type == 1003:
        # like module_account, got to common_login_step page
        url = site_host + 'index.php?route=account/register'

    else:
        # others, go to home page
        url = site_host

    return url


@pytest.fixture(scope='module', params=get_params('common'))
def common_params(request):
    yield request.param


@pytest.fixture(scope='module', params=get_params('payment_oceanpayment_status'))
def op_params(request):
    yield request.param


@pytest.fixture(scope='module', params=get_params('payment_op_klarna_status'))
def opk_params(request):
    yield request.param


@pytest.fixture(scope='module', params=get_params('payment_pacypayment_cashier_status'))
def pacyPayCa_params(request):
    yield request.param


@pytest.fixture(scope='module', params=get_params('payment_pacypayment_status'))
def pacypaycr_params(request):
    yield request.param


@pytest.fixture(scope='module', params=get_params('payment_pacypayment_klarna_status'))
def pacyPayKl_params(request):
    yield request.param


@pytest.fixture(scope='module', params=get_params('payment_payoneer_status'))
def payoneer_params(request):
    yield request.param


@pytest.fixture(scope='module', params=get_params('payment_paypal_status'))
def paypal_params(request):
    yield request.param


def check_fixture_value(key):
    res = get_params(key)
    return False if res else True
