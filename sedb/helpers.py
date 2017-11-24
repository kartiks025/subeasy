import tarfile, smtplib, re

import os
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
from collections import namedtuple

from .models import *

from io import BytesIO

from .utils import *
from .restricted_helpers import *
from .runner import *
from io import StringIO


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
    tar = tarfile.open(mode="w:gz", fileobj=out)
    all_testcases = Testcase.objects.filter(problem_id=prob_id)
    for t in all_testcases:
        info = tarfile.TarInfo(name=t.infile_name)
        info.size = len(t.infile)
        tar.addfile(tarinfo=info, fileobj=BytesIO(t.infile))
        info = tarfile.TarInfo(name=t.outfile_name)
        info.size = len(t.outfile)
        tar.addfile(tarinfo=info, fileobj=BytesIO(t.outfile))
    tar.close()
    response = HttpResponse(out.getvalue())
    response['Content-Disposition'] = 'attachment; filename=' + "problem" + prob_id + "_testcases.tar.gz"
    return response


# @instructor2_required
def download_testcase_input_file(request, sec_user_id, assign_id, prob_id, testcase_no):
    contents = Testcase.objects.get(testcase_no=testcase_no, problem_id=prob_id).infile
    response = HttpResponse(contents)
    response['Content-Disposition'] = 'attachment; filename=' + Testcase.objects.get(
        testcase_no=testcase_no, problem_id=prob_id).infile_name
    return response


# @instructor2_required
def download_testcase_output_file(request, sec_user_id, assign_id, prob_id, testcase_no):
    contents = Testcase.objects.get(testcase_no=testcase_no, problem_id=prob_id).outfile
    response = HttpResponse(contents)
    response['Content-Disposition'] = 'attachment; filename=' + Testcase.objects.get(
        testcase_no=testcase_no, problem_id=prob_id).outfile_name
    return response


# @instructor2_required
def download_your_submission(request, sec_user_id, assign_id, prob_id):
    final = UserSubmissions.objects.get(user_id=request.session['user_id'], problem_id=prob_id).final_submission_no
    contents = Submission.objects.get(user_id=request.session['user_id'], problem_id=prob_id, sub_no=final)
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
    testcases = [{'id': a.id, 'infile_name' : a.infile_name, 'outfile_name' : a.outfile_name, 'num': a.testcase_no, 'marks': a.marks, 'visibility': a.visibility}  for a in test]
    # print(testcases)
    return JsonResponse({
        'new_prob': False,
        'problem': model_to_dict(problem),
        'resource': model_to_dict(resource),
        'testcases': testcases
    })

