import os
import sys
import resource
import subprocess
import difflib

# diff = difflib.ndiff(open(file1).readlines(),open(file2).readlines())

def setlimits():
    resource.setrlimit(resource.RLIMIT_STACK, (8000000, 8000000))

def compile(cmd):
	PIPE = subprocess.PIPE
	clist = cmd.split()
	print("compiling",clist)
	p = subprocess.Popen(clist, stdout=PIPE, stderr=PIPE)
	out,err = p.communicate()
	print(p.returncode)

def run(cmd,input_file,output_file):
	inp = open(input_file,'r')
	PIPE = subprocess.PIPE
	clist = cmd.split()
	print("running",clist)
	p = subprocess.Popen(clist, stdin=inp, stdout=PIPE, stderr=PIPE, preexec_fn=setlimits)
	out,err = p.communicate()
	print(p.returncode)

	ofile = open(output_file,'r')
	# diff = difflib.SequenceMatcher(None,out,)
	# print(out.decode('UTF-8'))
	print(out.decode('UTF-8') == ofile.read())