import re
from time import sleep

import allure
from common.page_url import *
from common.config import *
from common.util import get_nowtime

@allure.feature('基础g工单')
@allure.testcase(manage_index_url, '测试用例链接-客服端')
@allure.testcase(visitor_url, '测试用例链接-访客端')
@allure.testcase(visitor_url, '测试用例工单链接-jira地址')
class TestTicket:
    # 接起时间
    email_time = None

    @allure.title("添加工单-客服手工录入")
    def test_001(self, page):
        """
        检查点：
        * 1. 访客端消息发送成功校验访客端出现'会话创建成功'
          2. 校验访客端出现'会话已被客服接起'
          3. 校验客服端新增消息与访客发送时间戳一致
        """
        page.goto(customer_ticket_url)
        page.pause()
        self.__class__.pageVisitorTime = get_nowtime()
        print(self.pageVisitorTime)
        page.get_by_text("新建工单").click()
        page.locator("div").filter(has_text=re.compile(r"^请选择$")).click()
        page.get_by_text("反馈").click()
        page.locator("div:nth-child(46) > div > div:nth-child(3) > span").first.click()
        page.get_by_placeholder("标题").click()
        page.get_by_placeholder("标题").fill(self.pageVisitorTime)
        page.locator("#status").get_by_text("未处理").click()
        page.get_by_role("listitem", name="未处理").click()
        page.locator("#priorityId span").first.click()
        page.get_by_role("listitem", name="低").click()
        page.locator("div:nth-child(4) > .ui-cmp-select > .ui-cmp-selectbar > label").click()
        page.get_by_role("listitem", name="未选择").click()
        page.locator("div:nth-child(5) > .ui-cmp-select > .ui-cmp-selectbar > label").click()
        page.get_by_role("listitem", name="未选择").click()
        page.locator(".jodit-wysiwyg").click()
        page.locator(".jodit-wysiwyg").fill("UiTest")
        page.get_by_text("+添加标签").click()
        page.get_by_role("listitem", name="测试误删").click()
        with page.expect_file_chooser() as fc_info:
            page.get_by_role("button", name="上传附件").click()
        file_chooser = fc_info.value
        file_chooser.set_files(data_path + "/UiTest.jpg")
        page.locator("#formlist").get_by_text("未选择").click()
        page.get_by_text("默认表单").click()
        page.get_by_text("提交", exact=True).click()
        with allure.step("进入我提交"):
            page.get_by_text("我提交").click()
            element = page.get_by_text(self.pageVisitorTime)
            with allure.step("断言"):
                assert element is not None, "元素不存在"

    @allure.title("修改工单")
    def test_002(self, page):
        """
        检查点：
        * 1. 访客端消息发送成功校验访客端出现'会话创建成功'
          2. 校验访客端出现'会话已被客服接起'
          3. 校验客服端新增消息与访客发送时间戳一致
        """
        page.goto(customer_ticket_url)
        page.pause()
        print(self.pageVisitorTime)
        page.get_by_text("我提交").click()
        page.get_by_text(self.pageVisitorTime).click()
        page.get_by_text("编辑工单").click()
        page.get_by_text("UiTest", exact=True).nth(1).click()
        page.get_by_text("UiTest", exact=True).nth(1).fill("newUiTest")
        page.get_by_text("保存").click()
        with allure.step("断言"):
            element = page.get_by_text("newUiTest", exact=True).first
            assert element is not None, "元素不存在"

    @allure.title("开启并添加工单通知邮箱")
    def test_003(self, page):
        page.goto(manage_index_url)
        page.pause()
        self.__class__.email_time = get_nowtime()
        print(self.email_time)
        var = self.email_time + "@qq.com"
        page.get_by_text("设置", exact=True).click()
        page.get_by_text("通知邮箱").click()
        page.locator("input[name=\"username\"]").click()
        page.locator("input[name=\"username\"]").fill(var)
        page.locator("input[name=\"password\"]").click()
        page.locator("input[name=\"password\"]").fill(var)
        page.locator("input[name=\"server\"]").click()
        page.locator("input[name=\"server\"]").fill("ui")
        page.locator("input[name=\"port\"]").fill("993")
        page.get_by_role("button", name="保存").click()
        element_locator = page.get_by_text("已停用")
        print(element_locator.is_visible())
        if element_locator.is_visible():
            element_locator.click()
        element_locator = page.get_by_text("已启用")
        with allure.step("断言"):
            assert element_locator.is_visible(), "未成功点击已启用按钮"
            print(page.input_value('input[name="username"]'))
            assert page.input_value('input[name="username"]') == var, "输入框的值不一致"

    @allure.title("关闭工单通知邮箱")
    def test_004(self, page):
        page.goto(manage_index_url)
        page.pause()
        page.get_by_text("设置", exact=True).click()
        page.get_by_title("通知邮箱").click()
        element_locator = page.get_by_text("已启用")
        print(element_locator.is_visible())
        if element_locator.is_visible():
            element_locator.click()
        element_locator = page.get_by_text("已停用")
        with allure.step("断言"):
            assert element_locator.is_visible(), "未成功点击已停用按钮"

    @allure.title("添加工单分类")
    def test_005(self, page):
        page.goto(manage_index_url)
        page.pause()
        page.get_by_text("设置", exact=True).click()
        page.get_by_text("工单分类").click()
        page.get_by_text("添加标签").click()
        page.get_by_placeholder("输入标签名称").fill("UiTest")
        page.get_by_text("请选择左侧标签").click()
        page.reload()
        # element = page.query_selector('[title="UiTest"]')
        # print(element)
        target_text = "UiTest"
        element = page.query_selector(f':has-text("{target_text}")')
        print(element)
        with allure.step("断言"):
            assert element is not None, "创建失败"

    @allure.title("修改工单分类")
    def test_006(self, page):
        page.goto(manage_index_url)
        page.pause()
        page.get_by_text("设置", exact=True).click()
        page.get_by_text("工单分类").click()
        page.get_by_text("UiTest", exact=True).click()
        page.get_by_role("listitem").filter(has_text="UiTest").locator("span").nth(1).click()
        page.get_by_placeholder("会话标签 ").fill("newUiTest")
        page.get_by_text("添加标签").nth(1).click()
        page.get_by_text("保存").click()
        target_text = "newUiTest"
        element = page.query_selector(f':has-text("{target_text}")')
        print(element)
        with allure.step("断言"):
            assert element is not None, "修改失败"

    @allure.title("删除工单分类")
    def test_007(self, page):
        page.goto(manage_index_url)
        page.pause()
        page.get_by_text("设置", exact=True).click()
        page.get_by_text("工单分类").click()
        page.get_by_text("newUiTest", exact=True).click()
        page.get_by_role("listitem").filter(has_text="newUiTest").locator("span").nth(2).click()
        page.get_by_text("删除", exact=True).click()
        page.reload()
        target_text = "newUiTest"
        element = page.query_selector(f':has-text("{target_text}")')
        print(element)
        with allure.step("断言"):
            assert element is None, "删除失败"

    @allure.title("添加工单优先级")
    def test_008(self, page):
        page.goto(manage_index_url)
        page.pause()
        page.get_by_text("设置", exact=True).click()
        page.locator(".iScrollIndicator").click()
        page.get_by_text("工单优先级").click()
        page.locator("span").filter(has_text="新建优先级").locator("span").click()
        page.locator("input[name=\"name\"]").fill("界面测试")
        page.locator("input[name=\"name\"]").click()
        page.locator("input[name=\"enName\"]").click()
        page.locator("input[name=\"enName\"]").fill("UiTest")
        page.get_by_text("保存").click()
        page.reload()
        target_text = "UiTest"
        element = page.query_selector(f':has-text("{target_text}")')
        print(element)
        assert element is not None, "输入框的值不一致"

    @allure.title("修改工单优先级")
    def test_009(self, page):
        page.goto(manage_index_url)
        page.pause()
        page.get_by_text("设置", exact=True).click()
        page.locator(".iScrollIndicator").click()
        page.get_by_text("工单优先级").click()
        page.locator("li:nth-child(3) > .t3 > span > .font-edit").click()
        page.locator("input[name=\"enName\"]").fill("newUiTest")
        page.locator("input[name=\"enName\"]").click()
        page.get_by_text("保存").click()
        page.reload()
        element = page.get_by_text("newUiTest")
        print(element)
        assert element is not None, "输入框的值不一致"

    @allure.title("删除工单优先级")
    def test_010(self, page):
        page.goto(manage_index_url)
        page.pause()
        page.get_by_text("设置", exact=True).click()
        page.locator(".iScrollIndicator").click()
        page.get_by_text("工单优先级").click()
        page.locator("li:nth-child(3) > .t3 > span:nth-child(2) > .font-delete").click()
        page.reload()
        target_text = "newUiTest"
        element = page.query_selector(f':has-text("{target_text}")')
        print(element)
        assert element is None, "未删除"

    @allure.title("添加工单状态")
    def test_011(self, page):
        page.goto(manage_index_url)
        page.pause()
        page.get_by_text("设置", exact=True).click()
        page.locator(".iScrollIndicator").click()
        page.get_by_text("工单状态").click()
        page.get_by_role("button", name="plus 新增状态").click()
        page.get_by_label("选项名称", exact=True).click()
        page.get_by_label("选项名称", exact=True).fill("界面测试")
        page.get_by_label("选项名称英文").click()
        page.get_by_label("选项名称英文").fill("UiTest")
        page.get_by_role("button", name="确 定").click()
        page.reload()
        target_text = "UiTest"
        element = page.query_selector(f':has-text("{target_text}")')
        print(element)
        assert element is not None, "输入框的值不一致"


    @allure.title("修改工单状态")
    def test_012(self, page):
        page.goto(manage_index_url)
        page.pause()
        page.get_by_text("设置", exact=True).click()
        page.locator(".iScrollIndicator").click()
        page.get_by_text("工单状态").click()
        page.get_by_role("row", name="界面测试 UiTest 未指定 否 x 3").locator("span").nth(1).click()
        page.get_by_label("选项名称英文").click()
        page.get_by_label("选项名称英文").fill("newUiTest")
        page.get_by_role("button", name="确 定").click()
        page.reload()
        element = page.get_by_text("newUiTest")
        print(element)
        assert element is not None, "输入框的值不一致"

    @allure.title("删除工单状态")
    def test_013(self, page):
        page.goto(manage_index_url)
        page.pause()
        page.get_by_text("设置", exact=True).click()
        page.locator(".iScrollIndicator").click()
        page.get_by_text("工单状态").click()
        page.get_by_role("row", name="界面测试 newUiTest 未指定 否 x 3").locator("span").nth(3).click()
        page.reload()
        target_text = "newUiTest"
        element = page.query_selector(f':has-text("{target_text}")')
        print(element)
        assert element is None, "输入框的值不一致"