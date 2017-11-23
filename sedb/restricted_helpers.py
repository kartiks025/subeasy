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


@instructor1_required
def edit_assign_home(request, sec_user_id, assign_id):
    print("edit_assign_home called")
    assignment_id = 0
    if request.method == 'POST':
        assign_num = request.POST['assign_num']
        title = request.POST['assign_title']
        visibility = request.POST['visibility']
        pub_time = request.POST['pub_time']
        soft_deadline = request.POST['soft_deadline']
        hard_deadline = request.POST['hard_deadline']
        freeze_deadline = request.POST['freeze_deadline']
        crib_deadline = request.POST['crib_deadline']
        description = request.POST['description']

        section = SecUser.objects.get(id=sec_user_id).sec
        if assign_id == '0':
            print("New Assignment")
            try:
                helper_file = request.FILES['helper_file'].file.read()
                helper_file_name = request.FILES['helper_file'].name
            except Exception:
                helper_file = None
                helper_file_name = ""
            deadline = Deadline(soft_deadline=soft_deadline, hard_deadline=hard_deadline,
                                freezing_deadline=freeze_deadline)
            deadline.save()
            assignment = Assignment(assignment_no=assign_num, title=title, description=description,
                                    publish_time=pub_time, visibility=(visibility == '1'), crib_deadline=crib_deadline,
                                    sec=section, num_problems=0, deadline=deadline, helper_file=helper_file,
                                    helper_file_name=helper_file_name)

            assignment.save()
            assignment_id = assignment.assignment_id
        else:
            try:
                assignment = Assignment.objects.get(assignment_id=assign_id)
                assignment.assignment_no = assign_num
                assignment.title = title
                assignment.visibility = (visibility == '1')
                assignment.publish_time = pub_time
                assignment.deadline.soft_deadline = soft_deadline
                assignment.deadline.hard_deadline = hard_deadline
                assignment.deadline.freezing_deadline = freeze_deadline
                assignment.description = description
                try:
                    print("try")
                    assignment.helper_file = request.FILES['helper_file'].file.read()
                    assignment.helper_file_name = request.FILES['helper_file'].name
                    print("try1")
                except Exception:
                    print("except")
                assignment.deadline.save()
                assignment.save()
                assignment_id = assignment.assignment_id
            except ObjectDoesNotExist:
                print("assignment doesn't exist")
                # do something

        print(sec_user_id)
        print(assign_num)
        print(title)
        print(visibility)
        print(pub_time)
        print(soft_deadline)
        print(hard_deadline)
        print(freeze_deadline)
        print(crib_deadline)
        print(description)

    return JsonResponse({
        'r_id': assignment_id
    })


@instructor_required
def get_students(request, sec_user_id):
    sec_user = SecUser.objects.get(id=sec_user_id);
    stu = SecUser.objects.filter(sec_id=sec_user.sec_id, role="Student")
    student = [{'id': a.user.user_id, 'name': a.user.name} for a in stu]

    cursor = connection.cursor()
    cursor.execute(
        '''select user_id,name from "user" where user_id not in (select user_id from sec_user where sec_id=%s);''',
        [sec_user.sec_id])
    users = dictfetchall(cursor)

    context = {'user': users, 'student': student}
    return JsonResponse(context, content_type="application/json")


@instructor_required
def get_tas(request, sec_user_id):
    sec_user = SecUser.objects.get(id=sec_user_id);
    teach = SecUser.objects.filter(sec_id=sec_user.sec_id, role="TA")
    ta = [{'id': a.user.user_id, 'name': a.user.name} for a in teach]

    cursor = connection.cursor()
    cursor.execute(
        '''select user_id,name from "user" where user_id not in (select user_id from sec_user where sec_id=%s);''',
        [sec_user.sec_id])
    users = dictfetchall(cursor)

    context = {'user': users, 'ta': ta}
    return JsonResponse(context, content_type="application/json")


@instructor1_required
def get_new_prob_no(request, sec_user_id, assign_id):
    assignment = Assignment.objects.get(assignment_id=assign_id)
    assignment.num_problems += 1
    assignment.save()
    return JsonResponse({
        'problem_no': assignment.num_problems
    })


