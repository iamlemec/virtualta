# convert files to text in bulk

import re
import os
import mammoth
import nbformat
import nbconvert
from glob import glob
from functools import partial

def ignore_images(image):
    return ''

def replace_extension(path, ext):
    dname, fname = os.path.split(path)
    name, _ = os.path.splitext(fname)
    return os.path.join(dname, f'{name}.{ext}')

def dir_to_dir(func, iext, oext):
    def wrapper(path, output):
        idir = os.path.isdir(path)
        odir = os.path.isdir(output)

        if idir and odir:
            for f in glob(f'*.{iext}', root_dir=path):
                p = os.path.join(path, f)
                o = os.path.join(output, f)
                m = replace_extension(o, oext)
                try:
                    func(p, m)
                except Exception as e:
                    print(f'Error converting {f}: {e}')
        elif not idir and not odir:
            func(path, output)
        else:
            raise ValueError('Input and output must both be directories or files')
    return wrapper

@partial(dir_to_dir, iext='docx', oext='md')
def convert_docx(path, output):
    print(f'convert_docx: {path} → {output}')
    with open(path, 'rb') as docx_file:
        result = mammoth.convert_to_markdown(docx_file, convert_image=ignore_images)
    with open(output, 'w') as md_file:
        md_file.write(result.value)

@partial(dir_to_dir, iext='ipynb', oext='md')
def convert_jupyter(path, output):
    print(f'convert_jupyter: {path} → {output}')
    notebook = nbformat.read(path, as_version=4)
    exporter = nbconvert.MarkdownExporter()
    body, resources = exporter.from_notebook_node(notebook)
    with open(output, 'w') as out:
        out.write(body)

def merge_markdown(path, output):
    with open(output, 'w') as out:
        for f in glob('*.md', root_dir=path):
            b, _ = os.path.splitext(f)
            p = os.path.join(path, f)
            with open(p, 'r') as inp:
                md = inp.read()
                title = ' '.join(re.split(r'[\s\.\-_]+', b))
                out.write(f'# {title}\n\n{md}\n\n---\n\n')
