class Test1():
    # Class variable
    num3 = 8
    def __init__(self,n1,n2):
        self.num1 = n1
        self.num2 = n2

    # Instance function
    def add(self):
        return self.num1 + self.num2 + self.num3
    # Instance function
    def sub(self):
        return self.num2-self.num1 + self.num3

    # Class function
    def mul (cls):
        print(cls.num3)
        print(cls.num3 * cls.num3)

    # Class function -- another way
    @classmethod
    def mul2(cls):
        print(cls.num3)
        print(cls.num3 * cls.num3)

    @staticmethod
    def fun1():
        print("calling a static method")

# End of the class
# class varibale value change
Test1.num3 = 20
testObject = Test1(1,2)
print(testObject.add())
print(testObject.sub())

# calling class function
# class name. function name(class name)
Test1.mul(Test1)

# calling class method  - another method
Test1.mul2()

# calling static method
Test1.fun1()