from distutils.core import setup
import py2exe

setup( windows = [ { "script": "view.py", "icon_resources": [(1, "view.ico")] } ] ,\
       options = {
                    "py2exe":
                    {
                    "compressed":1,
                    "optimize":2
                    }
                    }, zipfile=None)