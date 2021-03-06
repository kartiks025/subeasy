function loadHome(url){
    $.get(url,
    function(data, status){
        if(status == "success"){
            var obj = data.assign;
            var deadline = data.deadline;
            $("#assign_num").text(obj.assignment_no);
            $("#title").text(obj.title);
            $("#helper_file").text(obj.helper_file_name);
            $("#pub_time").text(formatDate(obj.publish_time));
            $("#soft_deadline").text(formatDate(deadline.soft_deadline));
            $("#hard_deadline").text(formatDate(deadline.hard_deadline));
            $("#freeze_deadline").text(formatDate(deadline.freezing_deadline));
            $("#crib_deadline").text(formatDate(obj.crib_deadline));
            $("#description").text(obj.description);
            loadProblems();
        }
        else{
            console.log("Some Error Occurred");
        }
    });
}

function loadProblems(){
    var url = $("#problemSubMenu").attr("data-loadUrl");
    $.get(url,
    function(data, status){
        if(status == "success"){
            $(".problems, .problems-link").remove();
            console.log(data);
            var ps = data.problems
            for(var i in ps){
                var prob_obj = ps[i].problem;
                appendProb(prob_obj.problem_id);
                var prob_id =prob_obj.problem_id;
                updateProblem(prob_id, prob_obj, ps[i].resource,ps[i].testcase,ps[i].hidden,ps[i].sol_visibility,ps[i].sub_file_name,ps[i].can_submit);
                console.log("#prob"+prob_id)
                var s = $("#prob"+prob_id).attr('data-loadUrl').replace('0',prob_id);
                $("#prob"+prob_id).attr('data-loadUrl', s);

                //new algo of replacing 0
                x = $("#prob"+prob_id+" a[name=helper_file]").attr('href')
                s = x.lastIndexOf("0");
                s = x.substr(0,s)+prob_obj.problem_id+x.substr(s+1,x.length-s-1);
                $("#prob"+prob_id+" a[name=helper_file]").attr('href',s)

                x = $("#prob"+prob_id+" a[name=solution_file]").attr('href')
                s = x.lastIndexOf("0");
                s = x.substr(0,s)+prob_obj.problem_id+x.substr(s+1,x.length-s-1);
                $("#prob"+prob_id+" a[name=solution_file]").attr('href',s)

                x = $("#prob"+prob_id+" a[name=all_testcases]").attr('href')
                s = x.lastIndexOf("0");
                s = x.substr(0,s)+prob_obj.problem_id+x.substr(s+1,x.length-s-1);
                $("#prob"+prob_id+" a[name=all_testcases]").attr('href',s)

                x = $("#prob"+prob_id+" a[name=download_submission]").attr('href')
                s = x.lastIndexOf("0");
                s = x.substr(0,s)+prob_obj.problem_id+x.substr(s+1,x.length-s-1);
                $("#prob"+prob_id+" a[name=download_submission]").attr('href',s)

                x = $("#prob"+prob_id+" form[name=submit_form]").attr('action')
                s = x.lastIndexOf("0");
                s = x.substr(0,s)+prob_obj.problem_id+x.substr(s+1,x.length-s-1);
                $("#prob"+prob_id+" form[name=submit_form]").attr('action',s)

                x = $("#prob"+prob_id+" form[name=evaluate_form]").attr('action')
                s = x.lastIndexOf("0");
                s = x.substr(0,s)+prob_obj.problem_id+x.substr(s+1,x.length-s-1);
                $("#prob"+prob_id+" form[name=evaluate_form]").attr('action',s)
            }
        }
        else{
            console.log("Some Error Occurred");
        }
    });
}

function reloadProblem(elem){
    var url = elem.attr('data-loadUrl');
    // alert(url);
    $.get(url,
    function(data, status){
        if(status == "success"){
            var prob_id = "#prob"+data.problem.problem_id;
            console.log("hi "+data.problem.problem_id)
            updateProblem(data.problem.problem_id, data.problem, data.resource,data.testcases,data.hidden, data.sol_visibility,data.sub_file_name,data.can_submit);
        }
        else{
            console.log("Some Error Occurred");
        }
    });
}


