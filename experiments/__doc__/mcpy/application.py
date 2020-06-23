from mymacros import macros, document  # noqa: F401


with document:
    # comentario a
    a = "5.1"
    """ docu a """
    b = False
    """ docu b """
    c = 3
    """ docu c """


class d(object):
    def __init__(self):
        with document:
            self.at1 = 4.5
            """ documenting d.at1 """


print("a = "+str(a)+"  # "+_help_a)  # noqa: F821
print("b = "+str(b)+"  # "+_help_b)  # noqa: F821
print("c = "+str(c)+"  # "+_help_c)  # noqa: F821
e = d()
print("e.at1 = "+str(e.at1)+"  # "+e._help_at1)  # noqa: F821
