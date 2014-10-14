import i3
from subprocess import call

num = next(x for x in i3.get_workspaces() if x['focused'])['num']
call([
    "i3-input",
    "-F rename workspace to \"{}: %s\"".format(num),
    "-PNew name: "])
