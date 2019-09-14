import glob
import subprocess
import os

with open('template.html', 'r') as myfile:
    template = myfile.read()

def write_to_file(path, s):
    with open(path, 'w') as myfile:
        myfile.write(s)

def read_from_file(path):
    with open(path, 'r') as myfile:
        data = myfile.read()

    return data

def with_path(path):
    dr = os.path.dirname(path)
    if os.path.normpath(dr) == '.':
        return template.replace('{prefix}', '.')
    else:
        return template.replace('{prefix}', '../../../')

def comp(d):
    raw = os.path.splitext(d)[0]
    dr = os.path.dirname(d)
    with open(d, 'r') as myfile:
        data=myfile.readlines()

    data.insert(2, '\\input{../../../style/extra.tex}\n')
    result = subprocess.run([
        'pandoc',
        '--from',
        'latex',
        '--mathjax',
        '--metadata',
        f"pagetitle={d}",
        ],
        cwd=dr,
        input="".join(data),
        encoding='utf8',
        stdout=subprocess.PIPE).stdout


    final = with_path(d).replace('{content}', result)

    with open(dr + '/main.html', 'w') as myfile:
        myfile.write(final)

    return dr + '/main.html'



    # subprocess.run(['cat'], cwd=dr, input="".join(data), encoding='utf8')

files = []
for d in glob.glob('uba/*/*/*.tex'):
    files.append(comp(d))

item = read_from_file('note_item.html')

write_to_file('index.html', with_path('index.html').replace('{content}',
    read_from_file('index_pre.html')))

body = ""
for f in files:
    body += item.replace('{link}', f).replace('{content}', f)

write_to_file('notes.html', with_path('notes.html').replace('{content}',
    read_from_file('notes_pre.html').replace('{content}', body)))
