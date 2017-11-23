function loadHome(url){
    $.get(url,
    function(data, status){
        if(status == "success"){
            var obj = data.assign;
            var deadline = data.deadline;
            $("#assign_num").text(obj.assignment_no);
            $("#title").text(obj.title);
            var d = new Date(obj.publish_time)
            $("#pub_time").text(formatDate(obj.publish_time));
            console.log(obj.publish_time);
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
                updateProblem(prob_id, prob_obj, ps[i].resource,ps[i].testcases);
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
    alert(url);
    $.get(url,
    function(data, status){
        if(status == "success"){
            var prob_id = "#prob"+data.problem.problem_id;
            console.log("hi "+data.problem.problem_id)
            updateProblem(data.problem.problem_id, data.problem, data.resource,data.testcases);
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

function updateProblem(problem_id, prob_obj, resource_obj,testcases){
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
    var link = $("#prob"+problem_id).attr('data-loadUrl');
    console.log(link)
    link = link.replace("get_user_assign_prob","problem");
    link = link.replace("assignments","assignment");
    console.log(link)
    s = link.lastIndexOf("0");
    s = link.substr(0,s)+prob_obj.problem_id+link.substr(s+1,link.length-s-1);
    var content = ""
    for(var i in testcases){
        // content += "<tr><td>"+testcases[i].testcase_no+"</td><td><a href=\""+link+"download_testcase_input_file/"+testcases[i].testcase_no+"/\">"+testcases[i].infile_name+"</a></td><td><a href=\""+link+"download_testcase_output_file/"+testcases[i].testcase_no+"/\">"+testcases[i].outfile_name+"</a></td><td>"+testcases[i].marks+"</td></tr>"
        content += "<tr><td>"+testcases[i].testcase_no+"</td><td><a href=\""+link+"download_testcase_input_file/"+testcases[i].testcase_no+"/\">"+testcases[i].infile_name+"</a></td><td><a href=\""+link+"download_testcase_output_file/"+testcases[i].testcase_no+"/\">"+testcases[i].outfile_name+"</a></td><td>"+testcases[i].marks+"</td><td>"+testcases[i].user_marks+"</td><td>"+testcases[i].error+"</td><td><a target=\"_blank\" href=\"/sedb/output_compare/"+testcases[i].id+"/\">Check Output</a></td></tr>"
    }
    $(prob_id+ ' tbody[name ="testcases"]').html(content);
    // $(prob_id+" input[sol_visibility][value="+prob_obj.sol_visibility+"]").attr('checked',true);
}

function updateTestcases(problem_id,testcases){
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
        console.log(testcases[i].id)
        console.log(testcases[i].testcase_id)
        // content += "<tr><td>"+testcases[i].testcase_no+"</td><td><a href=\""+link+"download_testcase_input_file/"+testcases[i].testcase_no+"/\">"+testcases[i].infile_name+"</a></td><td><a href=\""+link+"download_testcase_output_file/"+testcases[i].testcase_no+"/\">"+testcases[i].outfile_name+"</a></td><td>"+testcases[i].marks+"</td></tr>"
        content += "<tr><td>"+testcases[i].testcase_no+"</td><td><a href=\""+link+"download_testcase_input_file/"+testcases[i].testcase_no+"/\">"+testcases[i].infile_name+"</a></td><td><a href=\""+link+"download_testcase_output_file/"+testcases[i].testcase_no+"/\">"+testcases[i].outfile_name+"</a></td><td>"+testcases[i].marks+"</td><td>"+testcases[i].user_marks+"</td><td>"+testcases[i].error+"</td><td><a target=\"_blank\" href=\"/sedb/output_compare/"+testcases[i].id+"/\">Check Output</a></td></tr>"
    }
    $(prob_id+ ' tbody[name ="testcases"]').html(content);
    // $(prob_id+" input[sol_visibility][value="+prob_obj.sol_visibility+"]").attr('checked',true);
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

function UploadButtonClick(elem){
    var frm = elem.parent()
    frm.validate();
    var formData = new FormData(frm[0]);
    console.log(frm.serialize());
    console.log(formData);
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
                if(data.success){
                    // $("<p style=\"color: green\">Submitted Successfully<p>").insertAfter(elem);
                    (function (el) {
                        setTimeout(function () {
                            el.remove()
                        }, 2000);
                    }($("<p style=\"color: green\">Submitted Successfully<p>").insertAfter(elem)));
                }
                else{
                    // $("<p style=\"color: red\">Submission error. Please check your file.y<p>").insertAfter(elem)
                    (function (el) {
                        setTimeout(function () {
                            el.remove()
                        }, 2000);
                    }($("<p style=\"color: red\">Submission error. Please check your file</p>").insertAfter(elem)));
                }
                frm.trigger("reset");
            },
            error: function (data) {
                console.log('An error occurred.');
                console.log(data);
                (function (el) {
                    setTimeout(function () {
                        el.remove()
                    }, 2000);
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
                console.log('Submission was successful.');
                console.log(data);
                $("#gif").remove();
                if(data.success){
                    // $("<p style=\"color: green\">"+data.testcases+"<p>").insertAfter(elem);
                    (function (el) {
                        setTimeout(function () {
                            el.remove()
                        }, 2000);
                    }($("<p style=\"color: green\">"+"See Results Above"+"<p>").insertAfter(elem)));
                    if(data.message!="Compilation Error")
                        updateTestcases(data.problem_id,data.testcases);
                }
                else{
                    // $("<p style=\"color: red\">Evaluation error. Please evaluate again.<p>").insertAfter(elem);
                    (function (el) {
                        setTimeout(function () {
                            el.remove()
                        }, 2000);
                    }($("<p style=\"color: red\">Evaluation error. Please evaluate again.<p>").insertAfter(elem)));
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