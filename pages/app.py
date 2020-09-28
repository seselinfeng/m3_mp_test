import minium
from appium import webdriver

from pages.basepage import BasePage
from pages.main import Main
from pages.my import My
from pages.orderdetail import OrderDetail
from pages.orderlist import OrderList
from pages.routing import Routing


class App(BasePage):
    def start(self):
        if self._mini is None:
            self._mini = minium.WXMinium()
        return self

    def stop(self):
        self._mini.app.exit()

    def restart(self):
        self._mini.reset_remote_debug()

    def main(self):
        return Main(self._mini)

    def routing(self):
        return Routing(self._mini)

    def order_list(self):
        return OrderList(self._mini)

    def my(self):
        return My(self._mini)

    def order_detail(self):
        return OrderDetail(self._mini)