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
import datetime
import traceback
from .models import *

from io import BytesIO

from .utils import *
from .restricted_helpers import *
from .runner import *
from io import StringIO
import csv


@user2_required #checked
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


@user2_required #checked
def download_helper_file(request, sec_user_id, assign_id):
    try:
        contents = Assignment.objects.get(assignment_id=assign_id).helper_file
        response = HttpResponse(contents)
        response['Content-Disposition'] = 'attachment; filename=' + Assignment.objects.get(
            assignment_id=assign_id).helper_file_name
    except:
        response = HttpResponse("")
        response['Content-Disposition'] = 'attachment; filename=' + "null"
    return response


@user3_required #checked
def download_problem_helper_file(request, sec_user_id, assign_id, prob_id):
    try:
        contents = Problem.objects.get(problem_id=prob_id).helper_file
        response = HttpResponse(contents)
        response['Content-Disposition'] = 'attachment; filename=' + Problem.objects.get(
            problem_id=prob_id).helper_file_name
    except:
        response = HttpResponse("")
        response['Content-Disposition'] = 'attachment; filename=' + "null"
    return response


@user3_required #checked
def download_problem_solution_file(request, sec_user_id, assign_id, prob_id):
    try:
        assignment = Assignment.objects.get(assignment_id=assign_id)
        problem = Problem.objects.get(problem_id=prob_id)
        sec_user = SecUser.objects.get(id=sec_user_id)
        if sec_user.role == "Student" and (datetime.datetime.now() < assignment.deadline.freezing_deadline or not problem.sol_visibility):
            response = HttpResponse("")
            response['Content-Disposition'] = 'attachment; filename=' + "null"
            return response
        contents = Problem.objects.get(problem_id=prob_id).solution_file
        response = HttpResponse(contents)
        response['Content-Disposition'] = 'attachment; filename=' + Problem.objects.get(
            problem_id=prob_id).solution_filename
    except:
        print(traceback.format_exc())
        response = HttpResponse("")
        response['Content-Disposition'] = 'attachment; filename=' + "null"
    return response


@user3_required #checked
def download_testcase_file(request, sec_user_id, assign_id, prob_id):
    out = BytesIO()
    tar = tarfile.open(mode="w:gz", fileobj=out)
    all_testcases = Testcase.objects.filter(problem_id=prob_id)
    sec_user = SecUser.objects.get(id=sec_user_id)
    for t in all_testcases:
        if sec_user.role == "Student" and not t.visibility:
            continue
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


@user4_required #checked
def download_testcase_input_file(request, sec_user_id, assign_id, prob_id, testcase_no):
    try:
        sec_user = SecUser.objects.get(id=sec_user_id)
        t = Testcase.objects.get(testcase_no=testcase_no, problem_id=prob_id)
        if sec_user.role == "Student" and not t.visibility:
            response = HttpResponse("")
            response['Content-Disposition'] = 'attachment; filename=' + "null"
            return response
        contents = t.infile
        response = HttpResponse(contents)
        response['Content-Disposition'] = 'attachment; filename=' + Testcase.objects.get(
            testcase_no=testcase_no, problem_id=prob_id).infile_name
    except:
        print(traceback.format_exc())
        response = HttpResponse("")
        response['Content-Disposition'] = 'attachment; filename=' + "null"
    return response


@user4_required #checked
def download_testcase_output_file(request, sec_user_id, assign_id, prob_id, testcase_no):
    try:
        sec_user = SecUser.objects.get(id=sec_user_id)
        t = Testcase.objects.get(testcase_no=testcase_no, problem_id=prob_id)
        if sec_user.role == "Student" and not t.visibility:
            response = HttpResponse("")
            response['Content-Disposition'] = 'attachment; filename=' + "null"
            return response
        contents = t.outfile
        response = HttpResponse(contents)
        response['Content-Disposition'] = 'attachment; filename=' + Testcase.objects.get(
            testcase_no=testcase_no, problem_id=prob_id).outfile_name
    except:
        print(traceback.format_exc())
        response = HttpResponse("")
        response['Content-Disposition'] = 'attachment; filename=' + "null"
    return response


