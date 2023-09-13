print('good morning vietnam')

for i in 'balls of fire':
    print(i)

print('u d man')

total = 8
f = total * 3
print(f)

# def divide_numbers(a, b):
#     try:
#         a = int(input('Enter a number'))
#         b = int(input('Enter a number '))
#
#         answer = a / b
#
#
#     except (ValueError, ZeroDivisionError):
#         answer = 'An error occured'
#
#
#     return answer
#
# print(divide_numbers(10, 2))

def divide_numbers2():
    while True:
        try:
            c = int(input('Enter a number: '))
            d = int(input('Enter a number: '))

            ans = c / d
            return ans

        except ValueError as e:
            print(f'Error was {e}. Please enter a number')

        except ZeroDivisionError as e:
            print(f'Error was {e}. Cant divide by zero. silly')



print(divide_numbers2())
