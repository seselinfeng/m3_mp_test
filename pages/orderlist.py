from pages.basepage import BasePage


class OrderList(BasePage):
    """订单列表页"""

    def scroll_to_footer(self):
        """
        滚动到页面底部
        :return:
        """
        self.step('../data/order_list.yaml')

    def get_order_list(self):
        """
        获取当前页面订单元素列表
        :return:
        """
        return self.steps('../data/order_list.yaml')
