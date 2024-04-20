def function(x):

    if x == 0:
        return
    
    return function(x-1)

# About 20 steps
function(5)


class MyClass():

    static_variable_1 = 1

    static_variable_2 = {
        "foo": 123,
        "bar": ["something", "something"],
        "nested": {
            "hello": 1,
            "world": {
                "again": ["happy", True]
            }
        }
    }

    def method_1(self, x: int):
        return x * 5
    
    def method_2(
        self,
        x: int,
        y: int
    ):
        while x >= 0:
            x -= 1
        return y

# About 150 steps
obj = MyClass()

for i in range(obj.method_1(2)):
    for n in range(obj.method_2(2, 2)):
        pass

# Exactly 1 step
data = {
    "foo": 123,
    "bar": ["something", "something"],
    "nested": {
        "hello": 1,
        "world": {
            "again": ["happy", True]
        }
    }
}

# About 17 steps
x = 5

while (lambda n: n)(x) >= 0:
    x -= 1
    pass

