import allure
from time import sleep

@allure.feature('login')
class TestLogin():

    @allure.story("登陆保存会话信息")
    def test_login(self, page, base_url):

        page.goto(base_url)
        page.get_by_placeholder("邮箱").click()
        page.get_by_placeholder("邮箱").fill("uitest1@easemob.com")
        page.get_by_placeholder("密码").click()
        page.get_by_placeholder("密码").fill("uitest1@easemob.com")
        page.get_by_text("登录", exact=True).click()

        sleep(2)
        # 保存cookies
        page.context.storage_state(path="auth/login.json")
