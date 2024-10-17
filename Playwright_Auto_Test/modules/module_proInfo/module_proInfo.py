"""
-*- coding: utf-8 -*-
@Author: wangcy
@E-mail:
@Time:
@Explain:
"""

from common.lo_logger import logger
from common.read_data import read_loc
from modules.module_common.module_common import ModuleCommon


class ModuleProInfo(ModuleCommon):

    def __init__(self, page, url, theme, host):
        super().__init__(page, url, theme=theme, host=host)
        self.proInfo_loc = read_loc(theme, "proInfo_loc.yaml")

    """----------------------------------------**** Write Review **** -----------------------------------------------"""

    async def click_write_review(self):
        try:
            await self.page.click(**self.proInfo_loc['write_review_button'])
            logger.debug(f"{self.host}点击 write view 按钮")
        except Exception as e:
            logger.error(f"{self.host}点击 write view 按钮出现异常:{e}")

    async def input_name_review(self):
        try:
            await self.page.fill(**self.proInfo_loc['review_input_name'])
            logger.debug(f"{self.host}输入姓名")
        except Exception as e:
            logger.error(f"{self.host}输入姓名出现异常:{e}")

    async def click_score_review(self):
        try:
            await self.page.click(**self.proInfo_loc['review_data_score'])
            logger.debug(f"{self.host}点击 score")
        except Exception as e:
            logger.error(f"{self.host}输入姓名出现异常:{e}")

    async def input_title_review(self):
        try:
            await self.page.fill(**self.proInfo_loc['review_input_title'])
            logger.debug(f"{self.host}输入title")
        except Exception as e:
            logger.error(f"{self.host}输入姓名出现异常:{e}")

    async def input_text_review(self):
        try:
            await self.page.fill(**self.proInfo_loc['review_input_text'])
            logger.debug(f"{self.host}输入文本")
        except Exception as e:
            logger.error(f"{self.host}输入文本:{e}")

    async def click_submit_review(self):
        try:
            await self.basic_click(**self.proInfo_loc['review_submit_button'])
            logger.debug(f"{self.host}点击submit")
        except Exception as e:
            logger.error(f"{self.host}点击submit出现异常:{e}")

    async def assert_review(self):
        try:
            assert_write_review = await self.basic_attribute(**self.proInfo_loc['review_submit_button'], name='id')
            logger.debug(f"{self.host}write review断言获取元素{assert_write_review}")
            return assert_write_review
        except Exception as e:
            logger.error(f"{self.host}点击submit出现异常:{e}")
            return "fail"

    async def case_write_review(self):
        await self.click_write_review()

    """-------------------------------------------**** 收藏商品 **** --------------------------------------------------"""

    async def add_wish_list(self):
        try:
            await self.basic_click(**self.proInfo_loc['add_wish'])
            logger.debug(f"{self.host}商品详情页点击心愿单")
        except Exception as e:
            logger.error(f"{self.host}商品详情页点击心愿单出现异常{e}")

    async def assert_add_wish(self):

        try:
            res = await self.basic_attribute(**self.proInfo_loc['add_wish'], name="class")
            logger.debug(f"{self.host}商品详情页收藏商品")
            return res
        except Exception as e:
            logger.error(f"{self.host}商品详情页收藏商品断言出现异常{e}")
            return "fail"

    """---------------------------------------**** 详情页修改商品数量 **** ----------------------------------------------"""

    async def plus_pro_num(self):
        try:
            await self.basic_click(**self.proInfo_loc['plus_pro_num_info'])
            logger.debug(f"{self.host}添加商品数量")
        except Exception as e:
            logger.error(f"{self.host}添加商品数量:{e}")

    """---------------------------------------**** ask question **** ------------------------------------------------"""

    async def ask_question(self):
        try:
            await self.page.click(**self.proInfo_loc['ask_question_pro_info'])
            logger.debug(f"{self.host}详情页点击 ask question")
        except Exception as e:
            logger.error(f"{self.host}详情页点击 ask question:{e}")

    async def input_name_ask_ques(self):
        try:
            await self.page.fill(**self.proInfo_loc['input_name_ask_que'])
            logger.debug(f"{self.host}ask question输入name")
        except Exception as e:
            logger.error(f"{self.host}ask question输入name出现异常:{e}")

    async def input_email_ask_ques(self):
        try:
            await self.page.fill(**self.proInfo_loc['input_email_ask_que'])
            logger.debug(f"{self.host}ask question输入email")
        except Exception as e:
            logger.error(f"{self.host}ask question输入email出现异常:{e}")

    async def input_text_ask_ques(self):
        try:
            await self.page.fill(**self.proInfo_loc['input_ques_ask_que'])
            logger.debug(f" ask question 输入text")
        except Exception as e:
            logger.error(f"{self.host}ask question输入text出现异常:{e}")

    async def submit_ask_ques(self):
        try:
            await self.page.click(**self.proInfo_loc['submit_ask_que'])
            logger.debug(f"ask question 点击submit")
        except Exception as e:
            logger.error(f"{self.host}ask question点击submit出现异常:{e}")

    async def assert_ask_ques(self):

        try:
            res = await self.basic_attribute(**self.proInfo_loc['assert_ask_que'])
            logger.debug(f"{self.host}ask question断言")
            return res
        except Exception as e:
            logger.error(f"{self.host}ask question断言出现异常:{e}")
            return "fail"

    async def case_ask_question(self):
        await self.ask_question()
        await self.input_name_ask_ques()
        await self.input_email_ask_ques()
        await self.input_text_ask_ques()
        await self.submit_ask_ques()

    """-------------------------------------------**** 分享商品 **** --------------------------------------------------"""

    async def sharePro(self):
        try:
            await self.page.click(**self.proInfo_loc['share_button'])
            logger.debug(f"{self.host}分享商品点击分享按钮")
        except Exception as e:
            logger.error(f"{self.host}点击分享按钮出现异常{e}")

    async def click_facebook(self):
        try:
            async with self.page.expect_popup() as popup_info:
                await self.page.click(**self.proInfo_loc['facebook'])
                logger.debug(f"{self.host}商品分享到facebook")
            new_page = await popup_info.value
            return new_page
        except Exception as e:
            logger.error(f"{self.host}商品分享到facebook出现异常{e}")

    async def assert_share_pro(self, new_page):
        try:
            res = new_page.url
            return res
        except Exception as e:
            logger.error(f"{self.host} 分享商品获取新窗口URL出现异常:{e}")

    async def case_share(self):
        await self.sharePro()
        new_page = await self.click_facebook()
        return new_page
