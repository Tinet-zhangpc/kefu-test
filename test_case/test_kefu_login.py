import allure
from time import sleep


@allure.feature('初始化登录缓存token')
class TestLogin:

    @allure.title("登陆保存会话信息")
    def test_login(self, page, base_url):
        page.goto(base_url)
        with allure.step("输入邮箱账号"):
            page.get_by_placeholder("邮箱").click()
            page.get_by_placeholder("邮箱").fill("uitest1@easemob.com")
        with allure.step("输入密码"):
            page.get_by_placeholder("密码").click()
            page.get_by_placeholder("密码").fill("uitest1@easemob.com")
        with allure.step("登录"):
            page.get_by_text("登录", exact=True).click()

        sleep(2)
        # 保存cookies
        with allure.step("保存cookies"):
            page.context.storage_state(path="auth/login.json")
