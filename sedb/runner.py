import os
import sys
import resource
import subprocess
import difflib
import signal

# diff = difflib.ndiff(open(file1).readlines(),open(file2).readlines())

def setlimits():
    resource.setrlimit(resource.RLIMIT_STACK, (8000000, 8000000))

def compile(cmd):
	PIPE = subprocess.PIPE
	clist = cmd.split()
	# print("compiling",clist)
	p = subprocess.Popen(clist, stdout=PIPE, stderr=PIPE)
	out,err = p.communicate()
	return p.returncode

def run(cmd,input_file,output_file):
	inp = open(input_file,'r')
	PIPE = subprocess.PIPE
	clist = cmd.split()
	# print("running",clist)
	p = subprocess.Popen(clist, stdin=inp, stdout=PIPE, stderr=PIPE, preexec_fn=setlimits)
	out,err = p.communicate()
	print(p.returncode)
	if p.returncode !=0:
		return (out.decode('UTF-8'), signal.Signals(-1*p.returncode).name)
	ofile = open(output_file,'r')
	if out.decode('UTF-8') == ofile.read():
		return (out.decode('UTF-8'), "")
	else:
		return (out.decode('UTF-8'), "different output")