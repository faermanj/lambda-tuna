#!/usr/bin/env python3

import click
import boto3
import pprint
import base64
import re
import json
import statistics
import random

pp = pprint.PrettyPrinter(indent=4)
awslambda = boto3.client('lambda')
max_memory=3008

def log(msg):
    print("Λ🐟  {}".format(msg))

class Invokation:
    def __init__(self,lambda_invoke):
        responseMetadata = lambda_invoke["ResponseMetadata"]
        httpHeaders = responseMetadata["HTTPHeaders"]
        logResult = httpHeaders["x-amz-log-result"]
        logResult = str(base64.b64decode(logResult))
                
        used_mem = re.search(r'Max Memory Used: (\d*) MB',logResult, re.IGNORECASE)
        if used_mem:
            used_mem = used_mem.group(1)
            used_mem = int(used_mem)
        self.used_mem = used_mem
        
        duration = re.search(r'Duration: (\S*) ms', logResult, re.IGNORECASE)
        if duration:
            duration = duration.group(1)
            duration = float(duration)
        self.duration = duration
        
    def __str__(self):
        return "{} ms / {} MB".format(self.duration,self.used_mem)

    def __repr__(self):
        return self.__str__()

class Funktion:
    margin = 1.1
    trials = {}

    def __init__(self,arn):
        self.arn = arn
        self.result = None
        self.invokes_per_trial = 5
        self.num_invokes = 0
        self.load_cfg()

    def load_cfg(self):
        fn_cfg = awslambda.get_function_configuration(FunctionName=self.arn)
        self.mem = int(fn_cfg['MemorySize'])
        self.name = str(fn_cfg['FunctionName'])

    def update_mem(self, mem):
        mem_size = int(mem)
        if (mem_size >= 128) and (mem_size < 3008):
            awslambda.update_function_configuration(
                FunctionName=self.arn,
                MemorySize=mem_size)
            self.load_cfg()
            #log("{} updated to {}".format(self.arn, self.mem))
        else:
            log("Invalid memory size {}".format(mem))
    
    def log(self,msg):
        log("[{}/{}] {}".format(self.name,self.mem,msg))

    def invoke(self):
        #TODO Consider multi-threaded invokes / counter consistency
        result = Invokation(awslambda.invoke(
            FunctionName=self.arn,
            InvocationType='RequestResponse',
            LogType='Tail',
            Payload=b''))
        self.num_invokes += 0
        self.log(str(result))
        return result
    
    def trial(self, new_mem):
        result = self.trials.get(new_mem)
        if(result):
            return result
        else:
            old_mem = self.mem
            if(new_mem != old_mem):
                self.update_mem(new_mem)
            #TODO Consider other strategies ( non fixed profiles, profile until stable)
            trials = range(self.invokes_per_trial)
            durations = list(map (lambda t: self.invoke().duration, trials))
            dur_mean = statistics.mean(durations)
            result = dur_mean
            self.trials[new_mem] = result

            if(new_mem != old_mem):
                self.update_mem(old_mem)
        return (dur_mean)
        
    def tune(self):
        improvement = self.mem

        while (improvement != None):
            self.dur = self.trial(improvement)

            more_mem = min(3008, random.uniform(1.5, 2.5)  * self.mem)
            more_dur = self.trial(more_mem)

            less_mem = max(128, random.uniform(0.3, 0.6) * self.mem)
            less_dur = self.trial(less_mem)

            if (less_dur * self.margin < self.dur):
                improvement = less_mem
                self.update_mem(less_mem)
            elif (more_dur * self.margin < self.dur):
                improvement = more_mem
                self.update_mem(more_mem)
            else:
                improvement = None
            
            log("Less Mem({:.0f} = {:.2f}) Current Mem({:.0f} = {:.2f}) More Mem({:.0f} = {:.2f})".format(less_mem,less_dur, self.mem,self.dur,more_mem,more_dur))
            log("Improvement = {}".format(improvement))
        
        log("Function tuned to {} = {}".format(self.mem,self.dur))
        

@click.command()
@click.option('--arn', required=True, help='ARN of the function to tuna.')
def lambda_tuna(arn=""):
    """Tuna your lambda functions."""
    Funktion(arn).tune()

if __name__ == '__main__':
    lambda_tuna()
