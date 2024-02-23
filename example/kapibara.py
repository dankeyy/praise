def f():
    try:
        1 / 0
    except:
        def g():
            class A:
                raise Exception("get rekt") from None
        g()

if __name__ == '__main__':
    f()