@user3_required #checked
def download_your_submission(request, sec_user_id, assign_id, prob_id):
    try:
        final = UserSubmissions.objects.get(user_id=request.session['user_id'], problem_id=prob_id).final_submission_no
        contents = Submission.objects.get(user_id=request.session['user_id'], problem_id=prob_id, sub_no=final)
        response = HttpResponse(contents.sub_file)
        response['Content-Disposition'] = 'attachment; filename=' + contents.sub_file_name
    except:
        response = HttpResponse("")
        response['Content-Disposition'] = 'attachment; filename=' + "null"
    return response


@user1_required #checking done
def get_assignments(request, sec_user_id):
    sec_user = SecUser.objects.get(id=sec_user_id);
    if sec_user.role == "Instructor" or sec_user.role == "TA":
        assign = Assignment.objects.filter(sec=sec_user.sec)
    elif sec_user.role == "Student":
        assign = Assignment.objects.filter(sec=sec_user.sec, visibility=True, publish_time__lt=datetime.datetime.now()).order_by('-publish_time')
    assignments = []
    for a in assign:
        print(datetime.datetime.now())
        print(a.publish_time)
        if datetime.datetime.now() > a.deadline.soft_deadline:
            print("yes")    
            assignments.append({'id': a.assignment_id, 'title': a.title, 'active':False})
        else:
            assignments.append({'id': a.assignment_id, 'title': a.title, 'active':True})
        print()
    context = {'assignments': assignments}
    return JsonResponse(context, content_type="application/json")


@instructor_required #checking done
def get_instructors(request, sec_user_id):
    sec_user = SecUser.objects.get(id=sec_user_id);
    ins = SecUser.objects.filter(sec_id=sec_user.sec_id, role="Instructor")
    instructor = [{'id': a.user.user_id, 'name': a.user.name} for a in ins]
    print(instructor)
    context = {'instructor': instructor}
    return JsonResponse(context, content_type="application/json")


@user3_required #checking done
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

@student2_required  #checking done
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

    assignment = Assignment.objects.get(assignment_id=assign_id)
    print(assignment.deadline.freezing_deadline)
    print(datetime.datetime.now())
    print()
    if datetime.datetime.now() < assignment.deadline.freezing_deadline or not problem.sol_visibility:
        sol_visibility = False
    else:
        sol_visibility = True
    # testcases = [{'id': a.id, 'num': a.testcase_no, 'marks': a.marks, 'visibility': a.visibility} for a in test]
    # print(testcases)
    # print(hidden)

    if datetime.datetime.now() > assignment.deadline.hard_deadline:
        can_submit = False
    else:
        can_submit = True

    try:
        final = UserSubmissions.objects.get(user_id=request.session['user_id'], problem_id=prob_id).final_submission_no
        sub_file_name = Submission.objects.get(user_id=request.session['user_id'], problem_id=prob_id, sub_no=final).sub_file_name
    except:
        sub_file_name = ""
    return JsonResponse({
        'new_prob': False,
        'problem': model_to_dict(problem),
        'resource': model_to_dict(resource),
        'testcases': testcases,
        'hidden' : hidden,
        'sol_visibility' : sol_visibility,
        'sub_file_name' : sub_file_name,
        'can_submit' : can_submit
    })

@user2_required #checked
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

