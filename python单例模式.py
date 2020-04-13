class earth:
    __test=None
    def __new__(cls, *args, **kwargs):
        if cls.__test==None:
            cls.__test=object.__new__(cls)#通过父类的__new__(cls)创建实例
            return cls.__test
        else:
            return cls.__test#返回上一个对象的引用
a=earth()
print(id(a))
b=earth()
print(id(b))