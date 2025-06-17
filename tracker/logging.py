from enum import IntEnum

class LogLevel(IntEnum):
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    NONE = 100  # suppress all logs

current_log_level = LogLevel.INFO


def set_log_level(level: LogLevel):
    global current_log_level
    current_log_level = level


def log(message: str, level: LogLevel = LogLevel.INFO):
    if level >= current_log_level:
        print(f"[{level.name}] {message}")


def log_function_call(level: LogLevel = LogLevel.DEBUG):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if level >= current_log_level:
                arg_str = ", ".join(
                    [repr(a) for a in args] + [f"{k}={v!r}" for k, v in kwargs.items()]
                )
                log(f"Calling {func.__name__}({arg_str})", level)
            result = func(*args, **kwargs)
            if level >= current_log_level:
                log(f"{func.__name__} returned {result!r}", level)
            return result

        return wrapper

    return decorator