@student2_required #checked
def submit_problem(request, sec_user_id, assign_id, prob_id):
    try:
        assignment = Assignment.objects.get(assignment_id=assign_id)
        if(assignment.deadline.hard_deadline<datetime.datetime.now()):
            return JsonResponse({
                'success': False,
                'message': 'Cannot submit beyond time'
            })
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
        if assignment.deadline.soft_deadline>datetime.datetime.now():
            days,hours,minutes,seconds = diff_time(assignment.deadline.soft_deadline,datetime.datetime.now())
            message = "Submitted Successfully before "+str(days)+" days, "+str(hours)+" hours, "+str(minutes)+" minutes, "+str(seconds)+" seconds."
        else:
            days,hours,minutes,seconds = diff_time(datetime.datetime.now(),assignment.deadline.soft_deadline)
            message = "Submitted Successfully after "+str(days)+" days, "+str(hours)+" hours, "+str(minutes)+" minutes, "+str(seconds)+" seconds."
        return JsonResponse({
            'success': True,
            'message': message,
            'sub_file_name': sub_file_name,
            'problem_id': prob_id
        })
    except:
        print(traceback.format_exc())
        return JsonResponse({
            'success': False,
            'message': 'Submission Error'
        })

@user3_required #check
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
            total_marks = 0
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
                        total_marks = total_marks + marks
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

            contents.marks_auto = total_marks
            contents.save()
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

@instructor1_required
def evaluate_all(request,sec_user_id,assign_id):
    cursor = connection.cursor()
    cursor.execute('''select user_id,name from "user" where user_id in (select user_id from sec_user where sec_id in (select sec_id from sec_user where id=%s) and role='Student')''',[sec_user_id])
    userArr = dictfetchall(cursor)

    cursor = connection.cursor()
    cursor.execute('''select problem_id from problem where assignment_id=%s order by problem_no''',[assign_id])
    problemArr = dictfetchall(cursor)

    sec_id = SecUser.objects.get(id=sec_user_id).sec_id

    for user in userArr:
        for prob in problemArr:
            try:
                print("evaluate_problem called")
                prob_id = prob['problem_id']
                if UserSubmissions.objects.filter(user_id=user['user_id'], problem_id=prob_id).exists():
                    final = UserSubmissions.objects.get(user_id=user['user_id'], problem_id=prob_id).final_submission_no
                    contents = Submission.objects.get(user_id=user['user_id'], problem_id=prob_id, sub_no=final)
                    problem = Problem.objects.get(problem_id=prob_id)
                    compile_cmd = problem.compile_cmd
                    # print(contents.sub_file)
                    print("database fetched")
                    sec_user_id = SecUser.objects.get(user_id=user['user_id'],sec_id=sec_id).id

                    work_dir = 'sedb/submissions/assign'+assign_id+'/prob'+str(prob_id)+'/sec_user'+str(sec_user_id)
                    if not os.path.exists(work_dir):
                        os.makedirs(work_dir)

                    with open(work_dir+'/'+problem.files_to_submit, "wb") as codeFile:
                        codeFile.write(contents.sub_file)

                    print("directory created")

                    json = []
                    hidden = []
                    print(work_dir)
                    print(compile_cmd)
                    total_marks = 0
                    if not compile(compile_cmd, work_dir):
                        print("compiled")
                        testcases = Testcase.objects.filter(problem=problem)
                        
                        for t in testcases:
                            (out, err) = run("./a.out", work_dir, t.infile, t.outfile, problem.resource_limit)
                            if err == 0:
                                marks = t.marks
                                total_marks = total_marks + marks
                            else:
                                marks = 0
                            s,created = SubTest.objects.update_or_create(testcase = t,sub=contents,defaults={'marks':marks,'error':err,'output':out.encode('UTF-8')})
                            s.save()
                    contents.marks_auto = total_marks
                    contents.save()
            except :
                print(traceback.format_exc())
    return JsonResponse({
                'success': True
            })


#@user_required check remaining
def download_submission(request,sub_id):
    contents = Submission.objects.get(id=sub_id)
    response = HttpResponse(contents.sub_file)
    response['Content-Disposition'] = 'attachment; filename=' + contents.sub_file_name
    return response

