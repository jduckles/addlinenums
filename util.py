import subprocess


def pandoc(arguments, cwd=None):
    PANDOC="/usr/bin/pandoc"
    command = list()
    command.append(PANDOC)
    command = command + arguments
    print("Running {}".format(command))
    subprocess.run(command, cwd=cwd)
