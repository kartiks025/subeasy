import resource
import signal
import subprocess


def setlimits(res):
    resource.setrlimit(resource.RLIMIT_STACK, (res.stack_limit*1000, res.stack_limit*1000+1))
    resource.setrlimit(resource.RLIMIT_CPU, (res.cpu_time, res.cpu_time+0.1))
    resource.setrlimit(resource.RLIMIT_FSIZE, (res.max_filesize*1000, res.max_filesize*1000+1))
    resource.setrlimit(resource.RLIMIT_DATA, (res.memory_limit*1000, res.memory_limit*1000+1))
    resource.setrlimit(resource.RLIMIT_NOFILE, (res.open_files, res.open_files))


def compile(cmd, work_dir):
    PIPE = subprocess.PIPE
    clist = cmd.split()
    p = subprocess.Popen(clist, stdout=PIPE, stderr=PIPE, cwd=work_dir)
    out, err = p.communicate()
    return p.returncode


def run(cmd, work_dir, inpView, outView, res):
    PIPE = subprocess.PIPE
    clist = cmd.split()
    print(clist)
    print(work_dir)
    p = subprocess.Popen(clist, stdin=PIPE, stdout=PIPE, stderr=PIPE,
                         preexec_fn=(lambda: setlimits(res)), cwd=work_dir)
    out, err = p.communicate(input=inpView)
    print(p.returncode,out)
    if p.returncode < 0:
        return out.decode('UTF-8'), signal.Signals(-1 * p.returncode).name
    if out == outView.tobytes():
        return out.decode('UTF-8'), 0
    else:
        return out.decode('UTF-8'), -1