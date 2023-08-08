# [] --> indicates an array, need declare a variable before use it
nums=[]

for i in range(3):
    print("Enter value for ",i+1)
    # Need to append input in the list
    nums.append(int(input()))

for i in nums:
    print("list values",i)

for i in range(3,6):
    # input takes string as argument to print a message
    nums.append(int( input("Enter value for "+ str(i+1)) ))

print(nums)

sum=0
for i in nums:
    sum=sum+i

print("Sum of the values",sum)

# No of items in the list
print("No of items in the list ", len(nums))

# Average of the sum
print("Average of the sum ",sum/len(nums))
