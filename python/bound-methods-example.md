# Пример: bound methods, classmethod и staticmethod своими руками

[← Декораторы](decorators.md) · [🏠 Домой](../README.md) · [Итератор →](iterators.md)

---

Разобранный пример того, как `classmethod`/`staticmethod` и bound-методы
устроены внутри CPython — через протокол дескрипторов (`__get__`). Дополняет
раздел [Декораторы](decorators.md).

```python
class MethodType:
    "Emulate PyMethod_Type in Objects/classobject.c"

    def __init__(self, func, obj):
        print(f'MethodType __init__ ({func=}, {obj=})', end='\n\n')
        self.__func__ = func
        self.__self__ = obj

    def __call__(self, *args, **kwargs):
        print(f'MethodType __call__ ({args=}, {kwargs=})', end='\n\n')
        func = self.__func__
        obj = self.__self__
        return func(obj, *args, **kwargs)


class ClassMethod:
    "Emulate PyClassMethod_Type() in Objects/funcobject.c"

    def __init__(self, f):
        print(f'ClassMethod __init__ ({f=})', end='\n\n')
        self.f = f

    def __get__(self, obj, cls=None):
        print(f'ClassMethod __get__ ({obj=}, {cls=})', end='\n\n')
        if cls is None:
            cls = type(obj)
        return MethodType(self.f, cls)

class StaticMethod:
    "Emulate PyStaticMethod_Type() in Objects/funcobject.c"

    def __init__(self, f):
        print(f'StaticMethod __init__ ({f=})', end='\n\n')
        self.f = f
    
    def __get__(self, obj, cls=None):
        print(f'StaticMethod __get__ ({obj=}, {cls=})', end='\n\n')

        return self.f


class A:
    @ClassMethod
    def foo(cls, a, b=10):
        print(f'A foo ({cls=}, {a=}, {b=})', end='\n\n')

print('runtime', end='\n\n')

a = A()

a.foo(10)
```

---

[← Декораторы](decorators.md) · [🏠 Домой](../README.md) · [Итератор →](iterators.md)
