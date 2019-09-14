import glob
import subprocess
import os

def comp(d):
    raw = os.path.splitext(d)[0]
    dr = os.path.dirname(d)
    with open(d, 'r') as myfile:
        data=myfile.readlines()
    data.insert(2, '\\input{../../../style/extra.tex}\n')
    subprocess.run([
        'pandoc',
        '-s',
        '--from',
        'latex',
        '--mathjax',
        '-o',
        'main.html',
        '--metadata',
        f"pagetitle={d}",
        ],
        cwd=dr,
        input="".join(data),
        encoding='utf8')
    # subprocess.run(['cat'], cwd=dr, input="".join(data), encoding='utf8')

for d in glob.glob('uba/*/*/*.tex'):
    comp(d)
