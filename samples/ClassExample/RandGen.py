import random

def generate_random_numbers(n):
  """Generates n random numbers between 0 and 100."""
  random_numbers = []
  for i in range(n):
    random_numbers.append(random.randint(1, 100000))
  return random_numbers

# Generate 1 lakh random numbers
random_numbers = generate_random_numbers(110000)
print(len(random_numbers))

# Print the random numbers
#for number in random_numbers:
#  print(number)

text_file = open("Output.txt", "w")
text_file.write(",".join(str(year) for year in random_numbers))
text_file.close()