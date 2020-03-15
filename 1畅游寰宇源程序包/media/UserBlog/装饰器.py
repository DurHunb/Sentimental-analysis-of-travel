from functools import wraps

'''
def hello(fn):
    print('hii')
    def wrapper():
        print("hello, %s" % fn.__name__)
        fn()
        print("goodby, %s" % fn.__name__)
    print('hi')
    return wrapper

print('we')

@hello
def foo():
    print("i am foo")

foo()
'''

'''#wraps 只能改变name、doc等
def hello(fn):
    @wraps(fn)
    def wrapper():
        print("hello, %s" % fn.__name__)
        fn()
        print("goodby, %s" % fn.__name__)
    return wrapper

@hello
def foo():
    # foo help doc
    print("i am foo")
    pass

foo()

print(foo.__name__)  # 输出 foo
print(foo.__doc__ ) # 输出 foo help doc
'''

'''#为了让 hello = makeHtmlTag(arg1, arg2)(hello) 成功，makeHtmlTag 必需返回一个decorator（这就是为什么我们在makeHtmlTag中加入了real_decorator()的原因）
def makeHtmlTag(tag, *args, **kwds):
    def real_decorator(fn):
        css_class = " class='{0}'".format(kwds["css_class"]) if "css_class" in kwds else ""

        def wrapped(*args, **kwds):
            return "<" + tag + css_class + ">" + fn(*args, **kwds) + "</" + tag + ">"

        return wrapped

    return real_decorator

@makeHtmlTag(tag="b", css_class="bold_css")
@makeHtmlTag(tag="i", css_class="italic_css")
def hello():
    return "hello world"

print(hello())

# 输出：
# <b class='bold_css'><i class='italic_css'>hello world</i></b>
'''