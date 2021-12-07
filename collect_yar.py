#!/usr/bin/env python3

import os
import subprocess
import glob
from pathlib import Path
from datetime import datetime




if os.path.exists('./rules-repo'):
    rc = subprocess.call("rm -rf rules-repo", shell=True)
if os.path.exists('./rules'):
    rc = subprocess.call("rm -rf rules", shell=True)
if os.path.exists('./repos'):
    rc = subprocess.call("rm -rf repos", shell=True)


# Clone all repos from repos.txt 
if not os.path.exists('./rules-repo'):
    rc = subprocess.call("mkdir rules-repo", shell=True)
    
    cmd = "cd rules-repo && git clone https://github.com/InQuest/awesome-yara.git "
    rc = subprocess.call(cmd, shell=True)

    cl = open("collects.txt", "w")
    cl.write(datetime.now().strftime("%H:%M:%S\n"))
    cl.close()

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



# Clone all repos from repos.txt 
if not os.path.exists('./repos'):
    rc = subprocess.call("mkdir repos", shell=True)



print("Clone all repos ...\n")
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

# root_dir needs a trailing slash (i.e. /root/dir/)
print("Move all *.yar file to ./rules ...\n")
for filename in glob.iglob('./repos/**/*.ya*', recursive=True):
    print(filename)
    rc = subprocess.call("mv "+filename +" ./rules", shell=True)


cl = open("collects.txt", "a")
cl.write(datetime.now().strftime("%H:%M:%S\n"))
cl.close()