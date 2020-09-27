import minium
from appium import webdriver

from pages.basepage import BasePage
from pages.main import Main
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
        pass

    def main(self):
        return Main(self._mini)

    def routing(self):
        return Routing(self._mini)

    def order_list(self):
        return OrderList(self._mini)