@instructor1_required # check
def get_all_submissions(request, sec_user_id, assign_id):
    print("get_all_submissions called")

    cursor = connection.cursor()
    cursor.execute('''select user_id,name from "user" where user_id in (select user_id from sec_user where sec_id in (select sec_id from sec_user where id=%s) and role='Student')''',[sec_user_id])
    userArr = dictfetchall(cursor)
    # print(userArr)

    cursor = connection.cursor()
    cursor.execute('''select problem_no from problem where assignment_id=%s order by problem_no''',[assign_id])
    problemArr = dictfetchall(cursor)

    cursor = connection.cursor()
    cursor.execute(
        '''with A as (select * from problem where assignment_id=%s),B as (select * from "user" where user_id in (select user_id from sec_user where sec_id in (select sec_id from sec_user where id=%s) and role='Student')),C as (select user_id,problem_id,final_submission_no as sub_no from user_submissions where problem_id in (select problem_id from A)),D as (select * from submission where (user_id,problem_id,sub_no) in (select * from C)),E as (select user_id,name,problem_id,problem_no from A,B) select user_id,name,problem_no,id,sub_file_name,marks_auto,marks_inst from E natural left outer join D order by problem_no''',
        [assign_id, sec_user_id])
    submissionArr = dictfetchall(cursor)

    allSubmissions = []

    for user in userArr:
        user_id = user['user_id']
        name = user['name']
        submissionList = []
        for elt in submissionArr:
            if elt['user_id'] == user_id:
                submissionList.append({'problem_no':elt['problem_no'],'marks':elt['marks_auto'],'marks_inst':elt['marks_inst'],'sub_id':elt['id'],'sub_file_name':elt['sub_file_name']})
        allSubmissions.append({'user_id':user_id,'name':name,'submissions':submissionList})

    print(allSubmissions)

    
    return JsonResponse({
                'problems':problemArr,
                'submissions': allSubmissions,
            })

@instructor1_required
def download_auto_csv(request, sec_user_id, assign_id):
    try:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="AutoEvaluationAssign'+assign_id+'.csv"'
        writer = csv.writer(response)

        cursor = connection.cursor()
        cursor.execute('''select user_id,name from "user" where user_id in (select user_id from sec_user where sec_id in (select sec_id from sec_user where id=%s) and role='Student')''',[sec_user_id])
        userArr = dictfetchall(cursor)


        cursor = connection.cursor()
        cursor.execute('''select problem_no from problem where assignment_id=%s order by problem_no''',[assign_id])
        problemArr = dictfetchall(cursor)

        print(problemArr)

        head = ['#','User ID','Name']

        for p in problemArr:
            head.append("Problem "+ str(p['problem_no']))

        writer.writerow(head)

        cursor = connection.cursor()
        cursor.execute(
            '''with A as (select * from problem where assignment_id=%s),B as (select * from "user" where user_id in (select user_id from sec_user where sec_id in (select sec_id from sec_user where id=%s) and role='Student')),C as (select user_id,problem_id,final_submission_no as sub_no from user_submissions where problem_id in (select problem_id from A)),D as (select * from submission where (user_id,problem_id,sub_no) in (select * from C)),E as (select user_id,name,problem_id,problem_no from A,B) select user_id,name,problem_no,marks_auto from E natural left outer join D order by problem_no''',
            [assign_id, sec_user_id])
        submissionArr = dictfetchall(cursor)

        allSubmissions = []

        i = 0
        for user in userArr:
            i=i+1
            user_id = user['user_id']
            name = user['name']
            submissionList = [i,user_id,name]
            for elt in submissionArr:
                if elt['user_id'] == user_id:
                    submissionList.append(elt['marks_auto'])
            writer.writerow(submissionList)
    except:
        print(traceback.format_exc())
        response = HttpResponse("")
        response['Content-Disposition'] = 'attachment; filename=' + "null"
    return(response)


@instructor1_required
def upload_inst_csv(request, sec_user_id, assign_id):
    if request.method == 'POST':
        file = request.FILES['inst_csv_file']
        decoded_file = file.read().decode('utf-8').splitlines()
        reader = csv.reader(decoded_file)
        for row in reader:
            print(row)
    return render('sedb:user_home')