@instructor2_required
def edit_assign_prob(request, sec_user_id, assign_id, prob_id):
    print("edit_assign_prob called")
    problem_id = 0
    assignment = Assignment.objects.get(assignment_id=assign_id)
    problem = None
    if request.method == "POST":
        prob_num = request.POST['prob_num']
        prob_title = request.POST['prob_title']
        description = request.POST['description']
        sol_visibility = (request.POST['sol_visibility'] == '1')
        files_to_submit = request.POST['files_to_submit']
        compile_cmd = request.POST['compile_cmd']
        resources_spec = False

        try:
            cpu_time = request.POST['cpu_time']
            clock_time = request.POST['clock_time']
            memory_limit = request.POST['memory_limit']
            stack_limit = request.POST['stack_limit']
            open_files = request.POST['open_files']
            max_filesize = request.POST['max_filesize']

            resources_spec = True
        except KeyError:
            print("keyError")

        if prob_id == '0':
            print("New problem")
            try:
                helper_file = request.FILES['helper_file'].file.read()
                helper_file_name = request.FILES['helper_file'].name
            except Exception:
                helper_file = None
                helper_file_name = ""
            try:
                solution_file = request.FILES['solution_file'].file.read()
                solution_file_name = request.FILES['solution_file'].name
            except Exception:
                solution_file = None
                solution_file_name = ""

            if resources_spec:
                resource = ResourceLimit(cpu_time=cpu_time, clock_time=clock_time, memory_limit=memory_limit,
                                         stack_limit=stack_limit, open_files=open_files, max_filesize=max_filesize)
                resource.save()
            else:
                resource = ResourceLimit.objects.get(resource_limit_id=1)
            problem = Problem(problem_no=prob_num, title=prob_title, description=description,
                              compile_cmd=compile_cmd, sol_visibility=sol_visibility, assignment=assignment,
                              resource_limit=resource, num_testcases=0, files_to_submit=files_to_submit,
                              helper_file=helper_file, solution_file=solution_file, helper_file_name=helper_file_name,
                              solution_filename=solution_file_name)
            problem.save()
            problem_id = problem.problem_id
        else:
            problem = Problem.objects.get(problem_id=prob_id)
            resource = problem.resource_limit
            print(resource.resource_limit_id)
            if resources_spec:
                print("changing resource")
                if resource.resource_limit_id != 1:
                    resource.cpu_time = cpu_time
                    resource.clock_time = clock_time
                    resource.memory_limit = memory_limit
                    resource.stack_limit = stack_limit
                    resource.open_files = open_files
                    resource.max_filesize = max_filesize
                    resource.save()
                else:
                    resource = ResourceLimit(cpu_time=cpu_time, clock_time=clock_time, memory_limit=memory_limit,
                                             stack_limit=stack_limit, open_files=open_files, max_filesize=max_filesize)
                    resource.save()

            problem.problem_no = prob_num
            problem.title = prob_title
            problem.description = description
            problem.compile_cmd = compile_cmd
            problem.sol_visibility = sol_visibility
            problem.assignment = assignment
            problem.resource_limit = resource
            problem.files_to_submit = files_to_submit

            try:
                problem.helper_file = request.FILES['helper_file'].file.read()
                problem.helper_file_name = request.FILES['helper_file'].name
            except Exception:
                print("except")

            try:
                problem.solution_file = request.FILES['solution_file'].file.read()
                problem.solution_filename = request.FILES['solution_file'].name
            except Exception:
                print("except")
            problem.save()
            problem_id = problem.problem_id

            try:
                print("testcase file")
                testcase_file = tarfile.open(fileobj=request.FILES['testcase_file'])
                print(type(testcase_file))

                in_pat = re.compile('in.*?([0-9]+)')
                out_pat = re.compile('out.*?([0-9]+)')

                in_file_dict = {}
                out_file_dict = {}
                for member in testcase_file.getmembers():
                    print(member.name)
                    if member.isfile():
                        mem_name = member.name.split('/')[-1]
                        in_lst = in_pat.findall(mem_name)
                        if len(in_lst) > 0:
                            in_file_dict[int(in_lst[-1])] = member
                        else:
                            out_list = out_pat.findall(mem_name)
                            if len(out_list) > 0:
                                out_file_dict[int(out_list[-1])] = member

                Testcase.objects.filter(problem_id=problem_id).delete()
                print()
                print()
                print()
                print()
                print("testcases")
                print()
                print(in_file_dict)
                print(out_file_dict)
                print()

                print()
                print()
                print()
                print()

                print(type(in_file_dict))
                for key, val in in_file_dict.items():
                    print(key)
                    try:
                        out_member = out_file_dict[key]
                        if problem is not None:
                            testcase = Testcase(problem=problem, testcase_no=key,
                                                marks=1, visibility=False,
                                                infile_name=val.name.split('/')[-1],
                                                infile=testcase_file.extractfile(val).read(),
                                                outfile_name=out_member.name.split('/')[-1],
                                                outfile=testcase_file.extractfile(out_member).read())
                            testcase.save()
                    except:
                        pass
                testcase_file.close()
            except:
                print("Exception")

    return JsonResponse({
        'r_id': problem_id
    })
