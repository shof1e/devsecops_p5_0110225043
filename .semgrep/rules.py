import subprocess

# ruleid: custom-no-eval
cmd = input("Masukkan perintah: ")
eval(cmd)

# ok: custom-no-eval
eval("2 + 2")

# ruleid: custom-subprocess-shell-true
subprocess.run("echo hello", shell=True)

# ok: custom-subprocess-shell-true
subprocess.run(["echo", "hello"], shell=False)
