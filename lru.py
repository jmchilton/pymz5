from functools32 import lru_cache

#@lru_cache(maxsize=24)
def moo(a, x):
    return a.callx(x)


class A:

    @lru_cache(maxsize=24)
    def callx(self, x):
        return x + 8

a1 = A()
moo(a1, 1)
moo(a1, 1)
moo(a1, 1)

a2 = A()
moo(a2, 1)
moo(a2, 1)
moo(a2, 1)

def pc():
    print "%s ; %s" % (a1.callx.cache_info(), a2.callx.cache_info())

pc()

moo(a2, 2)
pc()

moo(a2, 2)
pc()

moo(a1, 2)
pc()

moo(a1, 1)
pc()
