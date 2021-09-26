def addition(numbers):
    numbers = convert(numbers)
    answer=0
    for n in numbers:
        answer=answer+n 
    answer = str(answer)
    return answer

def convert(numbers):
    numbers = [int(i) for i in numbers.split() if i.isdigit()]
    numbers = [int(numeric_string) for numeric_string in numbers]
    return numbers

def subtraction(numbers):
    numbers = convert(numbers)
    answer = 0
    for n in numbers:
        answer = -answer + n 
    answer = str(answer)
    return answer

def multiplication(numbers):
    numbers = convert(numbers)
    answer = 1
    for n in numbers:
        answer = answer * n 
    answer = str(answer)
    return answer

def division(numbers):
    numbers = convert(numbers)
    answer = 1
    for n in numbers:
        answer = n/answer 
    answer = str(answer)
    return answer

def percentages(numbers):
    numbers = convert(numbers)
    answer = numbers[0]/numbers[1]
    answer = answer*100
    answer = str(answer)
    return answer+"percent"

def tothePower(numbers):
    numbers = convert(numbers)
    answer = 1
    for n in numbers:
        if(answer != 1):
            answer = answer**n
        else:
            answer = n
    answer = str(answer)
    return answer
