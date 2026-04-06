import re

def generator_numbers(text):
    pattern = r"\d+\.\d+"
    for match in re.findall(pattern, text):
        yield float(match)


def sum_profit(text, func):
    total = sum(func(text))
    print(f"Загальний дохід: {total}")
    return total


# запуск
text = "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів."

sum_profit(text, generator_numbers)