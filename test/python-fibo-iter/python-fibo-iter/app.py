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