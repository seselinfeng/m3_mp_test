import datetime
import inspect
import json
import minium
import yaml
from minium import WXMinium, IdeNative

from pages.decorator import handle_black


class BasePage(minium.MiniTest):
    _params = {}  # 参数化的数据

    def __init__(self, mini: WXMinium = None):
        super(BasePage, self).__init__()
        self._mini = mini

    @handle_black
    def find(self, locator, value: str = None):
        """
        查找元素
        :param locator:
        :param value:
        :return: element
        """
        element = None
        if isinstance(locator, tuple):
            element = self._mini.app.get_current_page().get_element(*locator)
        elif isinstance(value, dict):
            element = self._mini.app.get_current_page().get_element(locator, **value)
        else:
            element = self._mini.app.get_current_page().get_element(locator, inner_text=value)
        return element

    @handle_black
    def finds(self, locator, value: str = None):
        """
        查找多个元素
        :param locator:
        :param value:
        :return: element
        """
        elements: list
        if isinstance(locator, tuple):
            elements = self._mini.app.get_current_page().get_elements(*locator)
        elif isinstance(value, dict):
            elements = self._mini.app.get_current_page().get_elements(locator, **value)
        else:
            elements = self._mini.app.get_current_page().get_elements(locator)
        return elements

    def wait_data(self, locator, value: str = None):
        """
        等待元素出现
        """
        if isinstance(locator, tuple):
            result = self._mini.app.get_current_page().wait_data_contains(*locator)
        elif isinstance(value, dict):
            result = self._mini.app.get_current_page().wait_data_contains(locator, **value)
        else:
            result = self._mini.app.get_current_page().wait_data_contains(locator, inner_text=value)
        return result

    def is_exists(self, locator, value: str = None):
        """
        判断元素是否存在
        """
        if isinstance(locator, tuple):
            result = self._mini.app.get_current_page().element_is_exists(*locator)
        elif isinstance(value, dict):
            result = self._mini.app.get_current_page().element_is_exists(locator, **value)
        else:
            result = self._mini.app.get_current_page().element_is_exists(locator, max_timeout=value)
        return result

    def call_js_method(self, func, args=None):
        """
        调用原生JS方法
        """
        return self._mini.app.get_current_page().call_method(func, args)

    def get_image(self):
        """
        断言失败截图
        """
        filename = "%s.png" % datetime.datetime.now().strftime("%H%M%S%f")
        self._mini.app.screen_shot(save_path=f"../screenshot/{filename}")
        with open(f"../screenshot/{filename}", "rb") as f:
            content = f.read()
        allure.attach(content, filename, attachment_type=allure.attachment_type.PNG)

    def step(self, path: str = None):
        """
        操作步骤以及操作步骤的数据驱动
        :param path:
        :return: element
        """
        element = None
        with open(path, encoding='utf-8') as f:
            # 获取调用函数的名称
            name = inspect.stack()[1].function
            # 反射原理获取当前函数的yaml数据驱动
            steps = yaml.safe_load(f)[name]
            # 序列化steps为字符串 Serialize ``obj`` to a JSON formatted ``str``.
            raw = json.dumps(steps)
            # 将yaml文件中特殊格式字符串转义为数据 ${name} --> name
            for key, value in self._params.items():
                raw = raw.replace('${' + key + '}', value)
            # 反序列化
            steps = json.loads(raw)
            for step in steps:
                # 定位元素
                if 'selector' in step.keys():
                    if step.get('type') == 'elements':
                        if 'index' in step.keys():
                            element = self.finds(step.get('selector'), step.get('params'))[step.get('index')]
                    else:
                        element = self.find(step.get('selector'), step.get('params'))
                # 触发事件
                if 'action' in step.keys():
                    action = step.get('action')
                    if action == 'click':
                        # 点击事件
                        element.click()
                    if action == 'input':
                        # 输入文本
                        element.input(step.get('value'))
                    if action == 'get_text':
                        # 获取文本
                        element = element.inner_text
                    if action == 'element_is_exists':
                        element = self.is_exists(step.get('locator'), step.get('params'))

                # 滚动页面
                if 'scroll' in step.keys():
                    element = self.find(step.get('selector'), step.get('params'))
                    element.scroll_to(step.get('x'), step.get('y'))
        return element

    def steps(self, path: str = None):
        """
        操作步骤以及操作步骤的数据驱动
        :param path:
        :return: elements
        """
        elements = None
        with open(path, encoding='utf-8') as f:
            # 获取调用函数的名称
            name = inspect.stack()[1].function
            # 反射原理获取当前函数的yaml数据驱动
            steps = yaml.safe_load(f)[name]
            # 序列化steps为字符串 Serialize ``obj`` to a JSON formatted ``str``.
            raw = json.dumps(steps)
            # 将yaml文件中特殊格式字符串转义为数据 ${name} --> name
            for key, value in self._params.items():
                raw = raw.replace('${' + key + '}', value)
            # 反序列化
            steps = json.loads(raw)
            for step in steps:
                # 定位元素
                if 'selector' in step.keys():
                    if step.get('type') == 'elements':
                        elements = self.finds(step.get('selector'), step.get('params'))
        return elements
