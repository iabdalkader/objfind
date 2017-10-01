#! /usr/bin/env python
import os, sys
import subprocess
from operator import itemgetter

if __name__ == "__main__":
    if len(sys.argv) == 1 or not (sys.argv[1] in ('text', 'bss', 'data')):
        print('objfind.py <sort key (text, bss or data)>')
        sys.exit(1)
    
    objfiles = []
    sortkey = sys.argv[1]
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".o"):
                 objfiles.append({'path':os.path.join(root, file)})

    for i, obj in enumerate(objfiles):
        try:
            output = subprocess.check_output(['size', obj['path']])
        except subprocess.CalledProcessError as e:
            print('size stdout output:\n', e.output)
        sizes = [int(s) for s in output.split() if s.isdigit()]
        objfiles[i]['text'] = sizes[0]
        objfiles[i]['data'] = sizes[1]
        objfiles[i]['bss']  = sizes[2]

print(sortkey + '\t' + "object file")
for obj in sorted(objfiles, key=itemgetter(sortkey)):
    print(str(obj[sortkey]) + '\t' + obj['path'])
