from subprocess import run
from glob import glob
from shutil import rmtree
from os import cpu_count
from src.main import version

rmtree('src\\__pycache__', ignore_errors=True)

files = [f'--include-plugin-files={file}' for file in glob('src/*.py')]
files.remove('--include-plugin-files=src\\main.py')

cmd = ('nuitka --assume-yes-for-downloads --remove-output --standalone --onefile --follow-imports',
       f'--windows-company-name=" " --windows-product-name="GameTweak" --windows-file-version="{version}" --windows-product-version="{version}" --windows-file-description="GameTweak"',
       ' '.join(files), f'--lto=yes --jobs={cpu_count()} --disable-console -o gametweak.exe src\\main.py')

run(' '.join(cmd), shell=True)