# @instructor2_required
def get_user_assign_prob(request, sec_user_id, assign_id, prob_id):
    problem = Problem.objects.get(problem_id=prob_id)
    resource = problem.resource_limit
    test = Testcase.objects.filter(problem_id=prob_id)
    try:
        final = UserSubmissions.objects.get(user_id=request.session['user_id'], problem_id=prob_id).final_submission_no
        contents = Submission.objects.get(user_id=request.session['user_id'], problem_id=prob_id, sub_no=final)
    except:
        c = namedtuple('c', 'id')
        contents = c(id=0)
    print(contents)
    print(contents.id)
    cursor = connection.cursor()
    cursor.execute(
        '''select * from (select id,testcase_no,marks,visibility,infile_name,outfile_name from testcase where problem_id=%s and visibility=true) test left outer join (select testcase_id,id,marks as user_marks,error from sub_test where sub_id=%s) sub on sub.testcase_id=test.id;''',
        [prob_id, contents.id])
    testcases = dictfetchall(cursor)

    cursor = connection.cursor()
    cursor.execute(
        '''select testcase_no,marks,user_marks from (select id,testcase_no,marks from testcase where problem_id=%s and visibility=false) test left outer join (select testcase_id,marks as user_marks from sub_test where sub_id=%s) sub on sub.testcase_id=test.id''',
        [prob_id, contents.id])
    hidden = dictfetchall(cursor)
    # testcases = [{'id': a.id, 'num': a.testcase_no, 'marks': a.marks, 'visibility': a.visibility} for a in test]
    # print(testcases)
    print(hidden)
    return JsonResponse({
        'new_prob': False,
        'problem': model_to_dict(problem),
        'resource': model_to_dict(resource),
        'testcases': testcases,
        'hidden' : hidden
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
        testcases = [{'id': a.id, 'infile_name' : a.infile_name, 'outfile_name' : a.outfile_name, 'num': a.testcase_no, 'marks': a.marks, 'visibility': a.visibility} for a in test]
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

        if UserSubmissions.objects.filter(user_id=request.session['user_id'], problem_id=prob_id).exists():
            print("yes")
            x = UserSubmissions.objects.get(user_id=request.session['user_id'], problem_id=prob_id)
            x.num_submissions = x.num_submissions + 1
            s = Submission(user_id=request.session['user_id'], problem_id=prob_id, sub_no=x.num_submissions,
                           sub_file=sub_file, sub_file_name=sub_file_name)
            x.final_submission_no = x.num_submissions
            s.save()
            x.save()
        else:
            print("no")
            x = UserSubmissions(user_id=request.session['user_id'], problem_id=prob_id, num_submissions=1,
                                final_submission_no=1)
            x.save()
            s = Submission(user_id=request.session['user_id'], problem_id=prob_id, sub_no=x.num_submissions,
                           sub_file=sub_file, sub_file_name=sub_file_name)
            s.save()
            print("done")
        return JsonResponse({
            'success': True
        })
    except:
        pass
        return JsonResponse({
            'success': False
        })


def evaluate_problem(request, sec_user_id, assign_id, prob_id):
    try:
        print("evaluate_problem called")
        if UserSubmissions.objects.filter(user_id=request.session['user_id'], problem_id=prob_id).exists():
            final = UserSubmissions.objects.get(user_id=request.session['user_id'], problem_id=prob_id).final_submission_no
            contents = Submission.objects.get(user_id=request.session['user_id'], problem_id=prob_id, sub_no=final)
            problem = Problem.objects.get(problem_id=prob_id)
            compile_cmd = problem.compile_cmd
            # print(contents.sub_file)
            print("database fetched")

            work_dir = 'sedb/submissions/assign'+assign_id+'/prob'+prob_id+'/sec_user'+sec_user_id
            if not os.path.exists(work_dir):
                os.makedirs(work_dir)

            with open(work_dir+'/'+problem.files_to_submit, "wb") as codeFile:
                codeFile.write(contents.sub_file)

            print("directory created")

            json = []
            hidden = []
            print(work_dir)
            print(compile_cmd)
            if not compile(compile_cmd, work_dir):
                print("compiled")
                testcases = Testcase.objects.filter(problem=problem)
                for t in testcases:
                    (out, err) = run("./a.out", work_dir, t.infile, t.outfile, problem.resource_limit)
                    # print()
                    # print(out)
                    # print()
                    if err == 0:
                        marks = t.marks
                    else:
                        marks = 0
                    s,created = SubTest.objects.update_or_create(testcase = t,sub=contents,defaults={'marks':marks,'error':err,'output':out.encode('UTF-8')})
                    s.save()
                message = "Compiled Successfully"
            else:
                message = "Compilation Error"
            cursor = connection.cursor()
            cursor.execute(
                '''select * from (select id,testcase_no,marks,visibility,infile_name,outfile_name from testcase where problem_id=%s and visibility=true) test left outer join (select testcase_id,id,marks as user_marks,error from sub_test where sub_id=%s) sub on sub.testcase_id=test.id;''',
                [prob_id, contents.id])
            json = dictfetchall(cursor)

            cursor = connection.cursor()
            cursor.execute(
                '''select testcase_no,marks,user_marks from (select id,testcase_no,marks from testcase where problem_id=%s and visibility=false) test left outer join (select testcase_id,marks as user_marks from sub_test where sub_id=%s) sub on sub.testcase_id=test.id''',
                [prob_id, contents.id])
            hidden = dictfetchall(cursor)
            # testcases = [{'id': a.id, 'num': a.testcase_no, 'marks': a.marks, 'visibility': a.visibility} for a in test]
            # print(testcases)
            return JsonResponse({
                'success': True,
                'message': message,
                'testcases': json,
                'hidden' : hidden,
                'problem_id': prob_id
            })

    except :
        pass
        return JsonResponse({
            'success': False,
            'message' : "No file submitted"
        })
