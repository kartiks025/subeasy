import tarfile, smtplib, re
import pytz
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import *
from django.forms.models import model_to_dict

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from bcrypt import hashpw, gensalt
from django.shortcuts import redirect, reverse
from django.core import serializers
from django.db import connection

from .models import *

from io import BytesIO

from .utils import *
from .restricted_helpers import *
from .runner import *

@user2_required
def get_assign_home(request, sec_user_id, assign_id):
    if assign_id == '0':
        return JsonResponse(
            {
                'new_assign': True
            }
        )
    assignment = Assignment.objects.get(assignment_id=assign_id)
    deadline = assignment.deadline
    context = {'new_assign': False, 'assign': model_to_dict(assignment), 'deadline': model_to_dict(deadline)}
    return JsonResponse(context)


@user2_required
def download_helper_file(request, sec_user_id, assign_id):
    contents = Assignment.objects.get(assignment_id=assign_id).helper_file
    response = HttpResponse(contents)
    response['Content-Disposition'] = 'attachment; filename=' + Assignment.objects.get(
        assignment_id=assign_id).helper_file_name
    return response


# @instructor2_required
def download_problem_helper_file(request, sec_user_id, assign_id, prob_id):
    contents = Problem.objects.get(problem_id=prob_id).helper_file
    response = HttpResponse(contents)
    response['Content-Disposition'] = 'attachment; filename=' + Problem.objects.get(
        problem_id=prob_id).helper_file_name
    return response


# @instructor2_required
def download_problem_solution_file(request, sec_user_id, assign_id, prob_id):
    contents = Problem.objects.get(problem_id=prob_id).solution_file
    response = HttpResponse(contents)
    response['Content-Disposition'] = 'attachment; filename=' + Problem.objects.get(
        problem_id=prob_id).solution_filename
    return response


# @instructor2_required
def download_testcase_file(request, sec_user_id, assign_id, prob_id):
    out = BytesIO()
    tar = tarfile.open(mode="w:gz",fileobj=out)
    all_testcases = Testcase.objects.filter(problem_id=prob_id)
    for t in all_testcases:
        info = tarfile.TarInfo(name=t.infile_name)
        info.size = len(t.infile)
        tar.addfile(tarinfo=info,fileobj=BytesIO(t.infile))
        info = tarfile.TarInfo(name=t.outfile_name)
        info.size = len(t.outfile)
        tar.addfile(tarinfo=info,fileobj=BytesIO(t.outfile))
    tar.close()
    response = HttpResponse(out.getvalue())
    response['Content-Disposition'] = 'attachment; filename=' + "problem"+prob_id+"_testcases.tar.gz"
    return response


# @instructor2_required
def download_testcase_input_file(request, sec_user_id, assign_id, prob_id, testcase_no):
    contents = Testcase.objects.get(testcase_no=testcase_no,problem_id=prob_id).infile
    response = HttpResponse(contents)
    response['Content-Disposition'] = 'attachment; filename=' + Testcase.objects.get(
        testcase_no=testcase_no,problem_id=prob_id).infile_name
    return response


# @instructor2_required
def download_testcase_output_file(request, sec_user_id, assign_id, prob_id, testcase_no):
    contents = Testcase.objects.get(testcase_no=testcase_no,problem_id=prob_id).outfile
    response = HttpResponse(contents)
    response['Content-Disposition'] = 'attachment; filename=' + Testcase.objects.get(
        testcase_no=testcase_no,problem_id=prob_id).outfile_name
    return response


# @instructor2_required
def download_your_submission(request, sec_user_id, assign_id, prob_id):
    final = UserSubmissions.objects.get(user_id=request.session['user_id'],problem_id=prob_id).final_submission_no
    contents = Submission.objects.get(user_id=request.session['user_id'],problem_id=prob_id,sub_no=final)
    response = HttpResponse(contents.sub_file)
    response['Content-Disposition'] = 'attachment; filename=' + contents.sub_file_name
    return response


@user1_required
def get_assignments(request, sec_user_id):
    sec_user = SecUser.objects.get(id=sec_user_id);
    if sec_user.role == "Instructor" or sec_user.role == "TA":
        assign = Assignment.objects.filter(sec=sec_user.sec)
    elif sec_user.role == "Student":
        assign = Assignment.objects.filter(sec=sec_user.sec, visibility=True)
    assignments = [{'id': a.assignment_id, 'title': a.title} for a in assign]
    context = {'assignments': assignments}
    return JsonResponse(context, content_type="application/json")


