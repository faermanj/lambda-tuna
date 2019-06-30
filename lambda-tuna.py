#!/usr/bin/env python3

import click
import boto3
import pprint
import base64
import re

pp = pprint.PrettyPrinter(indent=4)
awslambda = boto3.client('lambda')
max_memory=3008

def log(msg):
    print("Λ🐟  {}".format(msg))


def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)


def update_mem(arn, mem):
    awslambda.update_function_configuration(
        FunctionName=arn,
        MemorySize=min(max_memory,int(mem))
    )
    log("{} tuned to {}".format(arn, mem))


def invoke(arn):
    invoke_result = None
    invoke = awslambda.invoke(
        FunctionName=arn,
        InvocationType='RequestResponse',
        LogType='Tail',
        Payload=b''
    )
    # pp.pprint(invoke)
    responseMetadata = invoke["ResponseMetadata"]
    httpHeaders = responseMetadata["HTTPHeaders"]
    logResult = httpHeaders["x-amz-log-result"]
    logResult = str(base64.b64decode(logResult))
    # pp.pprint(logResult)
    used_mem = re.search(r'Max Memory Used: (\d*) MB',
                         logResult, re.IGNORECASE)
    duration = re.search(r'Duration: (\S*) ms', logResult, re.IGNORECASE)

    if used_mem:
        used_mem = used_mem.group(1)
        used_mem = int(used_mem)

    if duration:
        duration = duration.group(1)
        duration = float(duration)

    if (used_mem and duration):
        invoke_result = (used_mem, duration)
    return invoke_result


@click.command()
@click.option('--arn', required=True, help='ARN of the function to tuna.')
@click.option('--maxi', default=10, help='Max number of invokes to attempt')
@click.option('--margin', default=0.10, help='Percentage of duration improvement threshold') #TODO Poor naming
def lambda_tuna(arn="", maxi=10, margin=0.10):
    """Tuna your lambda functions."""
    log(arn)
    max_mem = 0
    old_mem =0
    is_improving = True
    duration_best = 0
    log("Starting at minimum")
    update_mem(arn,128)
    while(is_improving):
        invokes = []
        fn_cfg = awslambda.get_function_configuration(FunctionName=arn)
        # pp.pprint(fn_cfg)
        mem = int(fn_cfg['MemorySize'])
        if (not old_mem):
            old_mem=mem
        for i in range(0, maxi):
            # pp.pprint(mem)
            invoke_result = invoke(arn)
            (used_mem, duration) = invoke_result
            if (used_mem > max_mem):
                max_mem = used_mem
            invokes.append(invoke_result)
            log("{} {}/{} MB {} ms".format(i,used_mem, mem, duration))
        log("Memory (max/cfg): {}/{} MB".format(max_mem, mem))
        durations = list(map(lambda x: x[1], invokes))
        duration_mean = int(mean(durations))        
        if (not duration_best):
            duration_best = duration_mean

        log("Duration (avg/best): {}/{} ms".format(duration_mean, duration_best))
        improvement = duration_best - duration_mean            
        improvement_perc =  float(improvement) / float(duration_best)
        is_improving = improvement == 0 or improvement_perc > margin
        can_increase = mem < max_memory
        if (not can_increase):
            log("Can't increase further than {}".format(max_memory))
        if(improvement_perc):
            log("Improved in {}({}%) >? {}%".format(improvement,int(improvement_perc*100),int(margin * 100)))
        step_up = can_increase and is_improving
        if step_up:
            #is improving                
            step = int(max_mem + (mem - max_mem)/4)
            new_mem = min(3008,mem + step)
            old_mem = mem
            log("Up memory {}+{}={} MB".format(old_mem,step,new_mem))
            duration_best = duration_mean
            update_mem(arn,new_mem)
        else:
            #not improving                            
            new_mem = old_mem
            log("No longer improving, set to {} and stop".format(new_mem))
            update_mem(arn,new_mem)

if __name__ == '__main__':
    lambda_tuna()