function appendProb(problem_id){
    $('<li/>').append($('<a/>',{
        id : "link"+problem_id,
        href : "#prob"+problem_id,
        "class" : "side-nav-link problems-link",
        text : "Problem "+problem_id,
        on : {
            click : function(){
                SideAssignNavClick($(this));
            }
        }
    })).appendTo($("#problemSubMenu"));
    console.log($("#problem-form").attr('data-loadurl'));
    console.log("appending");
    $('<div/>',{
        id: "prob"+problem_id,
        "class" : "hidden problem",
        html : $("#problem-form").html(),
        "data-loadurl" : $("#problem-form").attr('data-loadurl')
    }).appendTo($("#content"));
}

function updateProblem(problem_id, prob_obj, resource_obj,testcases,hidden,sol_visibility,sub_file_name,can_submit){
    $("#link"+problem_id).text("Problem "+prob_obj.problem_no);
    var prob_id = '#prob' +problem_id;
    console.log(resource_obj);
    $(prob_id+' div[name="prob_name"]').text(prob_obj.problem_no+". "+prob_obj.title);
    $(prob_id+' div[name="description"]').text(prob_obj.description);
    $(prob_id+' span[name="files_to_submit"]').text(prob_obj.files_to_submit);
    $(prob_id+' span[name="compile_cmd"]').text(prob_obj.compile_cmd);
    $(prob_id+ ' span[name="cpu_time"]').text(resource_obj.cpu_time + " seconds");
    $(prob_id+ ' span[name ="clock_time"]').text(resource_obj.clock_time + " seconds");
    $(prob_id+ ' span[name ="memory_limit"]').text(resource_obj.memory_limit + " kB");
    $(prob_id+ ' span[name ="stack_limit"]').text(resource_obj.stack_limit + " kB");
    $(prob_id+ ' span[name ="open_files"]').text(resource_obj.open_files);
    $(prob_id+ ' span[name ="max_filesize"]').text(resource_obj.max_filesize + " kB");
    $(prob_id+ ' span[name ="max_filesize"]').text(resource_obj.max_filesize + " kB");

    $(prob_id+ ' a[name ="helper_file"]').text(prob_obj.helper_file_name);
    $(prob_id+ ' a[name ="download_submission"]').text(sub_file_name);
    if(!can_submit){
        $(prob_id+ ' input[name ="submission_file"]').prop('disabled', true);
    } else{
        $(prob_id+ ' input[name ="submission_file"]').prop('disabled', false);
    }


    console.log(sol_visibility)
    if(!sol_visibility){
        console.log("hide");
        $(prob_id+ ' div[class ="solution_file"]').hide();
    }
    else{
        console.log("show");
        $(prob_id+ ' div[class ="solution_file"]').show();
    }

    var link = $("#prob"+problem_id).attr('data-loadUrl');
    console.log(link)
    link = link.replace("get_user_assign_prob","problem");
    link = link.replace("assignments","assignment");
    console.log(link)
    s = link.lastIndexOf("0");
    s = link.substr(0,s)+prob_obj.problem_id+link.substr(s+1,link.length-s-1);
    var content = ""
    for(var i in testcases){
        if(testcases[i].error=='0')
            testcases[i].error="Output Matches"
        else if(testcases[i].error=='-1')
            testcases[i].error="Output Does Not Match"
        if(testcases[i].user_marks==null)
            content += "<tr><td>"+testcases[i].testcase_no+"</td><td><a a class=\"link\" href=\""+link+"download_testcase_input_file/"+testcases[i].testcase_no+"/\">"+testcases[i].infile_name+"</a></td><td><a a class=\"link\" href=\""+link+"download_testcase_output_file/"+testcases[i].testcase_no+"/\">"+testcases[i].outfile_name+"</a></td><td>"+testcases[i].marks+"</td><td>"+"0-Not Evaluated"+"</td><td>"+"Not evaluated"+"</td><td>Not Evaluated</td></tr>";
        else
            content += "<tr><td>"+testcases[i].testcase_no+"</td><td><a a class=\"link\" href=\""+link+"download_testcase_input_file/"+testcases[i].testcase_no+"/\">"+testcases[i].infile_name+"</a></td><td><a a class=\"link\" href=\""+link+"download_testcase_output_file/"+testcases[i].testcase_no+"/\">"+testcases[i].outfile_name+"</a></td><td>"+testcases[i].marks+"</td><td>"+testcases[i].user_marks+"</td><td>"+testcases[i].error+"</td><td><a class=\"link\" target=\"_blank\" href=\"/sedb/output_compare/"+testcases[i].id+"/\">Check Output</a></td></tr>";
    }
    $(prob_id+ ' tbody[name ="testcases"]').html(content);
    content = ""
    for(var i in hidden){
        if(hidden[i].user_marks==null)
            content += "<tr><td>"+hidden[i].testcase_no+"</td><td>"+hidden[i].marks+"</td><td>"+"0-Not Evaluated"+"</td></tr>"
        else
            content += "<tr><td>"+hidden[i].testcase_no+"</td><td>"+hidden[i].marks+"</td><td>"+hidden[i].user_marks+"</td></tr>"
    }
    $(prob_id+ ' tbody[name ="hidden"]').html(content);
    // $(prob_id+" input[sol_visibility][value="+prob_obj.sol_visibility+"]").attr('checked',true);
}

