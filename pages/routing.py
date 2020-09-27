from pages.basepage import BasePage


class Routing(BasePage):

    def goto_order_list(self):
        """
        跳转到订单列表页面
        :return: Page
        """
        return self._mini.app.navigate_to("/pages/order/list/list")

    def goto_main(self):
        """
        跳转到首页,tabBar页面需要switch_tab方法
        :return: Page
        """
        return self._mini.app.switch_tab("/pages/home/home")
