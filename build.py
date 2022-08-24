from subprocess import run
from shutil import rmtree
from os import cpu_count
from pathlib import Path

for path in Path('src').glob('**/__pycache__'):
       rmtree(path)

version = '1.0.0'
files = [f'--include-plugin-files={file}' for file in Path('src').rglob('**/*.py')]
files.remove('--include-plugin-files=src\\main.py')

cmd = ('nuitka --assume-yes-for-downloads --remove-output --standalone --onefile --follow-imports',
       f'--windows-company-name=" " --windows-product-name="GameTweak" --windows-file-version="{version}" --windows-product-version="{version}" --windows-file-description="GameTweak"',
       ' '.join(files), f'--lto=yes --jobs={cpu_count()} --disable-console -o GameTweak.exe src\\main.py')

run(' '.join(cmd), shell=True)
