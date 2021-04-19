from abc import ABCMeta


class SingletonMeta(ABCMeta):
    """Singleton metaclass for state classes"""
    __instance = {}

    def __call__(cls, *args, **kwargs):
        """Return singleton instance"""
        if cls not in cls.__instance:
            cls.__instance[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        # Call on_called method to debug
        return cls.__instance[cls]


class Singleton(metaclass=SingletonMeta):
    pass