function updateTestcases(problem_id,testcases,hidden){
    var prob_id = '#prob' +problem_id;
    var link = $("#prob"+problem_id).attr('data-loadUrl');
    console.log(link)
    link = link.replace("get_user_assign_prob","problem");
    link = link.replace("assignments","assignment");
    console.log(link)
    s = link.lastIndexOf("0");
    s = link.substr(0,s)+problem_id+link.substr(s+1,link.length-s-1);
    var content = ""
    for(var i in testcases){
        if(testcases[i].error=='0')
            testcases[i].error="Output Matches"
        else if(testcases[i].error=='-1')
            testcases[i].error="Output Does Not Match"
        if(testcases[i].user_marks==null)
            content += "<tr><td>"+testcases[i].testcase_no+"</td><td><a class=\"link\" href=\""+link+"download_testcase_input_file/"+testcases[i].testcase_no+"/\">"+testcases[i].infile_name+"</a></td><td><a class=\"link\" href=\""+link+"download_testcase_output_file/"+testcases[i].testcase_no+"/\">"+testcases[i].outfile_name+"</a></td><td>"+testcases[i].marks+"</td><td>"+"0-Not Evaluated"+"</td><td>"+"Not evaluated"+"</td><td>Not Evaluated</td></tr>";
        else
            content += "<tr><td>"+testcases[i].testcase_no+"</td><td><a class=\"link\" href=\""+link+"download_testcase_input_file/"+testcases[i].testcase_no+"/\">"+testcases[i].infile_name+"</a></td><td><a class=\"link\" href=\""+link+"download_testcase_output_file/"+testcases[i].testcase_no+"/\">"+testcases[i].outfile_name+"</a></td><td>"+testcases[i].marks+"</td><td>"+testcases[i].user_marks+"</td><td>"+testcases[i].error+"</td><td><a class=\"link\" target=\"_blank\" href=\"/sedb/output_compare/"+testcases[i].id+"/\">Check Output</a></td></tr>";
    }
    $(prob_id+ ' tbody[name ="testcases"]').html(content);
    content = ""
    for(var i in hidden){
        if(hidden[i].user_marks==null)
            content += "<tr><td>"+hidden[i].testcase_no+"</td><td>"+hidden[i].marks+"</td><td>"+"0-Not Evaluated"+"</td></tr>"
        else
            content += "<tr><td>"+hidden[i].testcase_no+"</td><td>"+hidden[i].marks+"</td><td>"+hidden[i].user_marks+"</td></tr>"
    }
    $(prob_id+ ' tbody[name ="hidden"]').html(content);
}

