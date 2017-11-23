import os
import sys
import resource
import subprocess
import difflib
import signal


# diff = difflib.ndiff(open(file1).readlines(),open(file2).readlines())

def setlimits():
    resource.setrlimit(resource.RLIMIT_STACK, (8000000, 8000000))
    resource.setrlimit(resource.RLIMIT_CPU, (1, 2))


def compile(cmd, work_dir):
    PIPE = subprocess.PIPE
    clist = cmd.split()
    # print("compiling",clist)
    p = subprocess.Popen(clist, stdout=PIPE, stderr=PIPE, cwd=work_dir)
    out, err = p.communicate()
    return p.returncode


def run(cmd, work_dir, inpView, outView):
    # inp = open(input_file, 'r')
    PIPE = subprocess.PIPE
    clist = cmd.split()
    # print("running",clist)
    p = subprocess.Popen(clist, stdin=PIPE, stdout=PIPE, stderr=PIPE, preexec_fn=setlimits, cwd=work_dir)
    out, err = p.communicate(input=inpView)
    print(p.returncode)
    if p.returncode != 0:
        return out.decode('UTF-8'), signal.Signals(-1 * p.returncode).name
    # ofile = open(output_file, 'r')
    if out == outView.tobytes():
        return out.decode('UTF-8'), ""
    else:
        return out.decode('UTF-8'), "different output"
