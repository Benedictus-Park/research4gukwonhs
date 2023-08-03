def decorator_test(f):
    def wrapper():
        print("a")
        f()
        print("c")

    return wrapper

@decorator_test
def fuck():
    print("b")

fuck()

# a
# b
# c