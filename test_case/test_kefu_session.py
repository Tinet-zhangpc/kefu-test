import re

import allure
from common.util import get_nowtime
from playwright.sync_api import expect
from common.page_url import *
from datetime import datetime
from time import sleep

@allure.feature('基础会话')
@allure.testcase(customer_service_url, '测试用例链接-客服端')
@allure.testcase(visitor_url, '测试用例链接-访客端')
@allure.testcase(visitor_url, '测试用例工单链接-jira地址')
class TestSession:
    # 标识会话用户昵称
    userName = None
    # 标识会话用户发送的数据
    pageVisitorTime = None
    # 发起时间
    start_time = None
    # 接起时间
    pick_up_time = None

    @allure.title("会话自动接入")
    def test_001(self, page):
        """
        检查点：
        * 1. 访客端消息发送成功校验访客端出现'会话创建成功'
          2. 校验访客端出现'会话已被客服接起'
          3. 校验客服端新增消息与访客发送时间戳一致
        """
        page.goto(customer_service_url)
        page.pause()
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
            self.__class__.pageVisitorTime = get_nowtime()
            print(self.pageVisitorTime)
            page1.get_by_placeholder("点击输入内容...").fill(self.pageVisitorTime)

            page1.get_by_placeholder("点击输入内容...").press("Enter")
        with allure.step("断言"):
            expect(page1.get_by_text("会话创建成功")).not_to_be_empty()
            expect(page1.get_by_text("会话已被客服接起")).not_to_be_empty()
            page1.close()
            expect(page.get_by_text(self.pageVisitorTime)).not_to_be_empty()

    @allure.title("客服发送消息")
    def test_002(self, page):
        """
        检查点：
        * 1. 客服端消息发送成功校验访客端新增消息访客服送时间戳一致
        """
        page.goto(customer_service_url)
        with allure.step("客服端输入框输入“当前时间戳”，点击发送按钮"):
            pageCustomerServiceTime = get_nowtime()
            page.get_by_placeholder("请输入...").click()
            page.get_by_placeholder("请输入...").fill(pageCustomerServiceTime)
            # sleep(3)
            page.get_by_placeholder("请输入...").press("Enter")

            # 使用选择器定位元素并获取 value 值
            self.__class__.userName = page.input_value('input[name="nickname"]')
            print(self.userName)
            print(self.__class__.userName)
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
            page.get_by_title("邀请评价").locator("span").first.click()
            page.locator("div:nth-child(41) > div > div:nth-child(3) > span").first.click()
        with allure.step("断言评价邀请已发送"):
            expect(page.get_by_text("评价邀请已发送")).not_to_be_empty()
        with allure.step("回到客户端页面"):
            page.goto(visitor_url)
        with allure.step("断言是否弹出立即评价"):
            expect(page.get_by_text("立即评价")).not_to_be_empty()
        with allure.step("点击立即评价弹出弹框"):
            element = page.get_by_text("服务评价")
            if element.is_visible():
                print("直接弹出了服务评价， 不点击立即评价了")
            else:
                page.get_by_role("button", name="立即评价").click()
        with allure.step("编辑评价评价内容，提交评价"):
            page.get_by_role("listitem", name="非常不满意").click()
            page.get_by_text("已解决").click()
            page.get_by_placeholder("请输入评价内容").click()
            page.get_by_placeholder("请输入评价内容").fill("uiTest")
            page.get_by_text("提交评价").click()
        with allure.step("断言: 提交成功"):
            expect(page.get_by_text("提交成功")).not_to_be_empty()

        page.goto(customer_service_url)
        with allure.step("断言: 访客已评价：1分，非常不满意"):

            expect(page.get_by_text("访客已评价：1分，非常不满意")).not_to_be_empty()

    @allure.title("客服关闭会话")
    def test_004(self, page):
        """
        检查点： 1. 会话成功关闭校验会话列表该访客会话消失
        """
        with allure.step("客服端点击会话结束按钮"):
            page.goto(customer_service_url)
            page.get_by_title("结束会话").click()
        with allure.step("断言: 话列表该访客会话列表暂无访客"):
            expect(page.get_by_text("暂无访客")).not_to_be_empty()
        page.goto(visitor_url)
        with allure.step("断言: 访客端出现'会话已结束"):
            expect(page.get_by_text("会话已结束")).not_to_be_empty()

    @allure.title("验证历史会话新增")
    def test_005(self, page):
        """
        1.校验历史会话记录列表新增一条访客昵称一致的数据
        2.校验客户信息记录列表新增一条访客昵称一致的数据
        3.校验基础质检记录列表新增一条访客昵称一致的数据
        """
        print(self.__class__.userName)
        print(self.userName)
        page.goto(manage_index_url)
        page.get_by_text("历史", exact=True).click()
        with allure.step("进入会话记录"):
            page.get_by_title("会话记录").click()
        with allure.step("断言: 校验历史会话记录列表新增一条访客昵称一致的数据"):
            expect(page.locator("#em-history").get_by_text(self.userName)).not_to_be_empty()
        with allure.step("进入客户信息/自定义筛选条件"):
            page.get_by_title("客户信息").click()
            page.get_by_text("自定义筛选条件").click()
        with allure.step("断言: 校验客户信息记录列表新增一条访客昵称一致的数据"):
            expect(page.locator("#em-visitors").get_by_text(self.userName)).not_to_be_empty()
        with allure.step("进入会话记录"):
            page.locator("[id=\"single-spa-application\\:\\@kefu\\/pt-layout\"]").get_by_text("质检", exact=True).click()
            page.get_by_title("基础质检").click()
        with allure.step("断言: 校验基础质检记录列表新增一条访客昵称一致的数据"):
            expect(page.locator("#em-qualitycheck").get_by_text(self.userName)).not_to_be_empty()

    @allure.title("验证历史会话详情")
    def test_006(self, page):
        """
        1.校验历史会话记录详情中有数据
        """
        print(self.__class__.userName)
        page.goto(manage_index_url)
        page.get_by_text("历史", exact=True).click()
        with allure.step("进入会话记录"):
            page.get_by_title("会话记录").click()
        with allure.step("进入会话记录详情"):
            page.locator("#em-history").get_by_text(self.userName).click()
        with allure.step("断言: 校验历史会话记录详情中有数据"):
            page.input_value('input[name="nickname"]')
            assert page.input_value('input[name="nickname"]') != '', "输入框的值不能为空"
            expect(page.get_by_text(self.pageVisitorTime).first).not_to_be_empty()
        with allure.step("记录: 进入记录标记时间"):
            page.get_by_text("记录", exact=True).click()

            element = page.get_by_role("listitem").filter(has_text="发起会话")
            # 提取时间文本
            self.__class__.start_time = element.inner_text().splitlines()[1]
            print(self.start_time)  # 输出文本内容
            element = page.get_by_role("listitem").filter(has_text="将待接入会话手动接起")
            # 提取时间文本
            self.__class__.pick_up_time = element.inner_text().splitlines()[1]
            print(self.pick_up_time)  # 输出文本内容

    @allure.title("验证客户详情并修改")
    def test_007(self, page):
        """
        1.校验返回列表名字项数据正确
        """
        print(self.__class__.userName)
        page.goto(manage_index_url)
        with allure.step("进入历史"):
            page.get_by_text("历史", exact=True).click()
            page.get_by_title("客户信息").click()
            page.get_by_text("自定义筛选条件").click()
            page.locator("#em-visitors").get_by_text(self.userName).click()
            page.get_by_placeholder("真实姓名").click()
            page.get_by_placeholder("真实姓名").press("Meta+a")
            page.get_by_placeholder("真实姓名").fill("name")
            page.get_by_placeholder("昵称").click()
            page.locator(".button-close > .font-close").click()
        # 重新加载页面
        with allure.step("重新加载页面"):
            page.reload()
        element = page.get_by_role("listitem").filter(has_text=self.userName)
        # 或者判断元素内是否包含指定的文本内容
        print(element.inner_text())
        is_contain_name = 'name' in element.inner_text()
        print(is_contain_name)
        with allure.step("断言: 校验返回列表名字项数据正确"):
            assert is_contain_name

    @allure.title("基础质检评分")
    def test_008(self, page):
        """
        1.校验返回列表名字项数据正确
        """
        print(self.__class__.userName)
        page.goto(manage_index_url)
        with allure.step("进入质检内容"):
            page.locator("[id=\"single-spa-application\\:\\@kefu\\/pt-layout\"]").get_by_text("质检", exact=True).click()
            page.get_by_title("基础质检").click()
        with allure.step("编辑评分"):
            page.locator("#em-qualitycheck").get_by_text(self.userName).click()
            page.locator("span").filter(has_text=re.compile(r"^质检$")).click()
            page.locator("span").filter(has_text=re.compile(r"^评分$")).click()
            page.get_by_placeholder("0-5").click()
            page.get_by_placeholder("0-5").press("Meta+a")
            page.get_by_placeholder("0-5").fill("2")
            page.get_by_text("保存", exact=True).click()
            page.locator(".em-chat-readonly-detail > div > a").first.click()
            element = page.get_by_role("listitem").filter(has_text=self.userName)
            # 或者判断元素内是否包含指定的文本内容
            print(element.inner_text())
        is_contain_name = '2' in element.inner_text()
        print(is_contain_name)
        with allure.step("断言: 校验返回列表评分项数据正确"):
            assert is_contain_name

    @allure.title("工作量筛选")
    def test_009(self, page):
        """
        1.客服端点击管理员模式 统计>在线客服>工作量，点击筛选排序，按照客服接起会话时间-1秒，+1秒进行筛选
        """
        print(self.__class__.userName)
        print(self.start_time)
        print(self.pick_up_time)
        dt = datetime.strptime(self.pick_up_time, '%Y-%m-%d %H:%M:%S')

        hour = dt.hour  # 提取小时
        minute = dt.minute  # 提取分钟
        second = dt.second - 1  # 提取秒钟

        page.goto(manage_index_url)
        with allure.step("进入筛选界面"):
            page.get_by_text("统计", exact=True).click()
            page.get_by_title("工作量").click()
            page.get_by_text("筛选排序").click()
        with allure.step("配置筛选条件"):
            page.locator("span").filter(has_text="本周").locator("label").click()
            page.get_by_role("listitem", name="今天").click()
            page.get_by_placeholder("开始时间").click()
            page.get_by_role("definition").filter(
                has_text=re.compile(r"^000102030405060708091011121314151617181920212223$")). \
                get_by_role("combobox").select_option(str(hour))
            page.get_by_role("combobox").nth(1).select_option(str(minute))
            page.get_by_role("combobox").nth(2).select_option(str(second))

            second = dt.second + 1  # 提取秒钟
            page.get_by_placeholder("结束时间").click()
            page.get_by_role("definition").filter(
                has_text=re.compile(r"^000102030405060708091011121314151617181920212223$")). \
                get_by_role("combobox").select_option(str(hour))
            page.get_by_role("combobox").nth(1).select_option(str(minute))
            page.get_by_role("combobox").nth(2).select_option(str(second))

            page.get_by_text("筛选查询").click()
        element = page.get_by_role("row", name="结束会话数 ꀓ 1 条", exact=True).get_by_text("1")
        print(element)
        with allure.step("断言: 校验返回列表各项数据正确"):
            expect(element).not_to_be_empty()

    @allure.title("工作质量筛选")
    def test_010(self, page):
        """
        1.客服端点击管理员模式 统计>在线客服>工作量，点击筛选排序，按照客服接起会话时间-1秒，+1秒进行筛选
        """
        print(self.__class__.userName)
        print(self.start_time)
        print(self.pick_up_time)
        dt = datetime.strptime(self.pick_up_time, '%Y-%m-%d %H:%M:%S')

        hour = dt.hour  # 提取小时
        minute = dt.minute  # 提取分钟
        second = dt.second - 1  # 提取秒钟

        page.goto(manage_index_url)
        with allure.step("进入筛选界面"):
            page.get_by_text("统计", exact=True).click()
            page.get_by_title("工作质量").click()
        with allure.step("进入筛选界面"):
            page.locator("#em-workquality").get_by_text("筛选排序").click()
            page.locator("span").filter(has_text="本周").locator("label").click()
        page.get_by_role("listitem", name="今天").click()
        page.get_by_placeholder("开始时间").click()
        page.get_by_role("definition").filter(
            has_text=re.compile(r"^000102030405060708091011121314151617181920212223$")).get_by_role(
            "combobox").select_option(str(hour))
        page.get_by_role("combobox").nth(1).select_option(str(minute))
        page.get_by_role("combobox").nth(2).select_option(str(second))
        second = dt.second + 1  # 提取秒钟
        page.get_by_placeholder("结束时间").click()
        page.get_by_role("definition").filter(
            has_text=re.compile(r"^000102030405060708091011121314151617181920212223$")).get_by_role(
            "combobox").select_option(str(hour))
        page.get_by_role("combobox").nth(1).select_option(str(minute))
        page.get_by_role("combobox").nth(2).select_option(str(second))
        page.get_by_text("筛选查询").click()
        with allure.step("断言: 校验返回列表各项数据正确"):
            element = page.get_by_role("cell", name="1分")
            expect(element).not_to_be_empty()

    @allure.title("访客统计筛选")
    def test_011(self, page):
        """
        1.客服端点击管理员模式 统计>在线客服>工作量，点击筛选排序，按照客服接起会话时间-1秒，+1秒进行筛选
        """
        print(self.__class__.userName)
        print(self.start_time)
        print(self.pick_up_time)
        dt = datetime.strptime(self.start_time, '%Y-%m-%d %H:%M:%S')

        hour = dt.hour  # 提取小时
        minute = dt.minute  # 提取分钟
        second = dt.second - 1  # 提取秒钟

        page.goto(manage_index_url)
        page.get_by_text("统计", exact=True).click()
        page.get_by_title("访客统计").click()
        page.locator("#em-visitorSource").get_by_text("筛选排序").click()
        page.locator("span").filter(has_text="本周").locator("label").click()
        page.get_by_role("listitem", name="今天").click()
        page.get_by_placeholder("开始时间").click()
        page.get_by_role("definition").filter(
            has_text=re.compile(r"^000102030405060708091011121314151617181920212223$")).get_by_role(
            "combobox").select_option(str(hour))
        page.get_by_role("combobox").nth(1).select_option(str(minute))
        page.get_by_role("combobox").nth(2).select_option(str(second))
        second = dt.second + 1  # 提取秒钟
        page.get_by_placeholder("结束时间").click()
        page.get_by_role("definition").filter(
            has_text=re.compile(r"^000102030405060708091011121314151617181920212223$")).get_by_role(
            "combobox").select_option(str(hour))
        page.get_by_role("combobox").nth(1).select_option(str(minute))
        page.get_by_role("combobox").nth(2).select_option(str(second))

        page.get_by_text("筛选查询").click()
        with allure.step("断言: 校验返回列表各项数据正确"):
            element = page.get_by_role("cell", name="独立访客数 ꀓ 1")
            expect(element).not_to_be_empty()

    @allure.title("排队统计筛选")
    def test_012(self, page):
        """
        1.客服端点击管理员模式 统计>在线客服>工作量，点击筛选排序，按照客服接起会话时间-1秒，+1秒进行筛选
        """
        print(self.__class__.userName)
        print(self.start_time)
        print(self.pick_up_time)
        dt = datetime.strptime(self.start_time, '%Y-%m-%d %H:%M:%S')

        hour = dt.hour  # 提取小时
        minute = dt.minute  # 提取分钟
        second = dt.second - 1  # 提取秒钟

        page.goto(manage_index_url)
        page.get_by_text("统计", exact=True).click()
        page.get_by_text("排队统计").click()
        page.locator("#em-queue").get_by_text("筛选排序").click()
        page.locator("span").filter(has_text="本周").locator("label").click()
        page.get_by_role("listitem", name="今天").click()
        page.get_by_placeholder("开始时间").click()
        page.get_by_role("definition").filter(
            has_text=re.compile(r"^000102030405060708091011121314151617181920212223$")).get_by_role(
            "combobox").select_option(str(hour))
        page.get_by_role("combobox").nth(1).select_option(str(minute))
        page.get_by_role("combobox").nth(2).select_option(str(second))
        second = dt.second + 1  # 提取秒钟
        page.get_by_placeholder("结束时间").click()
        page.get_by_role("definition").filter(
            has_text=re.compile(r"^000102030405060708091011121314151617181920212223$")).get_by_role(
            "combobox").select_option(str(hour))
        page.get_by_role("combobox").nth(1).select_option(str(minute))
        page.get_by_role("combobox").nth(2).select_option(str(second))

        page.get_by_text("筛选查询").click()
        with allure.step("断言: 校验返回列表各项数据正确"):
            element = page.get_by_role("cell", name="1").first
            expect(element).not_to_be_empty()

    @allure.title("验证客服排队中会话")
    def test_013(self, page):
        """
       1.访客端消息发送成功校验访客端出现'会话创建成功校验访客端出现‘当前排队人数为1
       2. 待接入列表新增一条数据，点击查看数据详情校验待接入tab角标=1校验会话包含的访客消息与访客发送时间戳一致
        """
        page.goto(customer_service_url)
        page.locator(".newagentfont-chatstate").click()
        with allure.step("设置坐席状态-空闲"):
            page.get_by_text("忙碌").click()
            element = page.get_by_text("修改在线状态")
            if element.is_visible():
                page.locator("div:nth-child(42) > div > div:nth-child(3) > span").first.click()
            else:
                print("元素不存在")
        with allure.step("设置坐席最大接待数=1"):
            page.get_by_title("工作台设置").click()
            page.get_by_role("spinbutton").get_by_role("textbox").click()
            page.get_by_role("spinbutton").get_by_role("textbox").fill("1")
            page.get_by_text("保存").click()
        with allure.step("访客端输入框输入“当前时间戳”，点击发送按钮"):
            page.goto(visitor_url)
            page.get_by_placeholder("点击输入内容...").click()
            self.__class__.pageVisitorTime = get_nowtime()
            print(self.pageVisitorTime)
            page.get_by_placeholder("点击输入内容...").fill(self.pageVisitorTime)
            page.get_by_placeholder("点击输入内容...").press("Enter")
        with allure.step("断言"):
            expect(page.get_by_text("会话创建成功")).not_to_be_empty()
            expect(page.get_by_text("当前排队人数为1")).not_to_be_empty()
            page.goto(customer_service_url)
        with allure.step("断言"):
            sleep(3)
            expect(page.get_by_text("待接入 1")).not_to_be_empty()
        page.get_by_text("待接入", exact=True).click()
        page.locator("#em-wait").get_by_role("img").click()
        # print(page.get_by_text(self.pageVisitorTime).inner_text())
        with allure.step("断言"):
            expect(page.get_by_text(self.pageVisitorTime).first).not_to_be_empty()

    @allure.title("验证管理员排队中会话")
    def test_014(self, page):
        """
        1.排队列表新增一条数据，点击查看校验会话包含的访客消息与访客发送F致
        """
        page.goto(manage_index_url)
        page.get_by_text("监控", exact=True).click()
        page.get_by_text("当前服务").click()
        page.get_by_text("当前服务").click()
        page.get_by_text("排队中会话").click()
        page.locator("#em-wait").get_by_role("img").click()
        with allure.step("断言"):
            expect(page.get_by_text(self.pageVisitorTime).first).not_to_be_empty()

    @allure.title("排队中会话客服手动接起")
    def test_015(self, page):
        """
        1.，查看客服模式-在线工作台-待接入，点击当前非队会话的接起按钮
        """
        print(self.__class__.userName)
        print(self.start_time)
        print(self.pick_up_time)

        page.goto(customer_service_url)
        page.get_by_text("待接入").click()
        page.get_by_title("接入").locator("span").click()
        page.get_by_text("会话", exact=True).click()
        # page.get_by_text("待接入 0").click()
        self.__class__.userName = page.get_by_placeholder("昵称", exact=True).input_value()
        print(page.get_by_placeholder("昵称", exact=True).input_value())
        print(self.__class__.userName)
        with allure.step("断言"):
            expect(page.get_by_text(self.pageVisitorTime).first).not_to_be_empty()
            expect(page.get_by_text("待接入 0")).not_to_be_empty()

    @allure.title("验证管理员进行中会话")
    def test_016(self, page):
        """
        1..进行中列表新增一条数据，点击查看数据详情校验会话包含的访客消息与访客发送时间戳一致
        """
        print(self.__class__.userName)
        print(self.start_time)
        print(self.pick_up_time)

        page.goto(manage_index_url)
        page.get_by_text("监控", exact=True).click()
        page.get_by_title("进行中会话").click()
        page.locator("#em-session").get_by_text(self.userName).click()

        with allure.step("断言"):
            expect(page.get_by_text(self.pageVisitorTime).first).not_to_be_empty()

    @allure.title("验证管理员关闭进行中会话")
    def test_017(self, page):
        """
        1.进行中列表该数据消失校验待接入列表无数据
        2. 点击刷新按钮校验进行中列表无数据
        """
        print(self.__class__.userName)
        print(self.start_time)
        print(self.pick_up_time)

        page.goto(manage_index_url)
        page.get_by_text("监控", exact=True).click()
        page.get_by_title("进行中会话").click()
        page.locator("#em-session").filter(has_text=self.userName).get_by_title("结束会话").locator("span").click()
        page.get_by_text("关闭", exact=True).click()
        with allure.step("断言"):
            expect(page.locator("#em-session").get_by_text("无数据")).not_to_be_empty()
        with allure.step("进入排队中会话"):
            page.get_by_title("排队中会话").click()
        with allure.step("断言"):
            expect(page.locator("#em-wait").get_by_text("无数据")).not_to_be_empty()

    @allure.title("客服发送表情消息")
    def test_018(self, page):
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
            self.__class__.pageVisitorTime = get_nowtime()
            print(self.pageVisitorTime)
            page1.get_by_placeholder("点击输入内容...").fill(self.pageVisitorTime)
            page1.get_by_placeholder("点击输入内容...").press("Enter")
        with allure.step("断言"):
            expect(page1.get_by_text("会话创建成功")).not_to_be_empty()
            expect(page1.get_by_text("会话已被客服接起")).not_to_be_empty()
            page1.close()
            expect(page.get_by_text(self.pageVisitorTime)).not_to_be_empty()
        page.goto(customer_service_url)
        with allure.step("客服端输入框输入“当前时间戳”，点击发送按钮"):
            page.get_by_title("表情").locator("span").click()
            page.locator(".ui-itm-emogrid > img").first.click()
            page.locator("#em-chat").get_by_text("发送", exact=True).click()
        with allure.step("返回客户端页面"):
            page.goto(visitor_url)
        element = page.get_by_role('img')
        print(element)
        with allure.step("断言"):
            assert element is not None, "元素不存在"

    @allure.title("访客添加留言")
    def test_019(self, page):
        page.goto(visitor_url)
        with allure.step("客服端输入框输入“当前时间戳”，点击发送按钮"):
            page.get_by_title("留言").first.click()
            self.__class__.pageVisitorTime = get_nowtime()
            print(self.pageVisitorTime)
            page.frame_locator("#easemob-iframe-note").get_by_placeholder("姓名").click()
            page.frame_locator("#easemob-iframe-note").get_by_placeholder("姓名").fill(self.pageVisitorTime)
            page.frame_locator("#easemob-iframe-note").get_by_placeholder("手机号").click()
            page.frame_locator("#easemob-iframe-note").get_by_placeholder("手机号").fill("18000000000")
            page.frame_locator("#easemob-iframe-note").get_by_placeholder("邮箱").click()
            page.frame_locator("#easemob-iframe-note").get_by_placeholder("邮箱").fill("UiTest@qq.com")
            page.frame_locator("#easemob-iframe-note").get_by_placeholder("请输入留言").fill("UiTestContent")
            page.frame_locator("#easemob-iframe-note").locator("div").filter(has_text=re.compile(r"^留言$")).click()
        with allure.step("返回客户端页面"):
            page.goto(manage_index_url)
            page.get_by_text("历史", exact=True).click()
            page.get_by_title("留言").click()
            element = page.get_by_text(self.pageVisitorTime)
        print(element)
        with allure.step("断言"):
            assert element is not None, "元素不存在"

    @allure.title("客服发送常用语")
    def test_020(self, page):
        page.goto(customer_service_url)
        with allure.step("进入客服发送常用语"):
            page.get_by_role("listitem", name="常用语").get_by_text("常用语").click()
            page.get_by_role("heading", name="W 欢迎语：").locator("span").nth(1).click()
            page.get_by_text("您好!很高兴为您服务，有什么可以为您效劳的。").click()
            page.locator("#em-chat").get_by_text("发送", exact=True).click()
        with allure.step("返回访客端页面"):
            page.goto(visitor_url)
            element = page.get_by_text("您好!很高兴为您服务，有什么可以为您效劳的。")
        print(element)
        with allure.step("断言"):
            assert element is not None, "元素不存在"

    @allure.title("客服发送知识库")
    def test_021(self, page):
        page.goto(customer_service_url)
        with allure.step("进入客服发送知识库"):
            try:
                page.get_by_text("展开").click(timeout=3000)
            except Exception:
                print("没有按钮不点击了")
            page.get_by_role("listitem", name="知识库").get_by_text("知识库").click()
            page.locator("#em-chat").get_by_title("用例测试勿删").click()
            page.locator(".newagentfont-send").click()
        with allure.step("返回访客端页面"):
            page.goto(visitor_url)
            element = page.get_by_text('用例测试勿删')
            print(element)
        with allure.step("断言"):
            assert element is not None, "元素不存在"


    @allure.title("客服添加会话标签")
    def test_022(self, page):
        """
        检查点：
        * 1. 客服端消息发送成功校验访客端新增消息访客服送时间戳一致
        """
        page.goto(customer_service_url)
        page.reload()
        with allure.step("进入客服添加会话标签"):
            page.get_by_title("会话标签").first.click()
            page.get_by_text("咨询").click()
            page.get_by_text("功能咨询").click()
            page.get_by_placeholder("添加备注").click()
            page.get_by_placeholder("添加备注").fill("Uitest")
            page.get_by_text("保存").click()
            element = page.locator(".em-summary-tag")
            print(element)
            page.get_by_text("会话备注")
            print(element)
        with allure.step("断言"):
            assert element is not None, "元素不存在"

    @allure.title("客服进行会话转接")
    def test_023(self, page):
        page.goto(customer_service_url)
        with allure.step("进入客服进行会话转接"):
            page.get_by_title("转接").click()
            page.get_by_text("uitest2@easemob.com").click()
            page.get_by_text("转接", exact=True).click()
        with allure.step("返回管理员端页面"):
            page.goto(manage_index_url)
            page.get_by_text("监控", exact=True).click()
            page.get_by_text("进行中会话").click()
            element = page.get_by_title("uitest2@easemob.com")
            print(element)
        with allure.step("断言"):
            assert element is not None, "元素不存在"

    @allure.title("会话结束自动发送满意度邀请")
    def test_024(self, page):
        """
        检查点：
        * 1. 客服端消息发送成功校验访客端新增消息访客服送时间戳一致
        """
        page.goto(manage_index_url)
        with allure.step("进入会话结束自动发送满意度邀请"):
            page.get_by_text("监控", exact=True).click()
            page.get_by_title("进行中会话").click()
            page.locator("#em-session").get_by_title("结束会话").first.locator("span").click()
            page.get_by_text("关闭", exact=True).click()
            element = page.locator("#em-session").get_by_text("无数据")
            print(element)
            with allure.step("断言"):
                assert element is not None, "元素不存在"
        with allure.step("返回访客端页面"):
            page.goto(visitor_url)
            element = page.get_by_text("请对我的服务做出评价")
            # page.locator("div").filter(has_text=re.compile(r"^服务评价$")).locator("i").click()
            print(element)
        with allure.step("断言"):
            assert element is not None, "元素不存在"
