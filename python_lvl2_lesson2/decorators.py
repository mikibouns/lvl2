import json

def method_convert_data(encoding_type):
    ''''''
    def decorator(func):
        def wrapper(self, data=False):
            if data:
                if isinstance(data, bytes):
                    data = data.decode(encoding_type)
                    data = json.loads(data)
                result_value = func(self, data)
            else:
                result_value = func(self)

            if isinstance(result_value, list) or isinstance(result_value, dict):
                result_value = json.dumps(result_value)
            return result_value.encode(encoding_type)
        return wrapper
    return decorator