#Diamond Problem 

## Diamond Problem Example
# A is the base (grandparent) class
# B and C are parent classes
# D is the child class (diamond inheritance)

class A:
    def __init__(self):
        print("initializing the A")

    def foo(self):
        pass


class B(A):
    def __init__(self):
        super().__init__()          # Calls A's constructor
        print("initializing the B")

    def foo(self):
        return "Implementation of B"


class C(A):
    def __init__(self):
        super().__init__()          # Calls A's constructor (only once due to MRO)
        print("initializing the C")

    def foo(self):
        return "Implementation of C"


class D(B, C):
    def __init__(self):
        super().__init__()          # MRO: D → B → C → A
        print("initialising the D")

    def foo(self):
        b = B.foo(self)                 # Explicitly resolving ambiguity
        c = C.foo(self)
        print(f"D resolves diamond by using: ({b}) AND ({c})")


#  main
d = D()
d.foo()

 