from copy import deepcopy
from typing import Callable, Any
import re

def del_dict_key_recursively(
        original_dict: dict, key: str, del_inplace: bool = True
) -> dict:
    """递归地删除字典中的某个Key-Value对

    Args:
        original_dict: 原始Dict
        key: 要删除的key名
        del_inplace: 是否原地删除, 默认为True

    Returns:
        迭代删除指定key-value后的新字典
    """
    if not del_inplace:
        original_dict = deepcopy(original_dict)
    if key in original_dict.keys():
        del original_dict[key]
    for v in original_dict.values():
        if isinstance(v, dict):
            del_dict_key_recursively(v, key)
    return original_dict


def dict_add(dict_a: dict, dict_b: dict, inplace: bool = True) -> dict:
    if not inplace:
        dict_a = deepcopy(dict_a)
    for k, v_b in dict_b.items():
        if k in dict_a:
            v_a = dict_a[k]
            # !NOTE: 不执行递归”相加“
            if type(v_b) is type(v_a) and hasattr(v_a, "__add__"):
                dict_a[k] = v_a + v_b
        else:
            dict_a[k] = v_b
    return dict_a


def del_dict_key_recursively_v2(
        original_dict: dict,
        get_del_keys_func: Callable[[dict], list[Any]],
        del_inplace: bool = True,
) -> dict:
    """递归地删除字典中的某个Key-Value对

    Args:
        original_dict: 原始Dict
        get_del_keys_func: 输入一个字典, 输出要删除的字典的 key list
        del_inplace: 是否原地删除, 默认为True

    Returns:
        迭代删除指定key-value后的新字典
    """
    if isinstance(original_dict, list):
        for v in original_dict:
            del_dict_key_recursively_v2(v, get_del_keys_func=get_del_keys_func)
    elif not isinstance(original_dict, dict):
        return original_dict
    if not del_inplace:
        original_dict = deepcopy(original_dict)
    keys_need_del = []
    # 获取这一轮要删除的 keys
    keys_need_del = get_del_keys_func(original_dict)
    for key in keys_need_del:
        del original_dict[key]
    for v in original_dict.values():
        if isinstance(v, dict):
            del_dict_key_recursively_v2(v, get_del_keys_func=get_del_keys_func)
        if isinstance(v, list):
            for vv in v:
                del_dict_key_recursively_v2(vv, get_del_keys_func=get_del_keys_func)
    return original_dict



def camel_to_snake(name):
    # 在大写字母前加上下划线，然后将字符串转换为小写
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
