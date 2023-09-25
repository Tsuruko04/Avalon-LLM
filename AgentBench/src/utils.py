import pprint
import requests
import random
import logging
import json
import numpy as np

# from SwissArmyTransformer import mpu, get_tokenizer

def parse_result(result):
    parsed_result = '\n'
    if isinstance(result, list):
        for result_item in result:
            if isinstance(result_item, dict):
                for result_sub_item in result_item:
                    parsed_result += str(result_item[result_sub_item]) + '\n'
                parsed_result += "-"*50 + '\n'
            elif isinstance(result_item, str):
                parsed_result += result_item + '\n'
            else:
                parsed_result += str(result_item) + '\n'
    elif isinstance(result, str):
        parsed_result += result
    else:
        parsed_result += str(result)

    return parsed_result

class JsonEncoder(json.JSONEncoder):
    """Convert numpy classes to JSON serializable objects."""

    def default(self, obj):
        if isinstance(obj, (np.integer, np.floating, np.bool_)):
            return obj.item()
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(JsonEncoder, self).default(obj)


def serialize(obj, max_depth=5, compress=False):
    """
        dump into json, including only basic types, list types and dict types. If other types are included, they will be converted into string.
    """
    if max_depth <= 0:
        return "..."
    if isinstance(obj, (int, float, str, bool, type(None))):
        return obj
    elif isinstance(obj, list) or isinstance(obj, tuple):
        if not compress or len(obj) <= 5:
            return [serialize(item, max_depth-1, compress) for item in obj]
        else:
            return [serialize(item, max_depth-1, True) for item in obj[:5]] + ["...(total: %d)" % len(obj)]
    elif isinstance(obj, dict):
        if not compress or len(obj) <= 5:
            return {str(key): serialize(obj[key], max_depth-1, compress) for key in obj}
        else:
            ret = {str(key): serialize(obj[key], max_depth-1, True) for key in list(obj.keys())[:5]}
            ret["...total..."] = len(obj)
            return ret
    elif hasattr(obj, '__dict__'):
        return serialize(obj.__dict__, max_depth, True)
    else:
        ret = str(obj)
        if len(ret) > 100:
            ret = ret[:45] + "   ...   " + ret[-45:]
        return ret


def print_rank_0(*args, **kwargs):
    # if torch.distributed.get_rank() == 0:
    print(*args, **kwargs)
    

class ColorMessage:
    @staticmethod
    def red(msg):
        return "\033[91m" + msg + "\033[0m"
    @staticmethod
    def green(msg):
        return "\033[92m" + msg + "\033[0m"
    @staticmethod
    def cyan(msg):
        return "\033[96m" + msg + "\033[0m"
    @staticmethod
    def yellow(msg):
        return "\033[93m" + msg + "\033[0m"
