import re
from time import sleep

import allure
from common.page_url import *
from common.config import *
from common.util import get_nowtime

@allure.feature('基础其他')
@allure.testcase(manage_index_url, '测试用例链接-客服端')
@allure.testcase(visitor_url, '测试用例链接-访客端')
@allure.testcase(visitor_url, '测试用例工单链接-jira地址')
class TestOther:
    # 标识会话用户昵称
    sessionPlugin = "UiTest"
    # 标识会话用户昵称
    newSessionPlugin = "newUiTest"
    # 标识会话用户昵称
    appPlugin = "快速创建的关联"
    # 标识会话用户昵称
    newAppPlugin = "new快速创建的关联"

    @allure.title("添加在线渠道-网站")
    def test_001(self, page):
        page.goto(manage_index_url)
        page.pause()
        page.get_by_text("接入", exact=True).click()
        page.get_by_title("网站").click()
        page.get_by_text("添加网页插件").click()
        page.get_by_role("textbox").click()
        page.get_by_role("textbox").fill(self.sessionPlugin)
        page.locator("span").filter(has_text="保存").click()
        frame = page.main_frame
        element = frame.query_selector('*:has-text("UiTest")')
        print(element)
        with allure.step("断言"):
            assert element is not None, "元素不存在"

    @allure.title("编辑在线渠道-网站")
    def test_002(self, page):
        page.goto(manage_index_url)
        page.get_by_text("接入", exact=True).click()
        page.get_by_title("网站").click()
        page.get_by_text(self.sessionPlugin, exact=True).first.click()
        page.locator(".ui-cmp-iconbtn").first.click()
        page.get_by_role("textbox").click()
        page.get_by_role("textbox").press("Meta+a")
        page.get_by_role("textbox").fill(self.newSessionPlugin)
        page.locator("span").filter(has_text="保存").click()
        page.get_by_role("button", name="保存").click()
        page.reload()
        # page.pause()
        frame = page.main_frame
        element = page.query_selector('*:has-text("newUiTest")')
        print(element)
        element = frame.query_selector('*:has-text("UiTest")')
        print(element)
        with allure.step("断言"):
            assert element is not None, "元素不存在"

    @allure.title("删除在线渠道-网站")
    def test_003(self, page):
        page.goto(manage_index_url)
        page.get_by_text("接入", exact=True).click()
        page.get_by_title("网站").click()
        page.get_by_text(self.newSessionPlugin, exact=True).first.click()
        page.get_by_role("button", name="删除").click()
        page.locator("span").filter(has_text=re.compile(r"^删除$")).click()
        # page.pause()
        page.reload()
        frame = page.main_frame
        element = frame.query_selector('*:has-text("newUiTest")')
        print(element)
        with allure.step("断言"):
            assert element is None, "元素未删除"

    @allure.title("添加在线渠道-app")
    def test_004(self, page):
        page.goto(manage_index_url)
        page.get_by_text("接入", exact=True).click()
        page.get_by_title("APP").click()
        page.locator("#em-attach").get_by_role("article").get_by_text("添加APP关联", exact=True).click()
        page.get_by_text("快速创建").nth(1).click()
        page.get_by_text(self.appPlugin).first.click()
        frame = page.main_frame
        element = frame.query_selector('*:has-text("二维码")')
        print(element)
        with allure.step("断言"):
            assert element is not None, "二维码不存在"

    @allure.title("编辑在线渠道-app")
    def test_005(self, page):
        page.goto(manage_index_url)
        page.get_by_text("接入", exact=True).click()
        page.get_by_title("APP").click()
        page.get_by_text(self.appPlugin).first.click()
        page.locator(".ui-cmp-iconbtn").first.click()
        page.get_by_role("textbox").click()
        page.get_by_role("textbox").fill("new快速创建的关联")
        frame = page.main_frame
        element = frame.get_by_text('保存', exact=True).all()
        element[5].click()
        frame = page.main_frame
        element = frame.query_selector('*:has-text("new快速创建的关联")')
        print(element)
        with allure.step("断言"):
            assert element is not None, "修改失败"

    @allure.title("删除在线渠道-app")
    def test_006(self, page):
        page.goto(manage_index_url)
        page.get_by_text("接入", exact=True).click()
        page.get_by_title("APP").click()
        page.get_by_text(self.newAppPlugin).first.click()
        page.get_by_text("立即解除").click()
        page.get_by_text("删除", exact=True).click()
        page.reload()
        frame = page.main_frame
        element = frame.query_selector('*:has-text("new快速创建的关联")')
        print(element)
        with allure.step("断言"):
            assert element is None, "删除失败"

    @allure.title("添加在线渠道-第三方")
    def test_007(self, page):
        page.goto(manage_index_url)
        page.get_by_text("接入", exact=True).click()
        page.get_by_text("第三方接入").click()
        page.locator("#em-rest").get_by_role("article").get_by_text("添加REST关联").click()
        page.get_by_placeholder("name").click()
        page.get_by_placeholder("name").fill("UiTest")
        page.get_by_placeholder("回调地址").click()
        page.get_by_placeholder("回调地址").fill(index_url)
        page.get_by_text("保存").click()
        frame = page.main_frame
        element = frame.query_selector('*:has-text("UiTest")')
        print(element)
        with allure.step("断言"):
            assert element is not None, "添加失败"

    @allure.title("编辑在线渠道-第三方")
    def test_008(self, page):
        page.goto(manage_index_url)
        page.get_by_text("接入", exact=True).click()
        page.get_by_text("第三方接入").click()
        page.get_by_text("UiTest", exact=True).first.click()
        page.get_by_text("编辑修改").click()
        page.get_by_placeholder("name").click()
        page.get_by_placeholder("name").fill("newUiTest")
        page.get_by_text("保存", exact=True).click()
        page.reload()
        frame = page.main_frame
        element = frame.locator(".app-list-item").filter(has_text="newUiTest")
        print(element)
        with allure.step("断言"):
            assert element is not None, "修改失败"

    @allure.title("删除在线渠道-第三方")
    def test_009(self, page):
        page.goto(manage_index_url)
        page.get_by_text("接入", exact=True).click()
        page.get_by_text("第三方接入").click()
        page.get_by_text("newUiTest").first.click()
        page.get_by_text("立即解除").click()
        page.get_by_text("删除", exact=True).click()
        page.reload()
        frame = page.main_frame
        element = frame.query_selector('*:has-text("newUiTest")')
        print(element)
        with allure.step("断言"):
            assert element is None, "删除失败"

    @allure.title("添加工单渠道-邮箱")
    def test_010(self, page):
        page.goto(manage_index_url)
        page.get_by_text("接入", exact=True).click()
        page.get_by_text("邮箱渠道").click()
        page.get_by_text("添加邮箱渠道").click()
        page.locator("input[name=\"username\"]").click()
        page.locator("input[name=\"username\"]").fill("UiTest@qq.com")
        page.locator("input[name=\"password\"]").click()
        page.locator("input[name=\"password\"]").fill("UiTest@qq.com")
        page.locator("input[name=\"sender_host\"]").first.click()
        page.locator("input[name=\"sender_host\"]").first.fill("ui")
        page.locator("input[name=\"sender_host\"]").nth(1).click()
        page.locator("input[name=\"sender_host\"]").nth(1).fill("993")
        page.locator("input[name=\"receiver_host\"]").click()
        page.locator("input[name=\"receiver_host\"]").fill("ui")
        page.locator("input[name=\"receiver_port\"]").click()
        page.locator("input[name=\"receiver_port\"]").fill("993")
        page.get_by_text("保存").click()
        element = page.get_by_text("UiTest@qq.com")
        print(element)
        with allure.step("断言"):
            assert element is not None, "元素不存在"

    @allure.title("修改工单渠道-邮箱")
    def test_011(self, page):
        page.goto(manage_index_url)
        page.get_by_text("接入", exact=True).click()
        page.get_by_text("邮箱渠道").click()
        page.locator(".font-edit").first.click()
        page.locator("input[name=\"username\"]").click()
        page.locator("input[name=\"username\"]").press("Meta+a")
        page.locator("input[name=\"username\"]").fill("newUiTest@qq.com")
        page.get_by_text("保存").click()
        element = page.query_selector('*:has-text("newUiTest@qq.com")')
        print(element)
        with allure.step("断言"):
            assert element is not None, "元素不存在"

    @allure.title("删除工单渠道-邮箱")
    def test_012(self, page):
        page.goto(manage_index_url)
        page.get_by_text("接入", exact=True).click()
        page.get_by_text("邮箱渠道").click()
        page.locator(".font-delete").first.click()
        element = page.query_selector('*:has-text("newUiTest@qq.com")')
        print(element)
        with allure.step("断言"):
            assert element is None, "未删除成功"

    @allure.title("添加工单渠道-网页")
    def test_013(self, page):
        page.goto(manage_index_url)

        page.get_by_text("接入", exact=True).click()
        page.get_by_text("网页渠道").click()
        page.get_by_text("新增网页渠道").click()
        page.locator("input[name=\"channel_name\"]").click()
        page.locator("input[name=\"channel_name\"]").fill("UiTest")
        page.get_by_text("保存").click()
        element = page.query_selector('*:has-text("UiTest")')
        print(element)
        with allure.step("断言"):
            assert element is not None, "元素不存在"

    @allure.title("修改工单渠道-网页")
    def test_014(self, page):
        page.goto(manage_index_url)
        page.get_by_text("接入", exact=True).click()
        page.get_by_text("网页渠道").click()
        page.locator(".font-edit").click()
        page.locator("input[name=\"channel_name\"]").click()
        page.locator("input[name=\"channel_name\"]").press("Meta+a")
        page.locator("input[name=\"channel_name\"]").fill("newUiTest")
        page.get_by_text("保存", exact=True).click()
        element = page.query_selector('*:has-text("newUiTest")')
        print(element)
        with allure.step("断言"):
            assert element is not None, "元素不存在"

    @allure.title("删除工单渠道-网页")
    def test_015(self, page):
        page.goto(manage_index_url)
        page.get_by_text("接入", exact=True).click()
        page.get_by_text("网页渠道").click()
        page.locator(".font-delete").first.click()
        element = page.query_selector('*:has-text("newUiTest")')
        print(element)
        with allure.step("断言"):
            assert element is None, "未删除成功"

    @allure.title("添加公共常用语分类")
    def test_016(self, page):
        page.goto(manage_index_url)
        page.pause()
        page.get_by_text("智能", exact=True).click()
        page.get_by_text("公共常用语").click()
        page.locator(".addPrase").click()
        page.get_by_placeholder("分类名称").fill("UiTest")
        page.get_by_text("保存").click()
        element = page.query_selector('*:has-text("UiTest")')
        print(element)
        with allure.step("断言"):
            assert element is not None, "元素不存在"

    @allure.title("修改公共常用语分类")
    def test_017(self, page):
        page.goto(manage_index_url)
        page.get_by_text("智能", exact=True).click()
        page.get_by_text("公共常用语").click()
        page.get_by_title("UiTest").first.click()
        page.locator(".font-edit").click()
        page.get_by_placeholder("分类名称").click()
        page.get_by_placeholder("分类名称").press("Meta+c")
        page.get_by_placeholder("分类名称").fill("newUiTest")
        page.get_by_text("保存").click()
        element = page.query_selector('*:has-text("newUiTest")')
        print(element)
        with allure.step("断言"):
            assert element is not None, "元素不存在"

    @allure.title("添加公共常用语")
    def test_018(self, page):
        page.goto(manage_index_url)
        page.get_by_text("智能", exact=True).click()
        page.get_by_text("公共常用语").click()
        page.get_by_text("newUiTest").first.click()
        page.get_by_text("添加常用语").click()
        page.get_by_placeholder("请输入常用语内容").click()
        page.get_by_placeholder("请输入常用语内容").press("Meta+a")
        page.get_by_placeholder("请输入常用语内容").fill("UiCommonPhrase")
        page.get_by_text("保存").click()
        element = page.query_selector('*:has-text("UiCommonPhrase")')
        print(element)
        with allure.step("断言"):
            assert element is not None, "元素不存在"

    @allure.title("修改公共常用语")
    def test_019(self, page):
        page.goto(manage_index_url)
        page.get_by_text("智能", exact=True).click()
        page.get_by_text("公共常用语").click()
        page.get_by_text("newUiTest").click()
        page.get_by_text("UiCommonPhrase").first.click()
        page.locator(".right-list-item > .font-edit").first.click()
        page.locator("textarea[name=\"edit_phrase\"]").click()
        page.locator("textarea[name=\"edit_phrase\"]").fill("newUiCommonPhrase")
        page.get_by_text("保存", exact=True).click()
        element = page.query_selector('*:has-text("newUiTest")')
        print(element)
        with allure.step("断言"):
            assert element is not None, "元素不存在"

    @allure.title("删除添加公共常用语")
    def test_020(self, page):
        page.goto(manage_index_url)
        page.get_by_text("智能", exact=True).click()
        page.get_by_text("公共常用语").click()
        page.get_by_title("newUiTest").first.click()
        page.get_by_text("newUiCommonPhrase").first.click()
        page.locator(".right-list-item > .font-delete").click()
        page.get_by_text("删除", exact=True).click()
        page.reload()
        sleep(3)
        element = page.query_selector('*:has-text("newUiCommonPhrase")')
        print(element)
        with allure.step("断言"):
            assert element is None, "未删除成功"

    @allure.title("删除添加公共常用语分类")
    def test_021(self, page):
        page.goto(manage_index_url)
        page.get_by_text("智能", exact=True).click()
        page.get_by_text("公共常用语").click()
        page.get_by_title("newUiTest").first.click()
        page.locator(".font-delete").click()
        page.get_by_text("删除", exact=True).click()
        page.reload()
        element = page.query_selector('*:has-text("newUiTest")')
        print(element)
        with allure.step("断言"):
            assert element is None, "未删除成功"

    @allure.title("添加客服知识语分类")
    def test_022(self, page):
        page.goto(manage_index_url)
        page.pause()
        page.get_by_text("智能", exact=True).click()
        page.get_by_title("客服知识库").click()
        page.get_by_text("管理分类").click()
        page.get_by_text("添加分类").click()
        page.get_by_placeholder("选择分类").fill(self.sessionPlugin)
        page.get_by_text("确定", exact=True).click()
        element = page.query_selector('*:has-text("UiTest")')
        print(element)
        with allure.step("断言"):
            assert element is not None, "元素不存在"

    @allure.title("修改客服知识语分类")
    def test_023(self, page):
        page.goto(manage_index_url)
        page.get_by_text("智能", exact=True).click()
        page.get_by_title("客服知识库").click()
        page.get_by_text("管理分类").click()
        page.get_by_text("UiTest").nth(3).click()
        element = page.get_by_title("修改").nth(3)
        print(element)
        element.click()
        page.get_by_role("textbox", name="输入分类名称").fill(self.newSessionPlugin)
        page.get_by_text("确定", exact=True).click()
        element = page.query_selector('*:has-text("newUiTest")')
        print(element)
        with allure.step("断言"):
            assert element is not None, "元素不存在"

    @allure.title("添加客服知识语")
    def test_024(self, page):
        page.goto(manage_index_url)
        page.get_by_text("智能", exact=True).click()
        page.get_by_title("客服知识库").click()
        sleep(5)
        page.locator("#em-knowledgebase").get_by_text("添加知识").click()
        page.get_by_placeholder("请在这里输入标题").click()
        page.get_by_placeholder("请在这里输入标题").fill("UiTestTitle")
        page.get_by_placeholder("请在这里输入作者").click()
        page.get_by_placeholder("请在这里输入作者").fill("Ui")
        page.get_by_placeholder("选择分类").click()
        page.get_by_title("newUiTest").click()
        page.locator(".em-category-selector > div:nth-child(3) > span").first.click()
        page.frame_locator("iframe[title=\"所见即所得编辑器\\, knEditor\"]").locator("html").click()
        page.frame_locator("iframe[title=\"所见即所得编辑器\\, knEditor\"]").locator("body").fill("UiTestContent")
        page.locator(".em-knowledge-create > .ui-cmp-btn").click()
        element = page.query_selector('*:has-text("UiTestTitle")')
        print(element)
        with allure.step("断言"):
            assert element is not None, "元素不存在"

    @allure.title("修改客服知识语")
    def test_025(self, page):
        page.goto(manage_index_url)
        page.get_by_text("智能", exact=True).click()
        page.get_by_title("客服知识库").click()
        page.get_by_text("UiTestTitle").click()
        page.locator("#em-knowledgebase").get_by_title("修改").first.click()
        page.get_by_placeholder("请在这里输入标题").click()
        page.get_by_placeholder("请在这里输入标题").fill("newUiTestTitle")
        page.locator(".em-knowledge-create > .ui-cmp-btn").click()
        element = page.query_selector('*:has-text("newUiTestTitle")')
        print(element)
        with allure.step("断言"):
            assert element is not None, "元素不存在"

    @allure.title("删除公共常用语分类")
    def test_026(self, page):
        page.goto(manage_index_url)
        page.get_by_text("智能", exact=True).click()
        page.get_by_title("客服知识库").click()
        page.get_by_text("newUiTestTitle").click()
        page.locator("#em-knowledgebase").get_by_title("删除").first.click()
        page.locator("div:nth-child(40) > div > div:nth-child(3) > span").first.click()
        element = page.query_selector('*:has-text("newUiTestTitle")')
        print(element)
        with allure.step("断言"):
            assert element is None, "未删除"

    @allure.title("删除公共常用语分类")
    def test_027(self, page):
        page.goto(manage_index_url)
        page.get_by_text("智能", exact=True).click()
        page.get_by_title("客服知识库").click()
        page.get_by_text("管理分类").click()
        page.get_by_text("UiTest").nth(3).click()
        page.get_by_title("删除").nth(3).click()
        page.locator("div:nth-child(41) > div > div:nth-child(3) > span").first.click()
        element = page.query_selector('*:has-text("newUiTest")')
        print(element)
        with allure.step("断言"):
            assert element is None, "未删除"

    @allure.title("添加客服")
    def test_028(self, page):
        page.goto(manage_index_url)
        page.get_by_text("成员", exact=True).click()
        page.get_by_role("complementary").get_by_text("客服", exact=True).click()
        page.get_by_text("添加客服").click()
        page.locator("input[name=\"nicename\"]").click()
        page.locator("input[name=\"nicename\"]").fill("UiTest")
        page.locator("input[name=\"trueName\"]").click()
        page.locator("input[name=\"trueName\"]").fill("UiTest")
        page.locator("input[name=\"username\"]").nth(2).click()
        page.locator("input[name=\"username\"]").nth(2).fill("UiTest@qq.com")
        page.locator("input[name=\"password\"]").nth(2).click()
        page.locator("input[name=\"password\"]").nth(2).fill("UiTest@qq.com")
        page.locator("input[name=\"confirmPassword\"]").nth(2).click()
        page.locator("input[name=\"confirmPassword\"]").nth(2).fill("UiTest@qq.com")
        page.get_by_text("保存", exact=True).click()
        element = page.query_selector('*:has-text("UiTest")')
        print(element)
        with allure.step("断言"):
            assert element is not None, "元素不存在"

    @allure.title("修改客服")
    def test_029(self, page):
        page.goto(manage_index_url)
        page.get_by_text("成员", exact=True).click()
        page.get_by_role("complementary").get_by_text("客服", exact=True).click()
        page.locator(".font-edit").last.click()
        page.locator("input[name=\"trueName\"]").click()
        page.locator("input[name=\"trueName\"]").fill("newUiTest")
        page.get_by_text("保存", exact=True).click()
        element = page.query_selector('*:has-text("newUiTest")')
        print(element)
        with allure.step("断言"):
            assert element is not None, "元素不存在"

    @allure.title("添加在线技能组")
    def test_030(self, page):
        page.goto(manage_index_url)
        page.get_by_role("complementary").get_by_text("成员", exact=True).click()
        page.get_by_title("在线技能组").click()
        page.locator("#em-group").get_by_text("添加技能组").click()
        page.get_by_role("textbox", name="请输入技能组名称").click()
        page.get_by_role("textbox", name="请输入技能组名称").fill("UiTestGroup")
        page.get_by_text("保存").nth(1).click()
        element = page.query_selector('*:has-text("UiTestGroup")')
        print(element)
        with allure.step("断言"):
            assert element is not None, "元素不存在"

    @allure.title("在线技能组添加成员")
    def test_031(self, page):
        page.goto(manage_index_url)
        page.get_by_role("complementary").get_by_text("成员", exact=True).click()
        page.get_by_title("在线技能组").click()
        page.get_by_text("UiTestGroup").click()
        page.locator("#em-group").get_by_text("成员管理").click()
        page.get_by_placeholder("搜索成员").first.click()
        page.get_by_placeholder("搜索成员").first.fill("newUiTest")
        page.get_by_role("listitem").filter(has_text="newUiTest").locator("span").click()
        page.get_by_text("添加到组").click()
        page.get_by_text("保存").nth(1).click()
        page.get_by_text("UiTestGroup").click()
        element = page.query_selector('*:has-text("newUiTest")')
        print(element)
        with allure.step("断言"):
            assert element is not None, "元素不存在"

    @allure.title("修改在线技能组")
    def test_032(self, page):
        page.goto(manage_index_url)
        page.get_by_role("complementary").get_by_text("成员", exact=True).click()
        page.get_by_title("在线技能组").click()
        page.get_by_text("UiTestGroup").click()
        page.locator("#em-group").get_by_text("基础设置").click()
        page.get_by_placeholder("请输入技能组名称").click()
        page.get_by_placeholder("请输入技能组名称").fill("newUiTestGroup")
        page.get_by_text("保存", exact=True).click()
        element = page.get_by_text("newUiTestGroup")
        print(element)
        element = page.query_selector('*:has-text("newUiTestGroup")')
        print(element)
        with allure.step("断言"):
            assert element is not None, "元素不存在"

    @allure.title("删除在线技能组")
    def test_033(self, page):
        page.goto(manage_index_url)
        page.get_by_role("complementary").get_by_text("成员", exact=True).click()
        page.get_by_title("在线技能组").click()
        page.get_by_text("newUiTestGroup").first.click()
        page.locator("#em-group").get_by_text("基础设置").click()
        page.get_by_text("删除技能组").click()
        page.get_by_text("删除", exact=True).click()
        page.reload()
        element = page.query_selector('*:has-text("newUiTestGroup")')
        print(element)
        with allure.step("断言"):
            assert element is None, "在线技能组未删除"

    @allure.title("删除客服")
    def test_034(self, page):
        page.goto(manage_index_url)
        page.get_by_text("成员", exact=True).click()
        page.get_by_title("客服", exact=True).click()
        page.locator(".font-delete").last.click()
        page.get_by_text("删除", exact=True).click()
        element = page.query_selector('*:has-text("newUiTest")')
        print(element)
        with allure.step("断言"):
            assert element is None, "客服未删除"

    @allure.title("添加角色")
    def test_035(self, page):
        page.goto(manage_index_url)
        page.get_by_role("complementary").get_by_text("成员", exact=True).click()
        page.get_by_title("角色管理").click()
        page.get_by_text("添加角色").click()
        page.get_by_role("textbox", name="角色名称").click()
        page.get_by_role("textbox", name="角色名称").fill("UiTest")
        page.locator(".em-permission-select > span").first.click()
        page.locator("body").press("ArrowDown")
        page.locator("body").press("ArrowDown")
        page.locator(".permission-menu-box > dl:nth-child(2) > dt > span").first.click()
        page.locator("#em-permissionSetting").get_by_text("保存").click()
        element = page.query_selector('*:has-text("UiTest")')
        print(element)
        with allure.step("断言"):
            assert element is not None, "元素不存在"

    @allure.title("修改角色")
    def test_036(self, page):
        page.goto(manage_index_url)
        page.get_by_role("complementary").get_by_text("成员", exact=True).click()
        page.get_by_title("角色管理").click()
        page.get_by_text("UiTest", exact=True).click()
        page.get_by_role("textbox", name="角色名称").click()
        page.get_by_role("textbox", name="角色名称").fill("newUiTest")
        page.locator("#em-permissionSetting").get_by_text("保存").click()
        element = page.query_selector('*:has-text("newUiTest")')
        print(element)
        with allure.step("断言"):
            assert element is not None, "元素不存在"

    @allure.title("删除角色")
    def test_037(self, page):
        page.goto(manage_index_url)
        page.get_by_text("成员", exact=True).click()
        page.get_by_text("角色管理").click()
        page.locator(".font-delete").last.click()
        page.get_by_text("删除", exact=True).click()
        element = page.query_selector('*:has-text("newUiTest")')
        print(element)
        with allure.step("断言"):
            assert element is None, "角色未删除"

    @allure.title("添加客户标签")
    def test_038(self, page):
        page.goto(manage_index_url)
        page.get_by_text("设置", exact=True).click()
        page.get_by_text("客户标签").click()
        page.get_by_text("添加标签").click()
        page.get_by_placeholder("输入标签名称").fill("UiTest")
        page.get_by_placeholder("输入标签名称").click()
        page.get_by_text("保存").click()
        element = page.query_selector('*:has-text("UiTest")')
        print(element)
        with allure.step("断言"):
            assert element is not None, "元素不存在"

    @allure.title("修改客户标签")
    def test_039(self, page):
        page.goto(manage_index_url)
        page.get_by_text("设置", exact=True).click()
        page.get_by_text("客户标签").click()
        page.get_by_text("UiTest", exact=True).click()
        page.locator("#em-tag span").filter(has_text="UiTest").locator("span").nth(1).click()
        page.get_by_role("textbox").fill("newUiTest")
        page.get_by_role("article").click()
        element = page.query_selector('*:has-text("newUiTest")')
        print(element)
        with allure.step("断言"):
            assert element is not None, "元素不存在"

    @allure.title("删除客户标签")
    def test_040(self, page):
        page.goto(manage_index_url)
        page.get_by_text("设置", exact=True).click()
        page.get_by_text("客户标签").click()
        page.locator("#em-tag").get_by_text("newUiTest").click()
        page.locator("#em-tag span").filter(has_text="newUiTest").locator("span").nth(3).click()
        page.get_by_text("删除", exact=True).click()
        page.reload()
        element = page.query_selector('*:has-text("newUiTest")')
        print(element)
        with allure.step("断言"):
            assert element is None, "角色未删除"

    @allure.title("添加业务标签")
    def test_041(self, page):
        page.goto(manage_index_url)
        page.get_by_text("设置", exact=True).click()
        page.get_by_text("业务标签").click()
        page.get_by_text("添加标签").click()
        page.get_by_placeholder("输入标签名称").fill("UiTest")
        page.get_by_placeholder("输入标签名称").press("Enter")
        element = page.query_selector('*:has-text("UiTest")')
        print(element)
        with allure.step("断言"):
            assert element is not None, "元素不存在"

    @allure.title("修改业务标签")
    def test_042(self, page):
        page.goto(manage_index_url)
        page.get_by_text("设置", exact=True).click()
        page.get_by_title("业务标签").click()
        page.get_by_title("UiTest").click()
        page.get_by_role("listitem").filter(has_text="UiTest").locator("span").nth(1).click()
        page.get_by_placeholder("会话标签 ").fill("newUiTest")
        page.get_by_placeholder("会话标签 ").press("Enter")
        page.get_by_text("保存", exact=True).click()
        element = page.query_selector('*:has-text("newUiTest")')
        print(element)
        with allure.step("断言"):
            assert element is not None, "元素不存在"

    @allure.title("删除业务标签")
    def test_043(self, page):
        page.goto(manage_index_url)
        page.get_by_text("设置", exact=True).click()
        page.get_by_title("业务标签").click()
        page.get_by_title("newUiTest").click()
        page.get_by_role("listitem").filter(has_text="newUiTest").locator("span").nth(2).click()
        page.get_by_text("删除", exact=True).click()
        page.reload()
        element = page.query_selector('*:has-text("newUiTest")')
        print(element)
        with allure.step("断言"):
            assert element is None, "角色未删除"

    @allure.title("添加时间计划")
    def test_044(self, page):
        page.goto(manage_index_url)
        page.get_by_text("设置", exact=True).click()
        page.get_by_text("工作时间").click()
        page.get_by_text("新建时间计划").click()
        page.get_by_placeholder("名称", exact=True).click()
        page.get_by_placeholder("名称", exact=True).fill("UiTest")
        page.get_by_text("保存").nth(3).click()
        element = page.query_selector('*:has-text("UiTest")')

        with allure.step("断言"):
            assert element is not None, "元素不存在"

    @allure.title("修改时间计划")
    def test_045(self, page):
        page.goto(manage_index_url)
        page.get_by_text("设置", exact=True).click()
        page.get_by_text("工作时间").click()
        page.get_by_text("UiTest", exact=True).click()
        page.locator("div:nth-child(5) > .control > .font-edit").click()
        page.get_by_placeholder("名称", exact=True).click()
        page.get_by_placeholder("名称", exact=True).fill("newUiTest")
        page.get_by_text("保存").nth(3).click()
        element = page.query_selector('*:has-text("newUiTest")')
        print(element)
        with allure.step("断言"):
            assert element is not None, "元素不存在"

    @allure.title("删除时间计划")
    def test_046(self, page):
        page.goto(manage_index_url)
        page.get_by_text("设置", exact=True).click()
        page.get_by_title("工作时间").click()
        page.get_by_text("newUiTest", exact=True).click()
        page.locator(".font-delete").click()
        page.get_by_text("删除", exact=True).click()
        page.reload()
        element = page.query_selector('*:has-text("newUiTest")')
        print(element)
        with allure.step("断言"):
            assert element is None, "删除失败"

    @allure.title("会话分配添加关联制定")
    def test_047(self, page):
        page.goto(manage_index_url)
        page.get_by_text("设置", exact=True).click()
        page.get_by_title("会话分配", exact=True).click()
        page.get_by_title("添加关联").click()
        page.get_by_role("listitem").filter(has_text="体验关联").click()
        page.locator("span").filter(has_text=re.compile(r"^添加$")).click()
        element = page.query_selector('*:has-text("体验关联")')
        print(element)
        with allure.step("断言"):
            assert element is not None, "元素不存在"

    @allure.title("会话分配修改关联制定")
    def test_048(self, page):
        page.goto(manage_index_url)
        page.get_by_text("设置", exact=True).click()
        page.get_by_title("会话分配", exact=True).click()
        page.locator("#em-routingStrategy").get_by_text("不指定").nth(1).click()
        page.get_by_role("listitem", name="未分组").click()
        element = page.query_selector('*:has-text("未分组")')
        print(element)
        with allure.step("断言"):
            assert element is not None, "元素不存在"

    @allure.title("会话分配删除关联制定")
    def test_049(self, page):
        page.goto(manage_index_url)
        page.get_by_text("设置", exact=True).click()
        page.get_by_title("会话分配", exact=True).click()
        page.locator(".relevance-list > li > .right > .font-delete").click()
        page.get_by_text("删除", exact=True).click()
        page.reload()
        element = page.query_selector('*:has-text("体验关联")')
        print(element)
        with allure.step("断言"):
            assert element is None, "删除失败"

    @allure.title("添加自定义表情")
    def test_050(self, page):
        page.goto(manage_index_url)
        page.get_by_text("设置", exact=True).click()
        page.get_by_title("自定义表情").click()
        page.locator("span").filter(has_text="上传表情").locator("span").click()
        page.get_by_label("点击选择本地文件").set_input_files(data_path + "/UiTest.zip")
        page.get_by_text("保存").click()
        page.get_by_text("保存").click()
        element = page.query_selector('*:has-text("UiTest")')
        print(element)
        with allure.step("断言"):
            assert element is not None, "元素不存在"

    @allure.title("修改自定义表情")
    def test_051(self, page):
        page.goto(manage_index_url)
        page.get_by_text("设置", exact=True).click()
        page.get_by_title("自定义表情").click()
        page.locator("li:nth-child(2) > .t3 > span > .font-edit").click()
        page.get_by_placeholder("请输入自定义表情名称").click()
        page.get_by_placeholder("请输入自定义表情名称").fill("newUiTest")
        page.get_by_text("保存", exact=True).click()
        element = page.query_selector('*:has-text("newUiTest")')
        print(element)
        with allure.step("断言"):
            assert element is not None, "元素不存在"

    @allure.title("删除自定义表情")
    def test_052(self, page):
        page.goto(manage_index_url)
        page.get_by_text("设置", exact=True).click()
        page.get_by_title("自定义表情").click()
        page.locator("li:nth-child(2) > .t3 > span:nth-child(2) > .font-delete").click()
        page.get_by_text("确定", exact=True).click()
        page.reload()
        element = page.query_selector('*:has-text("newUiTest")')
        print(element)
        with allure.step("断言"):
            assert element is None, "删除失败"

    @allure.title("添加iframe窗口")
    def test_053(self, page):
        page.goto(manage_index_url)
        page.get_by_text("设置", exact=True).click()
        page.locator(".iScrollIndicator").click()
        page.get_by_text("iframe窗口").click()
        page.get_by_role("button", name="+ 添加新窗口").click()
        page.get_by_label("窗口名称").click()
        page.get_by_label("窗口名称").fill("UiTest")
        page.get_by_label("URL").click()
        page.get_by_label("URL").fill("https://www.easemob.com")
        page.get_by_role("button", name="保 存").click()
        element = page.query_selector('*:has-text("UiTest")')
        print(element)
        with allure.step("断言"):
            assert element is not None, "元素不存在"

    @allure.title("修改iframe窗口")
    def test_054(self, page):
        page.goto(manage_index_url)
        page.get_by_text("设置", exact=True).click()
        page.locator(".iScrollIndicator").first.click()
        page.get_by_title("iframe窗口").click()
        page.get_by_role("row", name="UiTest https://www.easemob.com 编辑 删除").get_by_text("编辑").click()
        page.get_by_label("窗口名称").click()
        page.get_by_label("窗口名称").fill("newUiTest")
        page.get_by_role("button", name="保 存").click()
        element = page.query_selector('*:has-text("newUiTest")')
        print(element)
        with allure.step("断言"):
            assert element is not None, "元素不存在"

    @allure.title("删除iframe窗口")
    def test_055(self, page):
        page.goto(manage_index_url)
        page.get_by_text("设置", exact=True).click()
        page.locator(".iScrollIndicator").click()
        page.get_by_title("iframe窗口").click()
        page.get_by_role("row", name="newUiTest https://www.easemob.com 编辑 删除").get_by_text("删除").click()
        page.get_by_role("button", name="确 认").click()
        page.reload()
        element = page.query_selector('*:has-text("newUiTest")')
        print(element)
        with allure.step("断言"):
            assert element is None, "删除失败"

    @allure.title("添加自定义事件推送")
    def test_056(self, page):
        page.goto(manage_index_url)
        page.get_by_text("设置", exact=True).click()
        page.locator(".iScrollIndicator").click()
        page.get_by_text("客服事件推送").click()
        page.get_by_text("创建事件推送").click()
        page.get_by_placeholder("请填写").click()
        page.get_by_placeholder("请填写").fill("UiTest")
        page.get_by_placeholder("接收事件的服务器地址").fill("https://www.easemob.com")
        page.get_by_text("创建坐席").click()
        page.get_by_text("保存").click()
        element = page.query_selector('*:has-text("UiTest")')
        print(element)
        with allure.step("断言"):
            assert element is not None, "元素不存在"

    @allure.title("修改自定义事件推送")
    def test_057(self, page):
        page.goto(manage_index_url)
        page.get_by_text("设置", exact=True).click()
        page.locator(".iScrollIndicator").click()
        page.get_by_text("客服事件推送").click()
        page.get_by_text("自定义事件", exact=True).click()
        page.get_by_text("UiTest", exact=True).click()
        page.locator(".font-edit").click()
        page.get_by_placeholder("请填写").click()
        page.get_by_placeholder("请填写").fill("newUiTest")
        page.get_by_text("保存").click()
        element = page.query_selector('*:has-text("newUiTest")')
        print(element)
        with allure.step("断言"):
            assert element is not None, "元素不存在"

    @allure.title("删除自定义事件推送")
    def test_058(self, page):
        page.goto(manage_index_url)
        page.get_by_text("设置", exact=True).click()
        page.locator(".iScrollIndicator").click()
        page.get_by_text("客服事件推送").click()
        page.get_by_text("自定义事件", exact=True).click()
        page.get_by_text("newUiTest").click()
        page.locator(".font-delete").first.click()
        page.get_by_text("删除", exact=True).click()
        page.reload()
        element = page.query_selector('*:has-text("newUiTest")')
        print(element)
        with allure.step("断言"):
            assert element is None, "删除失败"

    @allure.title("修改企业基本信息")
    def test_059(self, page):
        page.goto(manage_index_url)
        page.get_by_text("账户", exact=True).click()
        page.get_by_placeholder("企业名称").click()
        corpName = "UiTest" + str(get_nowtime())
        print(corpName)
        page.get_by_placeholder("企业名称").fill(corpName)
        page.locator("#em-company").get_by_text("保存").click()
        page.reload()
        element = page.get_by_text(corpName)
        print(element)
        with allure.step("断言"):
            assert element is not None, "元素不存在"