function formatDate(date){
    var d = new Date(date)
    return d;
}

function SideAssignNavClick(elem){
    $("#list-nav .active").toggleClass("active");
    $(this).parent().toggleClass("active");

    var vis = $("#content :visible");
    vis.addClass('hidden');

    var toShowDiv = elem.attr("href");
    console.log(toShowDiv)
    $(toShowDiv).find("*").removeClass('hidden');
    $(toShowDiv).removeClass('hidden');
    if (String(toShowDiv)==("#submission")){
        console.log("yes")
        // window.history.pushState({"html":"","pageTitle":"Submission"},"", "submission/");
        $('#submission').load('submission #container');
    }   
    if (String(toShowDiv)==("#details")){
        loadHome();
    }
    if (String(toShowDiv).indexOf("#prob")!== -1){
        reloadProblem($(String(toShowDiv)));
    }

}

function UploadButtonClick(elem,img){
    var frm = elem.parent()
    frm.validate();
    var formData = new FormData(frm[0]);
    console.log(frm.serialize());
    console.log(formData);
    $("<img id=\"gif\" src=\""+img+"\" >").insertAfter(elem)
    if(frm.valid()){
        $.ajax({
            type: frm.attr('method'),
            url: frm.attr('action'),
            data: formData,
            contentType: false,
            processData: false,
            success: function (data) {
                $("#gif").remove();
                console.log('Submission was successful.');
                console.log(data);
                if(data.success){
                    // $("<p style=\"color: green\">Submitted Successfully<p>").insertAfter(elem);
                    (function (el) {
                        setTimeout(function () {
                            el.remove()
                        }, 5000);
                    }($("<p style=\"color: green\">"+data.message+"<p>").insertAfter(elem)));
                    $("#prob"+ data.problem_id+' a[name ="download_submission"]').text(data.sub_file_name);
                }
                else{
                    // $("<p style=\"color: red\">Submission error. Please check your file.y<p>").insertAfter(elem)
                    (function (el) {
                        setTimeout(function () {
                            el.remove()
                        }, 5000);
                    }($("<p style=\"color: red\">"+data.message+"</p>").insertAfter(elem)));
                }
                frm.trigger("reset");
            },
            error: function (data) {
                $("#gif").remove();
                console.log('An error occurred.');
                console.log(data);
                (function (el) {
                    setTimeout(function () {
                        el.remove()
                    }, 5000);
                }($("<p style=\"color: red\">Submission error. Please check your file</p>").insertAfter(elem)));
                frm.trigger("reset");
            },
        });
    }
}

function EvaluateButtonClick(elem,img){
    var frm = elem.parent()
    frm.validate();
    var formData = new FormData(frm[0]);
    console.log(frm.serialize());
    console.log(formData);
    console.log(frm.attr('action'));
    $("<img id=\"gif\" src=\""+img+"\" >").insertAfter(elem)
    if(frm.valid()){
        $.ajax({
            type: frm.attr('method'),
            url: frm.attr('action'),
            data: formData,
            contentType: false,
            processData: false,
            success: function (data) {
                console.log('Evaluation was successful.');
                console.log(data);
                $("#gif").remove();
                if(data.success){
                    // $("<p style=\"color: green\">"+data.testcases+"<p>").insertAfter(elem);
                    if(data.message!="Compilation Error"){
                        (function (el) {
                            setTimeout(function () {
                                el.remove()
                            }, 2000);
                        }($("<p style=\"color: green\">"+"See Results Above"+"<p>").insertAfter(elem)));
                    }
                    else{
                        (function (el) {
                            setTimeout(function () {
                                el.remove()
                            }, 10000);
                        }($("<p style=\"color: red\">"+"Compilation Error"+"<p>").insertAfter(elem)));
                    }
                    updateTestcases(data.problem_id,data.testcases,data.hidden);
                }
                else{
                    // $("<p style=\"color: red\">Evaluation error. Please evaluate again.<p>").insertAfter(elem);
                    (function (el) {
                        setTimeout(function () {
                            el.remove()
                        }, 2000);
                    }($("<p style=\"color: red\">Evaluation error. No file Submitted.<p>").insertAfter(elem)));
                }
                frm.trigger("reset");
            },
            error: function (data) {
                $("#gif").remove();
                console.log('An error occurred.');
                console.log(data);
                (function (el) {
                    setTimeout(function () {
                        el.remove()
                    }, 2000);
                }($("<p style=\"color: red\">Evaluation error. Please evaluate again.<p>").insertAfter(elem)));
                frm.trigger("reset");
            },
        });
    }
}

