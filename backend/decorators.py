from functools import wraps


def register_runtime_node_decorator(func):
    @wraps(func)
    def wrapped(instance, name):
        from backend.registry import register_runtime_node
        name = register_runtime_node(instance, name)

        return func(instance, name)

    return wrapped

