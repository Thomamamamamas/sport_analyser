import os
import platform
import sys
import shutil

data_spec_file = "\tdatas=[('config/*', '.')],\n"
import_spec_file = ["shutil.copytree('config', '{0}/config/'.format(DISTPATH))\n",
                    "shutil.copytree('driver', '{0}/driver/'.format(DISTPATH))\n"]

if platform.system() == 'Darwin':
    str_prefix = ''
    str_exe = ''
    str_binaries = ""
if platform.system() == 'Windows':
    str_prefix = 'python'
    str_exe = '.exe'
    str_binaries = "--add-binary 'driver\chromedriver.exe;driver\\'"

def all():
    fclean()
    os.system("%s pyinstaller%s crawler_main.py --onefile  %s --name crawler_sport_analyse" % (str_prefix, str_exe, str_binaries))
    modify_spec_file()
    os.system("%s pyinstaller%s --clean crawler_sport_analyse.spec" % (str_prefix, str_exe))

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
            if 'datas=[],' not in line and 'binaries=[' not in line:
                tmp = tmp + line
            elif 'binaries=[' in line:
                tmp = tmp + line.replace("'", "")
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