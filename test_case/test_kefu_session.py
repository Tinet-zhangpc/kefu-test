import allure
from time import sleep
from common.util import get_nowtime
from playwright.sync_api import expect
from common.page_url import *


@allure.feature('基础会话')
@allure.testcase(customer_service_url, '测试用例链接-客服端')
@allure.testcase(visitor_url, '测试用例链接-访客端')
@allure.testcase(visitor_url, '测试用例工单链接-jira地址')
class TestSession:

    # 标识会话用户昵称
    userName = None

    @allure.title("会话自动接入")
    def test_001(self, page):
        """
        检查点：
        * 1. 访客端消息发送成功校验访客端出现'会话创建成功'
          2. 校验访客端出现'会话已被客服接起'
          3. 校验客服端新增消息与访客发送时间戳一致
        """
        page.goto(customer_service_url)
        page.locator(".newagentfont-chatstate").click()
        with allure.step("设置坐席状态-空闲"):
            page.get_by_text("空闲").click()

        with allure.step("设置坐席最大接待数=1"):
            page.get_by_title("工作台设置").click()
            page.get_by_role("spinbutton").get_by_role("textbox").click()
            page.get_by_role("spinbutton").get_by_role("textbox").fill("1")
            page.get_by_text("保存").click()

        with allure.step("访客端输入框输入“当前时间戳”，点击发送按钮"):
            page1 = page.context.new_page()
            page1.goto(visitor_url)
            page1.get_by_placeholder("点击输入内容...").click()
            pageVisitorTime = get_nowtime()
            page1.get_by_placeholder("点击输入内容...").fill(pageVisitorTime)
            # 网络等待时间 不一定这么久
            sleep(3)
            page1.get_by_placeholder("点击输入内容...").press("Enter")
        with allure.step("断言"):
            # 断言
            sleep(3)
            expect(page1.get_by_text("会话创建成功")).not_to_be_empty()
            expect(page1.get_by_text("会话已被客服接起")).not_to_be_empty()
            expect(page.get_by_text(pageVisitorTime)).not_to_be_empty()

    @allure.title("客服发送消息")
    def test_002(self, page):
        """
        检查点：
        * 1. 客服端消息发送成功校验访客端新增消息访客服送时间戳一致
        """
        self.userName
        page.goto(customer_service_url)
        with allure.step("客服端输入框输入“当前时间戳”，点击发送按钮"):

            pageCustomerServiceTime = get_nowtime()
            page.pause()
            page.get_by_placeholder("请输入...").click()
            page.get_by_placeholder("请输入...").fill(pageCustomerServiceTime)
            sleep(3)
            page.get_by_placeholder("请输入...").press("Enter")
            element = page.get_by_placeholder("昵称", exact=True)
            element.click()
            userName = element.get_attribute("value")
            print(userName)
        with allure.step("返回客户端页面"):
            page.goto(visitor_url)
        with allure.step("断言"):
            expect(page.get_by_text(pageCustomerServiceTime)).not_to_be_empty()

    @allure.title("客服发送满意度邀请")
    def test_003(self, page):
        """
            检查点：
            * 1. 客服端邀请发送成功校验客服端出现'评价邀请已发送'
              2. 访客端收到评价邀请
              校验访客端展示服务评价弹窗
              校验访客端弹出提交成功提醒校验客服端出现'访客已评价：1分，非常不满意'
         """
        with allure.step("发送邀请评价"):
            page.goto(customer_service_url)
            sleep(5)
            page.get_by_title("邀请评价").locator("span").first.click()
            page.locator("div:nth-child(41) > div > div:nth-child(3) > span").first.click()
        with allure.step("断言评价邀请已发送"):
            expect(page.get_by_text("评价邀请已发送")).not_to_be_empty()
        with allure.step("回到客户端页面"):
            page.goto(visitor_url)
            sleep(5)
        with allure.step("断言是否弹出立即评价"):
            expect(page.get_by_text("立即评价")).not_to_be_empty()
        with allure.step("点击立即评价弹出弹框"):
            page.get_by_role("button", name="立即评价").click()
        with allure.step("编辑评价评价内容，提交评价"):
            page.get_by_role("listitem", name="非常不满意").click()
            page.get_by_text("已解决").click()
            page.get_by_placeholder("请输入评价内容").click()
            page.get_by_placeholder("请输入评价内容").fill("uiTest")
            page.get_by_text("提交评价").click()
        with allure.step("断言: 提交成功"):
            expect(page.get_by_text("提交成功")).not_to_be_empty()

        page.goto(
            customer_service_url)
        sleep(5)
        with allure.step("断言: 访客已评价：1分，非常不满意"):
            expect(page.get_by_text("访客已评价：1分，非常不满意")).not_to_be_empty()
        page.pause()

    @allure.title("客服关闭会话")
    def test_004(self, page):
        """
        检查点： 1. 会话成功关闭校验会话列表该访客会话消失
        """
        with allure.step("客服端点击会话结束按钮"):
            page.goto(customer_service_url)
            sleep(5)
            page.get_by_title("结束会话").click()
            sleep(5)
        with allure.step("断言: 话列表该访客会话列表暂无访客"):
            expect(page.get_by_text("暂无访客")).not_to_be_empty()

        page.goto(visitor_url)
        sleep(5)
        with allure.step("断言: 客端出现'会话已结束"):
            expect(page.get_by_text("会话已结束")).not_to_be_empty()
        page.pause()

    @allure.title("验证历史会话详情")
    def test_005(self, page):
        """
        1.校验历史会话记录列表新增一条访客昵称一致的数据
        2.校验客户信息记录列表新增一条访客昵称一致的数据
        3.校验基础质检记录列表新增一条访客昵称一致的数据
        """
        pass
        print(self.userName)
        page.goto(manage_index_url)
        sleep(5)
        page.get_by_text("历史", exact=True).click()
        with allure.step("进入会话记录"):
            page.get_by_title("会话记录").click()
        with allure.step("断言: 校验历史会话记录列表新增一条访客昵称一致的数据"):
            expect(page.get_by_text(self.userName)).not_to_be_empty()
        with allure.step("进入客户信息/自定义筛选条件"):
            page.get_by_title("客户信息").click()
            page.get_by_text("自定义筛选条件").click()
        with allure.step("断言: 校验客户信息记录列表新增一条访客昵称一致的数据"):
            expect(page.get_by_text(self.userName)).not_to_be_empty()
        with allure.step("进入会话记录"):
            page.locator("[id=\"single-spa-application\\:\\@kefu\\/pt-layout\"]").get_by_text("质检", exact=True).click()
            page.get_by_text("会话质检", exact=True).click()
            page.get_by_title("基础质检").click()
        with allure.step("断言: 校验基础质检记录列表新增一条访客昵称一致的数据"):
            expect(page.get_by_text(self.userName)).not_to_be_empty()