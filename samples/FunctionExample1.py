print("Enter value of A")
a = int(input())
print("Enter value of B")
b = int(input())

# function with two arguments1
def add_numbers(a, b):
    sum = a + b
    print('Sum: ', sum)
    return sum

sum1 = add_numbers(a,b)
print(sum1)