user_input = input()
# ruleid: custom-no-eval
eval(user_input)
# ok: custom-no-eval
eval("1 + 1")

import subprocess
# ruleid: custom-subprocess-shell-true
subprocess.run("ls " + user_input, shell=True)
# ok: custom-subprocess-shell-true
subprocess.run(["ls"], shell=False)
