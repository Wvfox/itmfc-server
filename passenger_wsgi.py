import sys, os
INTERP = os.path.join(os.path.dirname(__file__), 'venv311/bin/python3')

if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'config'))

from config.wsgi import application