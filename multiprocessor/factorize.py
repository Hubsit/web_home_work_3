from time import time
from multiprocessing import Pool, cpu_count


def factorize(*numbers):
    result = {}
    for number in numbers:
        result[number] = [i for i in range(1, number + 1) if not number % i]
    return result


if __name__ == '__main__':
    start = time()
    factorize(128, 255, 99999, 10651060)
    print(time() - start)

    start_cpu = time()
    with Pool(cpu_count()) as p:
        result = p.apply_async(factorize, (128, 255, 99999, 10651060))
    print(time() - start_cpu)

