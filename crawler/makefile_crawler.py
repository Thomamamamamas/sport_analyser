import os
import platform
import sys
import shutil

data_spec_file = "\tdatas=[('config/*', '.')],\n"
import_spec_file = ["shutil.copytree('config', '{0}/config/'.format(DISTPATH))\n"]

str_prefix = ''
str_exe = ''
if platform.system() == 'Windows':
    str_prefix = 'python'
    str_exe = '.exe'

def all():
    fclean()
    os.system("%s pyinstaller%s main.py --onefile  --add-binary 'driver\chromedriver.exe;driver\' --name crawler_sport_analyse" % (str_prefix, str_exe))
    modify_spec_file()
    os.system("%s pyinstaller%s --clean crawler_sport_analyse.spec")

def fclean():
    try:
        shutil.rmtree('dist', ignore_errors=False, onerror=None)
        shutil.rmtree('build', ignore_errors=False, onerror=None)
        os.remove("crawler_sport_analyse.spec")
    except:
        return

def modify_spec_file():
    tmp = ''
    with open('crawler_sport_analyse.spec', 'r') as spec_file:
        for line in spec_file:
            if 'datas=[],' not in line:
                tmp = tmp + line
            else:
                tmp = tmp + data_spec_file
        spec_file.close()
    tmp = tmp + 'import shutil\n'
    for i in range(0, len(import_spec_file)):
        tmp = tmp + import_spec_file[i]
    with open('crawler_sport_analyse.spec', 'w') as spec_file:
        spec_file.write(tmp)
        spec_file.close()


def makefile():
    if len(sys.argv) == 1 or sys.argv[0] == 'all':
        all()

if __name__ == '__main__':
    makefile()