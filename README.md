# lambda-tuna
λ🐟

Tune your lambda functions automagically!

Features:
* Set the memory value to the smallest possible keeping the most fast configuration (DOING)
* Meanwhile, watch aws cloudtrail and suggest an IAM policy (TODO)

## How so?

Given the function
```
def fibo(n):
    a,b,i = 1,1,1
    while i < n:
        i += 1
        a,b = b,a+b
    return a

def lambda_handler(event, context):
    x = 10000
    y = fibo(x)
    msg = "fibo({}) = {}".format(x,y)
    return msg
```

Auto tune it!

```
$ ./lambda-tuna.py --arn "arn:aws:lambda:us-east-1:975034036806:function:python-fibo-iter-PythonFiboIter-115WUIZB4O5YZ" 
Λ🐟  [python-fibo-iter-PythonFiboIter-115WUIZB4O5YZ/128] 48.18 ms / 53 MB
Λ🐟  [python-fibo-iter-PythonFiboIter-115WUIZB4O5YZ/128] 59.39 ms / 53 MB
Λ🐟  [python-fibo-iter-PythonFiboIter-115WUIZB4O5YZ/128] 46.35 ms / 53 MB
Λ🐟  [python-fibo-iter-PythonFiboIter-115WUIZB4O5YZ/128] 137.37 ms / 53 MB
Λ🐟  [python-fibo-iter-PythonFiboIter-115WUIZB4O5YZ/128] 41.94 ms / 53 MB
Λ🐟  [python-fibo-iter-PythonFiboIter-115WUIZB4O5YZ/301] 14.02 ms / 53 MB
Λ🐟  [python-fibo-iter-PythonFiboIter-115WUIZB4O5YZ/301] 17.14 ms / 53 MB
Λ🐟  [python-fibo-iter-PythonFiboIter-115WUIZB4O5YZ/301] 4.45 ms / 53 MB
Λ🐟  [python-fibo-iter-PythonFiboIter-115WUIZB4O5YZ/301] 3.85 ms / 53 MB
Λ🐟  [python-fibo-iter-PythonFiboIter-115WUIZB4O5YZ/301] 5.87 ms / 53 MB
Λ🐟  Less Mem(128 = 66.65) Current Mem(301 = 66.65) More Mem(302 = 9.07)
Λ🐟  Improvement = 302
Λ🐟  [python-fibo-iter-PythonFiboIter-115WUIZB4O5YZ/477] 3.93 ms / 53 MB
Λ🐟  [python-fibo-iter-PythonFiboIter-115WUIZB4O5YZ/477] 3.79 ms / 53 MB
Λ🐟  [python-fibo-iter-PythonFiboIter-115WUIZB4O5YZ/477] 3.93 ms / 53 MB
Λ🐟  [python-fibo-iter-PythonFiboIter-115WUIZB4O5YZ/477] 4.06 ms / 53 MB
Λ🐟  [python-fibo-iter-PythonFiboIter-115WUIZB4O5YZ/477] 3.98 ms / 53 MB
Λ🐟  Less Mem(128 = 66.65) Current Mem(477 = 9.07) More Mem(477 = 3.94)
Λ🐟  Improvement = 477
Λ🐟  [python-fibo-iter-PythonFiboIter-115WUIZB4O5YZ/852] 3.92 ms / 54 MB
Λ🐟  [python-fibo-iter-PythonFiboIter-115WUIZB4O5YZ/852] 3.92 ms / 54 MB
Λ🐟  [python-fibo-iter-PythonFiboIter-115WUIZB4O5YZ/852] 3.94 ms / 54 MB
Λ🐟  [python-fibo-iter-PythonFiboIter-115WUIZB4O5YZ/852] 4.08 ms / 54 MB
Λ🐟  [python-fibo-iter-PythonFiboIter-115WUIZB4O5YZ/852] 4.24 ms / 54 MB
Λ🐟  [python-fibo-iter-PythonFiboIter-115WUIZB4O5YZ/174] 28.32 ms / 53 MB
Λ🐟  [python-fibo-iter-PythonFiboIter-115WUIZB4O5YZ/174] 28.37 ms / 53 MB
Λ🐟  [python-fibo-iter-PythonFiboIter-115WUIZB4O5YZ/174] 49.24 ms / 53 MB
Λ🐟  [python-fibo-iter-PythonFiboIter-115WUIZB4O5YZ/174] 39.82 ms / 53 MB
Λ🐟  [python-fibo-iter-PythonFiboIter-115WUIZB4O5YZ/174] 25.53 ms / 53 MB
Λ🐟  Less Mem(174 = 34.26) Current Mem(477 = 3.94) More Mem(852 = 4.02)
Λ🐟  Improvement = None
Λ🐟  Function tuned to 477
```

Inspired by [alexcasalboni/aws-lambda-power-tuning](https://github.com/alexcasalboni/aws-lambda-power-tuning)