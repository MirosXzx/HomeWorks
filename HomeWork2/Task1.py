def caching_fibonacci():
    cache = {}

    def fibonacci(n):
        if n <= 0:
            return 0
        if n == 1:
            return 1

        if n in cache:
            return cache[n]

        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]

    return fibonacci


# запуск
fib = caching_fibonacci()

print(f"fib(10) = {fib(10)}")
print(f"fib(15) = {fib(15)}")