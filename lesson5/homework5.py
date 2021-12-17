import multiprocessing
import time

from multiprocessing import Pool, Process

def factorize_num(num):
    '''Function with multiprocessing. Take only one number and not return anything. 
    Print ctype array with numbers which input number can be divided whithout a remainder
    Example: factorize(128)'''

    res = []
    for i in range(1, num+1):
            if num % i == 0:
                res.append(i)
    result = multiprocessing.Array("i", len(res))
    for idx, i in enumerate(res):
        result[idx] = i
    print(result[:])

def factorize(*number):
    '''Function without multiprocessing. Take tuple as input and return tuple of lists. 
    Every list contains numbers which input number can be divided whithout a remainder
    Example: factorize(128, 255, 99999, 10651060)'''
    
    res = []
    for num in number:
        tmp = []
        for i in range(1, (num + 1)):
            if num % i == 0:
                tmp.append(i)
        
        res.append(tmp)
    return tuple(res)
    
    

#a, b, c, d  = factorize(128, 255, 99999, 10651060)

#assert a == [1, 2, 4, 8, 16, 32, 64, 128]
#assert b == [1, 3, 5, 15, 17, 51, 85, 255]
#assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
#assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]


#print (True if a == [1, 2, 4, 8, 16, 32, 64, 128] else False)
#print (True if b == [1, 3, 5, 15, 17, 51, 85, 255] else False)
#print (True if c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999] else False)
#print (True if d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060] else False)

if __name__ == "__main__":
    numbers = (128, 255, 99999, 10651060)
    start = time.perf_counter()

    with multiprocessing.Pool() as p:
        p.map(factorize_num, numbers)

    
    finish = time.perf_counter()
    print(f'Finished at {round(finish -start, 2)}')