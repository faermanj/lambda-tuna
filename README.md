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
$ ./lambda-tuna.py --arn "FUNCTION_ARN" --maxi 5
Λ🐟  FUNCTION_ARN
Λ🐟  Starting at minimum
Λ🐟  FUNCTION_ARN tuned to 128
Λ🐟  0 53/128 MB 25.15 ms
Λ🐟  1 53/128 MB 58.67 ms
Λ🐟  2 53/128 MB 47.37 ms
Λ🐟  3 53/128 MB 42.19 ms
Λ🐟  4 53/128 MB 56.8 ms
Λ🐟  Memory (max/cfg): 53/128 MB
Λ🐟  Duration (avg/best): 46/46 ms
Λ🐟  Up memory 128+71=199 MB
Λ🐟  FUNCTION_ARN tuned to 199
Λ🐟  0 53/199 MB 25.23 ms
Λ🐟  1 53/199 MB 17.74 ms
Λ🐟  2 53/199 MB 22.88 ms
Λ🐟  3 53/199 MB 28.58 ms
Λ🐟  4 53/199 MB 27.36 ms
Λ🐟  Memory (max/cfg): 53/199 MB
Λ🐟  Duration (avg/best): 24/46 ms
Λ🐟  Improved in 22(47%) >? 10%
Λ🐟  Up memory 199+89=288 MB
Λ🐟  FUNCTION_ARN tuned to 288
Λ🐟  0 53/288 MB 8.42 ms
Λ🐟  1 53/288 MB 20.74 ms
Λ🐟  2 53/288 MB 4.15 ms
Λ🐟  3 53/288 MB 3.77 ms
Λ🐟  4 53/288 MB 15.24 ms
Λ🐟  Memory (max/cfg): 53/288 MB
Λ🐟  Duration (avg/best): 10/24 ms
Λ🐟  Improved in 14(58%) >? 10%
Λ🐟  Up memory 288+111=399 MB
Λ🐟  FUNCTION_ARN tuned to 399
Λ🐟  0 53/399 MB 3.72 ms
Λ🐟  1 53/399 MB 9.26 ms
Λ🐟  2 53/399 MB 16.23 ms
Λ🐟  3 53/399 MB 16.88 ms
Λ🐟  4 53/399 MB 3.62 ms
Λ🐟  Memory (max/cfg): 53/399 MB
Λ🐟  Duration (avg/best): 9/10 ms
Λ🐟  Improved in 1(10%) >? 10%
Λ🐟  No longer improving, set to 288 and stop
Λ🐟  FUNCTION_ARN tuned to 288
```

Inspired by [alexcasalboni/aws-lambda-power-tuning](https://github.com/alexcasalboni/aws-lambda-power-tuning)