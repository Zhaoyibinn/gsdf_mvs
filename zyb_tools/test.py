def my_decorator(func):
    def wrapper(*args, **kwargs):
        print('my_decorator_wrapper')
        func(*args, **kwargs)
    return wrapper

@ my_decorator # 或 @my_decorator
def print_message(text):
    print(text)


print_message("okokok")