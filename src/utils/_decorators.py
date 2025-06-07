from src.localization import get_localizator


class t_property:
    def __init__(
        self,
        route: str,
        fget=None,
        fset=None,
        fdel=None
    ) -> None:
        self.localize = get_localizator(route)
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.name = None

    def __call__(self, fget) -> 't_property':
        self.fget = fget
        return self

    def setter(self, fset):
        self.fset = fset
        return self
    
    def deleter(self, fdel):
        self.fdel = fdel
        return self

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self

        if self.fget is None:
            raise AttributeError()

        value = self.fget(obj) if self.fget else None
        translated_name = self.localize(self.fget.__name__)

        return type('', (), {
            'value': value,
            'translated': translated_name
        })

    def __set__(self, obj, value):
        if not self.fset:
            raise AttributeError()
        self.fset(obj, value)

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError()
        self.fdel(obj)
