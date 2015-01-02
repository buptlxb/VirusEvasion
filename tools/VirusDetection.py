#!/usr/bin/env python
import sys
import os
import VirusTotal

args = sys.argv[:]
if len(args) < 2:
    print 'Usage:{0} INPUT'.format(sys.argv[0])
    sys.exit(1)

if os.name == 'nt':
    nul = 'nul'
elif os.name == 'posix':
    nul = '/dev/null'
else:
    print 'Unknown platform'

print '[+] Generating obfuscation options.'
apikey = r'34bfa9160e5ec9834a7aed717991c933a5ec9749615a0fceca71ff9afbd26a85'
cmd = r'python ../VirusEvasion.py --binary ' + sys.argv[1] + ' --output '
entry_size = [128, 512, 1024, 4096]
entry_options = [' ']
entry_options.extend(['-e ' + str(x) for x in entry_size])
data_options = [' ', '-d']

print '[+] Obfuscating the binary...'
print '[+] Uploading the obfuscated copy...'

d = os.path.dirname('Result/')
if not os.path.exists(d):
    os.makedirs(d)

counter = 0
resources = []
for eo in entry_options:
    for do in data_options:
        if eo == ' ' and do == ' ':
            continue
        output = 'Result/output{0:d}.exe~'.format(counter)
        os_cmd = '{0}{1} {2} {3} >{4}'.format(cmd, output, eo, do, nul)
        os.system(os_cmd)
        file_handler = open(output, 'rb')
        resources.append([VirusTotal.scan(apikey, file_handler), '{0} {1}'.format(eo, do)])
        counter += 1


print '[+] Retrieving scan report...'

Keys = ['AVG', 'Kaspersky', 'McAfee', 'Qihoo-360', 'Symantec']
print '{0:15s}'.format('Options'),
for key in Keys:
    print '{0:10s}'.format(key),
print '{0:10s}'.format('Overall')

while len(resources) != 0:
    resource = resources[-1][0]
    result = VirusTotal.report(apikey, resource)
    if result is None:
        continue
    print '{0:15s}'.format(resources[-1][1]),
    for key in Keys:
        if result['scans'][key]['detected']:
            print '{0:10s}'.format('FAIL'),
        else:
            print '{0:10s}'.format('PASS'),
    print result['positives'], '/', result['total']
    del resources[-1]