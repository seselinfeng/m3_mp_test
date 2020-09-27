import inspect

import yaml


def get_data(name, path):
    """
    获取对应方法的数据
    :param name: function name
    :param path: yaml path
    :return: data_list
    """
    return yaml.safe_load(open(path, encoding='utf-8')).get(name)
