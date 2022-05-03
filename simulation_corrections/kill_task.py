#!/usr/bin/env python3
import sys, os, re, subprocess

file_keyword = sys.argv[1]
#file_keyword = 'dengwei'

print(f'ps aux | grep \"{file_keyword}\"')

output = subprocess.Popen(f'ps aux | grep \"{file_keyword}\"', shell=True, stdout=subprocess.PIPE).stdout.read()

""" convert byte to utf-8 """
output = output.decode('utf-8')

id_list = []
for line in output.split('\n'):
    if 'sshd' in line:
        continue
    print(line)
    m = re.match(r'deng106\s+(\d+) .*', line)
    
    if m:
        jobid = m.group(1)
        id_list.append(jobid)

print('Jobid list')
print(id_list)
os.system('kill ' + ' '.join(id_list))
os.system(f'ps aux | grep \"{file_keyword}\"')
