#!/usr/bin/env python3

import os
import subprocess
import glob
from pathlib import Path
from datetime import datetime
import hashlib


RULEKEYS = ['rule', 'meta:', 'strings:', 'condition:', '{', '}' ]
EXCEPTIONVARIABLES = [
    'exclude',
    'include',
    'file_name',
    'file_type',
    'imphash',
    'md5',
    'new_file',
    'positives',
    'sha1',
    'sha256',
    'signatures',
    'ssdeep',
    'submissions',
    'tags',
    'vhash',
    'acronis',
    'ad_aware',
    'aegislab',
    'ahnlab',
    'ahnlab_v3',
    'alibaba',
    'alyac',
    'antivir7',
    'antivir',
    'antiy_avl',
    'apex',
    'arcabit',
    'avast',
    'avast_mobile',
    'avg',
    'avira',
    'avware',
    'babable',
    'baidu',
    'bitdefender',
    'bitdefendertheta',
    'bkav',
    'cat_quickheal',
    'clamav',
    'cmc',
    'commtouch',
    'comodo',
    'crowdstrike',
    'cybereason',
    'cylance',
    'cynet',
    'cyren',
    'drweb',
    'egambit',
    'elastic',
    'emsisoft',
    'endgame',
    'escan',
    'eset_nod32',
    'f_prot',
    'f_secure',
    'fireeye',
    'fortinet',
    'gdata',
    'ikarus',
    'invincea',
    'jiangmin',
    'k7antivirus',
    'k7gw',
    'kaspersky',
    'kingsoft',
    'malwarebytes',
    'max',
    'maxsecure',
    'mcafee',
    'mcafee_gw_edition',
    'microsoft',
    'microworld_escan',
    'nano_antivirus',
    'nod32',
    'nprotect',
    'paloalto',
    'panda',
    'prevx1',
    'qihoo_360',
    'rising',
    'sangfor',
    'sentinelone',
    'sophos',
    'sunbelt',
    'superantispyware',
    'symantec',
    'symantecmobileinsight',
    'tachyon',
    'tencent',
    'thehacker',
    'totaldefense',
    'trapmine',
    'trendmicro',
    'trendmicro_housecall',
    'trustlook',
    'vba32',
    'vipre',
    'virobot',
    'webroot',
    'whitearmor',
    'yandex',
    'zillya',
    'zonealarm',
    'zoner']

if os.path.exists('./rules-repo'):
    rc = subprocess.call("rm -rf rules-repo", shell=True)
if os.path.exists('./repos'):
    rc = subprocess.call("rm -rf repos", shell=True)
if os.path.exists('./rules'):
    rc = subprocess.call("rm -rf rules", shell=True)


# Collect repo link
if not os.path.exists('./rules-repo'):
    rc = subprocess.call("mkdir rules-repo", shell=True)
    
    cmd = "cd rules-repo && git clone https://github.com/InQuest/awesome-yara.git "
    rc = subprocess.call(cmd, shell=True)

    # cl = open("collects.txt", "w")
    # cl.write(datetime.now().strftime("%H:%M:%S\n"))
    # cl.close()

    isRule = False

    with open('./rules-repo/awesome-yara/README.md') as f:
        for line in f.readlines():
            # collect only in Rules session
            if '##' in line:
                if 'Rules' in line:
                    isRule = True
                else:
                    isRule = False
            

            if isRule and 'https://github.com' in line:
                # get link github
                line = line.split("](")[1]
                line = line.split(")")[0]
                if line[len(line)-1] == '/':
                    line=line[:len(line)-1]
                    
                # print(line)
                line = line.split("/tree")[0] + '.git'
                # write github link to file 
                cl = open("collects.txt", "a")
                cl.write(line + '\n')
                cl.close()
                print(line)


# Clone all repos from collects.txt 
if not os.path.exists('./repos'):
    rc = subprocess.call("mkdir repos", shell=True)

    print("\n\n=================================<<< Clone all repos ... >>>=====================================\n")
    # repos.txt collect by rice
    # with open('repos.txt') as f:
    # collects.txt collect by script
    with open('collects.txt') as f:
        for link in f.readlines():
            if 'https://github.com' in link:
                cmd = "cd repos && git clone "+ link.split('\n')[0] + " " +link.split('/')[3] + "-" + link.split('/')[4].split('.git')[0]
                rc = subprocess.call(cmd, shell=True)
                print('')
                # print(cmd)


# Coppy all .yar file from repos to rules 
if not os.path.exists('./rules'):
    rc = subprocess.call("mkdir rules", shell=True)


HASH=[]

# Move all valid *.yar file to ./rules
print("\n\n=================================<<< Move all *.yar file to ./rules ... >>>=====================================\n")
command = ""
for filename in glob.iglob('./repos/**/*.ya*', recursive=True):
    try:
        # print(filename)
        subprocess.call("dos2unix "+filename, shell=True)
        with open(filename) as f:
            text = str(f.readlines())

            RULE_CHECK=True

            if text.count('{') != text.count('}'):
                RULE_CHECK=False

            if RULE_CHECK == True:
                for substring in RULEKEYS:
                    if not substring in text:
                        RULE_CHECK = False
                        break
                for substring in EXCEPTIONVARIABLES:
                    if substring in text:
                        RULE_CHECK = False
                        break

            if RULE_CHECK == True:

                val = int(hashlib.sha1(text.encode("utf-8")).hexdigest(), 16) % (10 ** 8)
                # print("val 0 : {} => val in HASH : {}".format(val, val in HASH))
                # HASH.append(val)
                # print("val 1 : {} => val in HASH : {}".format(val, val in HASH))
                if not val in HASH:
                    HASH.append(val)
                    filename = filename.replace(' ','\ ')
                    command = "mv "+filename +" ./rules ;\n"
                    print(command)
                    rc = subprocess.call("mv "+filename +" ./rules", shell=True)
                print("val 1 : {} => val in HASH : {}".format(val, val in HASH))
                
    except OSError:
        print("Error: {}".format(OSError))
    except UnicodeDecodeError:
        print("Error: {}".format(UnicodeDecodeError))
    else:
        f.close()


# cl = open("collects.txt", "a")
# cl.write(datetime.now().strftime("%H:%M:%S\n"))
# cl.close()