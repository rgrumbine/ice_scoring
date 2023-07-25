# Check that the packages are installed.
from pkgutil import iter_modules
import sys

def check_import(packagename):
    if packagename in (name for _, name, _ in iter_modules()):
        return True
    else:
        return False

assert sys.version_info.major >= 3 and sys.version_info.minor >= 6, 'Please install Python 3.6!'

packages = [ 'math', 'csv', 'datetime', 'os',  'pkgutil', 'pstats', 'netCDF4', 'matplotlib', 'numpy' ]

all_passed = True
for p in packages:
  assert check_import(p), \
    '{0} not present. Please install via pip or conda.'.format(p)

if all_passed:
    print('All checks passed. Your python environment is good to go!')

