register = {}


def register_command(text, is_private=False):
    def function(func):
        f = func
        register[text] = {
            "func": f,
            "private": is_private
        }

        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return function


if __name__ == '__main__':
    # log("asd")
    print(register['测试']['func']("ok"))
