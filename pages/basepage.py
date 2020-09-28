import inspect
import json
import minium
import yaml
from minium import WXMinium


class BasePage(minium.MiniTest):
    _params = {}  # 参数化的数据

    def __init__(self, mini: WXMinium = None):
        super(BasePage, self).__init__()
        self._mini = mini

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
            print(steps)
            for step in steps:
                # 定位元素
                if 'selector' in step.keys():
                    if step.get('type') == 'elements':
                        if 'index' in step.keys():
                            element = self.finds(step.get('selector'), step.get('params'))[step.get('index')]
                    else:
                        element = self.find(step.get('selector'), step.get('params'))
                print(element)
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
                        element = element.text
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
