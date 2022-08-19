from subprocess import run
from glob import glob
files = [f'--include-plugin-files={file}' for file in glob('src/*.py')]
files.remove('--include-plugin-files=src\\main.py')

cmd = ('nuitka --remove-output --standalone --onefile --follow-imports',
       ' '.join(files), '--disable-console', '-o gametweak.exe src\\main.py')
run(' '.join(cmd), shell=True)