@instructor_required
def get_instructors(request, sec_user_id):
    sec_user = SecUser.objects.get(id=sec_user_id);
    ins = SecUser.objects.filter(sec_id=sec_user.sec_id, role="Instructor")
    instructor = [{'id': a.user.user_id, 'name': a.user.name} for a in ins]
    print(instructor)
    context = {'instructor': instructor}
    return JsonResponse(context, content_type="application/json")





# @instructor2_required
def get_assign_prob(request, sec_user_id, assign_id, prob_id):
    print("get_assign_prob called")
    if prob_id == '0':
        return JsonResponse({
            'new_prob': True
        })
    problem = Problem.objects.get(problem_id=prob_id)
    resource = problem.resource_limit
    test = Testcase.objects.filter(problem_id=prob_id)
    testcases = [{'id': a.id, 'num': a.testcase_no, 'marks': a.marks, 'visibility': a.visibility} for a in test]
    # print(testcases)
    return JsonResponse({
        'new_prob': False,
        'problem': model_to_dict(problem),
        'resource': model_to_dict(resource),
        'testcases': testcases
    })


@user2_required
def get_assign_all_prob(request, sec_user_id, assign_id):
    print("all prob called")
    assignment = Assignment.objects.get(assignment_id=assign_id)
    problems = Problem.objects.filter(assignment=assignment)
    # testcases = Testcase.objects.filter()
    prob_json = []
    for problem in problems:
        test = Testcase.objects.filter(problem_id=problem.problem_id)
        testcases = [{'id': a.id, 'num': a.testcase_no, 'marks': a.marks, 'visibility': a.visibility} for a in test]
        prob_json.append({'problem': model_to_dict(problem), 'resource': model_to_dict(problem.resource_limit),
                          'testcases': testcases})
    # print(prob_json)
    return JsonResponse({
        'problems': prob_json
    })


def submit_problem(request, sec_user_id, assign_id, prob_id):
    try:
        sub_file = request.FILES['submission_file'].file.read()
        sub_file_name = request.FILES['submission_file'].name

        if UserSubmissions.objects.filter(user_id=request.session['user_id'],problem_id=prob_id).exists():
            print("yes")
            x = UserSubmissions.objects.get(user_id=request.session['user_id'],problem_id=prob_id)
            x.num_submissions = x.num_submissions + 1
            s = Submission(user_id=request.session['user_id'],problem_id=prob_id,sub_no=x.num_submissions,sub_file=sub_file,sub_file_name=sub_file_name)
            x.final_submission_no=x.num_submissions
            s.save()
            x.save()
        else:
            print("no")
            x = UserSubmissions(user_id=request.session['user_id'],problem_id=prob_id,num_submissions=1,final_submission_no=1)
            x.save()
            s = Submission(user_id=request.session['user_id'],problem_id=prob_id,sub_no=x.num_submissions,sub_file=sub_file,sub_file_name=sub_file_name)
            s.save()
            print("done")
        return JsonResponse({
            'success': True
        })
    except :
        pass
        return JsonResponse({
            'success': False
        })

def evaluate_problem(request, sec_user_id, assign_id, prob_id):
    # try:
    if UserSubmissions.objects.filter(user_id=request.session['user_id'],problem_id=prob_id).exists():
        final = UserSubmissions.objects.get(user_id=request.session['user_id'],problem_id=prob_id).final_submission_no
        contents = Submission.objects.get(user_id=request.session['user_id'],problem_id=prob_id,sub_no=final)
        problem = Problem.objects.get(problem_id=prob_id)
        compile_cmd = problem.compile_cmd
        # print(contents.sub_file)
        with open(problem.files_to_submit, "wb") as codeFile:
            codeFile.write(contents.sub_file)
        json=[]
        if not compile(compile_cmd):    
            testcases = Testcase.objects.filter(problem=problem)
            for t in testcases:
                with open(t.infile_name, "wb") as inFile:
                    inFile.write(t.infile)
                with open(t.outfile_name, "wb") as outFile:
                    outFile.write(t.outfile)
                (out,err) = run("./a.out",t.infile_name,t.outfile_name)
                if err == 0:
                    marks = t.marks
                else:
                    marks = 0
                json.append({"testcase_num":t.testcase_no,"visibility":t.visibility,"marks":marks,"out":out,"error":err})
            print(json)
        else:
            return JsonResponse({
                'success': True,
                'message' : "Compilation Error",
                'testcases' : json
            })
        return JsonResponse({
                'success': True,
                'message' : "Compiled Successfully",
                'testcases' : json
            })
        
    # except :
    #     pass
    #     return JsonResponse({
    #         'success': False,
    #         'message' : "except"
    #     })
    