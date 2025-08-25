# Python 3.12.10
import os, sys, markdown
from urllib.parse import unquote
from jinja2 import Environment, FileSystemLoader
template = Environment(
    autoescape=True,
    loader=FileSystemLoader('/tmp/templates'),
).get_template('index.html')
os.chdir('/tmp')

sys.path.insert(0, os.getcwd())
from lib import hide

import_v('pymdownx.snippets', '9.11', 'pymdown-extensions')

def main():
    # Remove the flag - lets see if you can find me now!
    flag = ""
    hide.selfDestruct()

    payload = unquote("")

    msg = markdown.markdown(
        payload,
        extensions=['pymdownx.snippets'],
        extension_configs={
            'pymdownx.snippets': {
                'encoding': 'latin1'
            },
            'base_path': './templates',
            'check_paths': True
        }
    )
    resp = "You found the flag! &#x1F6A9;" if hide.validate(msg) else hide.notfound()

    print( template.render(msg=msg, msg_resp=resp) )

main()
