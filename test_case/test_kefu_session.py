import allure
from time import sleep
from common.util import get_nowtime
from playwright.sync_api import expect
from config import RunConfig



@allure.feature('基础会话')
class TestSession():


    @allure.story("会话自动接入")
    def test_001(self, page):
        """
        名称：1.用例名称 = 设置坐席状态-空闲 2.用例名称 = 设置坐席最大接待数-1
        步骤：
        1、打开浏览器
        2、输入 url sandbox.kefu.easemob.com
        3、点击搜索按钮
        检查点：
        * 1. 访客端消息发送成功校验访客端出现'会话创建成功'
          2. 校验访客端出现'会话已被客服接起'
          3. 校验客服端新增消息与访客发送时间戳一致
        """

        page.goto(RunConfig.customerServiceUrl)
        page.locator(".newagentfont-chatstate").click()
        page.get_by_text("空闲").click()
        page.get_by_title("工作台设置").click()
        page.get_by_role("spinbutton").get_by_role("textbox").click()
        page.get_by_role("spinbutton").get_by_role("textbox").fill("1")
        page.get_by_text("保存").click()

        page1 = page.context.new_page()
        page1.goto(RunConfig.visitorUrl)
        page.pause()

        page1.get_by_placeholder("点击输入内容...").click()
        pageVisitorTime = get_nowtime()
        page1.get_by_placeholder("点击输入内容...").fill(pageVisitorTime)
        # 网络等待时间 不一定这么久
        sleep(3)

        page1.get_by_placeholder("点击输入内容...").press("Enter")

        # 网络等待时间 不一定这么久
        # 断言
        sleep(3)
        expect(page1.get_by_text("会话创建成功")).not_to_be_empty()
        expect(page1.get_by_text("会话已被客服接起")).not_to_be_empty()
        expect(page.get_by_text(pageVisitorTime)).not_to_be_empty()

    @allure.story("客服发送消息")
    def test_002(self, page):
        """
        名称：1.用例名称 = 会话自动接入
        步骤：
        1. 客服端输入框输入“当前时间戳”，点击发送按钮
        检查点：
        * 1. 客服端消息发送成功校验访客端新增消息访客服送时间戳一致
        """
        page.goto(RunConfig.customerServiceUrl)
        pageCustomerServiceTime = get_nowtime()
        page.pause()
        page.get_by_placeholder("请输入...").click()
        page.get_by_placeholder("请输入...").fill(pageCustomerServiceTime)
        sleep(3)
        page.get_by_placeholder("请输入...").press("Enter")

        page.goto(RunConfig.visitorUrl)
        page.pause()
        expect(page.get_by_text(pageCustomerServiceTime)).not_to_be_empty()




    @allure.story("客服发送满意度邀请")
    def test_003(self, page):
        """
            名称：1..用例名称 = 会话自动接入
            步骤：
            1. 客服端点击“邀请评价”按钮，确认发送评价邀请
            2. 查看访客端服务评价弹窗，选择“1星”“已解决”输入评价内容“uiTest”，点击“提交评价”按钮
            检查点：
            * 1. 客服端邀请发送成功校验客服端出现'评价邀请已发送'
              2. 访客端收到评价邀请
              校验访客端展示服务评价弹窗
              校验访客端弹出提交成功提醒校验客服端出现'访客已评价：1分，非常不满意'
         """
        page.goto(RunConfig.customerServiceUrl)
        page.pause()
        sleep(5)
        page.get_by_title("邀请评价").locator("span").first.click()
        page.locator("div:nth-child(41) > div > div:nth-child(3) > span").first.click()

        expect(page.get_by_text("评价邀请已发送")).not_to_be_empty()

        page.goto(RunConfig.visitorUrl)
        page.pause()
        sleep(5)

        expect(page.get_by_text("立即评价")).not_to_be_empty()

        page.get_by_role("button", name="立即评价").click()

        page.get_by_role("listitem", name="非常不满意").click()
        page.get_by_text("已解决").click()
        page.get_by_placeholder("请输入评价内容").click()
        page.get_by_placeholder("请输入评价内容").fill("uiTest")
        page.get_by_text("提交评价").click()

        expect(page.get_by_text("提交成功")).not_to_be_empty()

        page.goto(RunConfig.customerServiceUrl)
        sleep(5)
        expect(page.get_by_text("访客已评价：1分，非常不满意")).not_to_be_empty()

        page.pause()

    @allure.story("客服关闭会话")
    def test_004(self, page):
        """
        1.用例名称 = 控制会话标签强制性-关闭
        2.用例名称 = 会话自动接入
        步骤：
        1. 客服端点击会话结束按钮
        检查点： 1. 会话成功关闭校验会话列表该访客会话消失
        """
        page.goto(RunConfig.customerServiceUrl)
        page.pause()
        page.get_by_title("结束会话").click()
        sleep(5)
        expect(page.get_by_text("暂无访客")).not_to_be_empty()

        page.goto(RunConfig.visitorUrl)
        sleep(5)
        expect(page.get_by_text("会话已结束")).not_to_be_empty()

        page.pause()