function loadMarks(){
    var url = $("#marksheet").attr('data-loadUrl');

    console.log(url);
    $.get(url,
    function(data, status){
        var content="";
        console.log(data);
        if(status == "success"){
            for (var i in data.problems){
                console.log(i);
                content += "<tr><td>Problem "+data.problems[i].problem_id+"</td><td>"+data.problems[i].count+"</td><td>"+data.problems[i].marks_inst+"</td></tr>";
            }
            $("#marksheet"+ ' tbody[name ="marks-row"]').html(content);
        }
    });

}

function loadProbCrib(elem,prob){
    var content = "";
    if($.isEmptyObject(prob.crib)){
        content = $('<div/>',{
            'class' : "container",
            html : $("#crib-form-div").html(),
        });
        var frm = content.find("form");
        var url = frm.attr('action');
        frm.attr('action',url.replace('/0/','/'+prob.prob_id+'/'));
    }
    else{
        content = $('<div/>',{
            'class' : "container",
            html : $("#crib-comment-div").html(),
        });
        var frm = content.find("form");
        var url = frm.attr('action');
        frm.attr('action',url.replace('/0/','/'+prob.crib.crib_id+'/'));

        content.find('.crib-text').html(prob.crib.timestamp+'<br>'+prob.crib.text);

        for(var c in prob.crib.comments){
            content.find('ul').append($('<li/>',{
                html : prob.crib.comments[c].user_id+','+prob.crib.comments[c].timestamp+'<br>'+prob.crib.comments[c].text
            }));
        }
    }
    elem.append(content);
}

function loadCribs(){
    console.log("loadCribs called");
    var url = $("#cribs").attr('data-loadUrl');
    $.get(url,
    function(data, status){
        console.log(data);
        if(status == "success"){
            $('#problem-crib-content').empty();
            $('#problem-crib-tab').empty();
            for (var i in data.crib){
                var prob = data.crib[i];
                console.log(prob);

                $('#problem-crib-content').append($('<div/>',{
                    id: "crib-problem-"+prob.prob_id,
                    'class' : 'tab-pane fade in'
                }));

                $('#problem-crib-tab').append($('<li/>').append($('<a/>',{
                    'data-toggle' : "tab",
                    href : "#crib-problem-"+prob.prob_id,
                    text : "Problem"+prob.prob_num,
                    'class' : ""
                })));
            }
            for (var i in data.crib){
                var prob = data.crib[i];
                console.log(prob);

                var elem = $("#"+"crib-problem-"+prob.prob_id);
                loadProbCrib(elem,prob);
            }
            if($('#problem-crib-content').children().length > 0){
                $('#problem-crib-tab>:first-child').addClass('active');
                $('#problem-crib-content>:first-child').addClass('active');
            }
            $('#problem-crib-content .crib-post-btn').on('click',function(){
                postCrib($(this));
            });
        }
    });
}

function postCrib(elem){
    var frm = elem.parent().parent().find("form");
    var url = frm.attr('action');
    var formData = new FormData(frm[0]);
    console.log("postCribs"+url);
    frm.validate();

    if(frm.valid()){
        $.ajax({
            type: frm.attr('method'),
            url: frm.attr('action'),
            data: formData,
            contentType: false,
            processData: false,
            success: function (data) {
                console.log('Submission was successful.');
                console.log(data);
                loadCribs();
            },
            error: function (data) {
                console.log('An error occurred.');
                console.log(data);
            },
        });
    }

}
