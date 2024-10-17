import string
import random

import allure
from common.lo_logger import logger
from playwright.async_api import Page
from modules.module_common.module_common import ModuleCommon
from common.read_data import read_loc


def gen_name():
    letters = string.ascii_letters
    random_string = ''.join(random.choice(letters) for _ in range(4))
    return random_string


def gen_phone():
    # 生成随机的前三位
    first_three_digits = str(random.randint(100, 999))
    # 生成随机的后八位
    last_eight_digits = ''.join(random.choice('0123456789') for _ in range(8))
    # 拼接手机号码
    phone_number = f"1{first_three_digits}{last_eight_digits}"

    return phone_number


class Account(ModuleCommon):

    def __init__(self, page: Page, url, theme, host):
        super().__init__(page, url, theme=theme, host=host)
        self.account_loc = read_loc(theme, "account_loc.yaml")

    async def click_account(self):
        try:
            await self.page.click(**self.account_loc['my_account'])
            logger.debug(f"{self.host}首页点击个人中心")
        except Exception as e:
            logger.error(f"{self.host}首页点击个人中心出现异常{e}")

    """-----------------------------------------**** 注册功能 ****-----------------------------------------------------"""

    async def click_register_title(self):
        try:
            await self.page.click(**self.account_loc['register'])
            logger.debug(f"{self.host} 个人中心点击 register ")
        except Exception as e:
            logger.error(f"{self.host}: 个人中心点击 register出现异常{e}")

    async def input_firstname_reg(self):
        try:
            await self.page.fill(**self.account_loc['firstname_reg'])
            logger.debug(f"{self.host}注册时输入firstname")
        except Exception as e:
            logger.error(f"{self.host}: 输入firstname 出现异常{e}")

    async def input_lastname_reg(self):
        try:
            await self.page.fill(**self.account_loc['lastname_reg'])
            logger.debug(f"{self.host}注册时输入lastname")
        except Exception as e:
            logger.error(f"{self.host}: 输入lastname 出现异常{e}")

    async def input_email_reg(self):
        try:
            await self.page.fill(**self.account_loc['email_reg'])
            logger.debug(f"{self.host}注册时输入邮箱")
        except Exception as e:
            logger.error(f"{self.host}: 输入邮箱 出现异常{e}")

    async def input_telephone_reg(self):
        try:
            await self.page.fill(**self.account_loc['telephone_reg'])
            logger.debug(f"{self.host}注册时输入电话号码")
        except Exception as e:
            logger.error(f"{self.host}: 注册时输入电话号码出现异常{e}")

    async def input_password_reg(self):
        try:
            await self.page.fill(**self.account_loc['password_reg'])
            logger.debug(f"{self.host}注册时输入密码")
        except Exception as e:
            logger.error(f"{self.host}: 注册时输入密码出现异常{e}")

    async def input_confirm_reg(self):
        try:
            await self.page.fill(**self.account_loc['confirm_reg'])
            logger.debug(f"{self.host}注册时输入确认密码")
        except Exception as e:
            logger.error(f"{self.host}: 注册时输入确认密码出现异常{e}")

    async def click_register_reg(self):
        try:
            await self.page.click(**self.account_loc['button_reg'])
            logger.debug(f"{self.host}点击注册按钮")
        except Exception as e:
            logger.error(f"{self.host}: 点击注册按钮出现异常{e}")

    async def assert_reg(self):
        try:
            res = await self.basic_attribute(**self.account_loc['assert_reg'])
            logger.debug(f"{self.host}注册断言元素标签{res}")
            return res
        except Exception as e:
            logger.error(f"{self.host}: 注册断言出现异常{e}")
            return "fail"

    async def account_register(self):
        if self.theme == 'kte':
            await self.input_firstname_reg()
            await self.input_lastname_reg()
            await self.input_email_reg()
            await self.input_password_reg()
        else:
            await self.click_register_title()
            await self.input_firstname_reg()
            await self.input_lastname_reg()
            await self.input_email_reg()
            await self.input_telephone_reg()
            await self.input_password_reg()
            await self.input_confirm_reg()
        await self.click_register_reg()

    """-----------------------------------------**** 谷歌登录功能****-----------------------------------------------------"""

    async def gmail_login(self):
        try:
            await self.basic_click(**self.account_loc['google_login'])
            logger.debug(f"{self.host}使用谷歌邮箱快捷登录")
        except Exception as e:
            logger.error(f"{self.host}: 使用谷歌邮箱快捷登录异常{e}")

    async def google_login_case(self):
        await self.gmail_login()

    """-----------------------------------------**** 登出功能****-----------------------------------------------------"""

    async def log_out(self):
        try:
            await self.basic_click(**self.account_loc['logoutButton'])
            logger.debug(f"{self.host}点击logout 按钮")
        except Exception as e:
            logger.error(f"{self.host}: 点击logout 按钮按钮出现异常{e}")

    async def sure_logout(self):
        try:
            await self.basic_click(**self.account_loc['sure_logout'])
            logger.debug(f"{self.host} logout点击sure按钮")
        except Exception as e:
            logger.error(f"{self.host}: logout点击sure按钮出现异常{e}")

    async def case_logout(self):
        await self.log_out()
        await self.sure_logout()

    """-----------------------------------------**** EDIT PASSWORD****-----------------------------------------------"""

    async def click_edit_password(self):
        try:
            await self.page.click(**self.account_loc['edit_password'])
            logger.debug(f"{self.host}点击修改密码按钮")
        except Exception as E:
            logger.error(f"{self.host}: 点击修改密码按钮出现异常{E}")

    async def input_current_pw(self):
        try:
            await self.page.fill(**self.account_loc['current_password'])
            logger.debug(f"{self.host}输入新密码")
        except Exception as e:
            logger.error(f"{self.host}: 输入新密码出现异常{e}")

    async def input_new_pw(self):
        try:
            await self.page.fill(**self.account_loc['input_new_password'])
            logger.debug(f"{self.host}输入新密码")
        except Exception as e:
            logger.error(f"{self.host}: 输入新密码出现异常{e}")

    async def input_new_pw_sec(self):
        try:
            await self.page.fill(**self.account_loc['confirm_new_password'])
            logger.debug(f"{self.host}:二次输入新密码")
        except Exception as e:
            logger.error(f"{self.host}:二次输入新密码出现异常{e}")

    async def submit_pw_confirm(self):
        try:
            await self.page.click(**self.account_loc['submit_changePas'])
            logger.debug(f"{self.host}确认密码")
        except Exception as e:
            logger.error(f"{self.host}: 确认密码出现异常{e}")

    async def confirm_success(self):
        try:
            if self.theme == 'kte':
                await self.page.wait_for_selector(**self.account_loc['continue_changePas'], timeout=3_000)
            else:
                await self.page.click(**self.account_loc['continue_changePas'])
            logger.debug(f"{self.host}修改密码完成后点击确认")
        except Exception as e:
            logger.error(f"{self.host}: 修改密码完成后点击确认异常{e}")

    async def case_edit_pw(self):
        await self.click_edit_password()
        if self.theme == 'kte':
            await self.input_current_pw()
        await self.input_new_pw()
        await self.input_new_pw_sec()
        await self.submit_pw_confirm()
        await self.confirm_success()

    """-----------------------------------------**** 我的订阅 ****-----------------------------------------------"""

    async def click_my_subscribe(self):
        try:
            await self.page.click(**self.account_loc['my_subscriber'])
            logger.debug(f"{self.host}点击我的订阅")
        except Exception as E:
            logger.error(f"{self.host}: 点击我的订阅出现异常{E}")

    async def submit_subscribe(self):
        try:
            await self.page.click(**self.account_loc['submit_subscribe'])
            logger.debug(f"{self.host}点击我的订阅的确认按钮")
        except Exception as E:
            logger.error(f"{self.host}: 点击我的订阅的确认按钮{E}")

    async def assert_subscribe(self):
        try:
            if self.theme == 'kte':
                res = await self.basic_attribute(**self.account_loc['assert_Reviews'])
                if 'success' in res:
                    return True
            else:
                res = self.assert_url()
                if 'newsletter' in res:
                    return True
            return False
        except Exception as E:
            logger.error(f"{self.host}: 点击我的订阅的确认按钮{E}")

    async def subscribe_case(self):
        await self.click_my_subscribe()
        await self.submit_subscribe()

    """-----------------------------------------**** contact US ****-----------------------------------------------"""

    async def click_contact_us(self):
        try:
            await self.page.locator(**self.account_loc['contact_us']).scroll_into_view_if_needed()
            await self.page.click(**self.account_loc['contact_us'])
            logger.debug(f"{self.host}点击contact_us")
        except Exception as E:
            logger.error(f"{self.host}: 点击contact_us出现异常{E}")

    async def assert_contact_us(self):
        """
        使用页面元素内有无联系我们表单断言, 404页面不会出现该标签
        """
        try:
            assert_res = await self.page.locator(**self.account_loc['assert_contact_us']).get_attribute('action')
            logger.debug(f'断言元素为{assert_res}')
            return assert_res
        except Exception as E:
            logger.error(f"{self.host}: contact_us断言出现异常{E}")

    """-----------------------------------------**** about US ****-----------------------------------------------"""

    async def click_about_us(self):
        try:
            await self.page.click(**self.account_loc['about_us'])
            logger.debug(f"{self.host}点击about_us")
        except Exception as E:
            logger.error(f"{self.host}: 点击about_us出现异常{E}")

    async def assert_about_us(self):
        """
        使用页面元素内有无注册元素断言, 404页面不会出现该标签
        """
        try:
            assert_res = await self.page.locator(**self.account_loc['assert_about_us']).get_attribute('href')
            logger.debug(f'断言元素为{assert_res}')
            return assert_res
        except Exception as E:
            logger.error(f"{self.host}: about_us断言出现异常{E}")

    """----------------------------------------**** Recently Viewed ****--------------------------------------------"""

    async def click_recently_viewed(self):
        try:
            await self.page.click(**self.account_loc['recently_Viewed'])
            logger.debug(f"{self.host} 点击最近浏览")
        except Exception as e:
            logger.error(f"{self.host}: 点击最近浏览出现异常{e}")

    async def case_recently_view(self):
        await self.click_recently_viewed()

    """-----------------------------------------**** Forget Password ****--------------------------------------------"""

    async def forget_password(self):
        try:
            await self.page.click(**self.account_loc['forget_button'])
            logger.debug(f"{self.host}点击forget password")
        except Exception as E:
            logger.error(f"{self.host}: 点击forget password出现异常{E}")

    async def input_email_forget(self):
        try:
            await self.page.fill(**self.account_loc['input_email_forget'])
            logger.debug(f"{self.host}输入邮箱")
        except Exception as E:
            logger.error(f"{self.host}: 输入邮箱出现异常{E}")

    async def save_button_forget(self):
        try:
            await self.page.click(**self.account_loc['submit_forget'])
            logger.debug(f"{self.host}点击确定")
        except Exception as E:
            logger.error(f"{self.host}: 点击确定出现异常{E}")

    async def assert_forget_password(self):
        try:
            res = await self.basic_attribute(**self.account_loc['asset_forget_Pass'])
            logger.debug(f"{self.host}获取忘记密码断言")
            return res
        except Exception as E:
            logger.error(f"{self.host}: 获取忘记密码断言异常{E}")
            return "fail"

    async def case_forget_password(self):
        await self.forget_password()
        await self.input_email_forget()
        await self.save_button_forget()

    """-----------------------------------------**** My Return ****--------------------------------------------"""

    async def click_MyReturn(self):
        try:
            await self.page.click(**self.account_loc['My_return'])
            logger.debug(f"{self.host}点击My return")
        except Exception as E:
            logger.error(f"{self.host}: 点击My return出现异常{E}")

    async def case_return(self):
        await self.click_MyReturn()

    """-----------------------------------------**** Reviews ****--------------------------------------------"""

    async def click_reviews(self):
        try:
            await self.page.click(**self.account_loc['Reviews'])
            logger.debug(f"{self.host} 点击Reviews")
        except Exception as E:
            logger.error(f"{self.host}: 点击Reviews出现异常{E}")

    async def case_reviews(self):
        await self.click_reviews()
