function loadHome(){
    var url = $("#detailsForm").attr('data-loadUrl');
    $.get(url,
    function(data, status){
        if(status == "success"){
            if (!data.new_assign){
                var obj = data.assign;
                var deadline = data.deadline;
                $("#assign_num").val(obj.assignment_no);
                $("#title").val(obj.title);
                if(obj.visibility == "1"){
                    $("#visible").attr('checked',true);
                }
                else{
                    $("#hidden").attr('checked',true);
                }
                $("#pub_time").val(obj.publish_time);
                $("#soft_deadline").val(deadline.soft_deadline);
                $("#hard_deadline").val(deadline.hard_deadline);
                $("#freeze_deadline").val(deadline.freezing_deadline);
                $("#crib_deadline").val(obj.crib_deadline);
                $("#description").val(obj.description);
            }
        }
        else{
            console.log("Some Error Occurred");
        }
    });
}

function updateProblem(problem_id, prob_obj, resource_obj,testcase_obj){
    $("#link"+problem_id).text("Problem "+prob_obj.problem_no);
    var prob_id = "#prob" + problem_id;
    $(prob_id+" input[name=prob_num]").val(prob_obj.problem_no);
    $(prob_id+" input[name=prob_title]").val(prob_obj.title);
    $(prob_id+" textarea[name=description]").val(prob_obj.description);
    $(prob_id+" input[name=files_to_submit]").val(prob_obj.files_to_submit);
    $(prob_id+" input[name=compile_cmd]").val(prob_obj.compile_cmd);
    $(prob_id+" input[sol_visibility][value="+prob_obj.sol_visibility+"]").attr('checked',true);

    $(prob_id+" input[name=cpu_time]").val(resource_obj.cpu_time);
    $(prob_id+" input[name=clock_time]").val(resource_obj.clock_time);
    $(prob_id+" input[name=memory_limit]").val(resource_obj.memory_limit);
    $(prob_id+" input[name=stack_limit]").val(resource_obj.stack_limit);
    $(prob_id+" input[name=open_files]").val(resource_obj.open_files);
    $(prob_id+" input[name=max_filesize]").val(resource_obj.max_filesize);

    var link = $(prob_id+" div[class=loadUrl]").attr('data-loadurl');
    link = link.replace("get_assign_prob","problem");
    console.log(link)

    $(prob_id+ ' tbody[name ="testcase_info"]').html("");

    for(var i in testcase_obj){
        var tr = '<tr/>';
        $(tr).append($('<td/>').append(
           testcase_obj[i].num        
        ).append($('<input/>',{
            "name" : "testcase_id",
            "type" : "hidden",
            value : testcase_obj[i].id

        }))).append($('<td/>').append($('<a/>',{
            href : link+"download_testcase_input_file/"+testcase_obj[i].num +"/",
            text : testcase_obj[i].infile_name
            
        }))).append($('<td/>').append($('<a/>',{
            href : link+"download_testcase_output_file/"+testcase_obj[i].num +"/",
            text : testcase_obj[i].outfile_name
            
        }))).append($('<td/>').append($('<input/>',{
            "name" : "visibility",
            "type" : "checkbox",
            "checked" : testcase_obj[i].visibility
        }))).append($('<td/>').append($('<input/>',{
            "name" : "marks",
            "type" : "number",
            value : testcase_obj[i].marks
        }))).appendTo($(prob_id+' tbody[name ="testcase_info"]'));
        
        
    }
    // console.log(testcase_obj);
    // console.log("Find Testcase object above");
}

function loadProblems(){
    // console.log("loadProblemsCalled");

    var url = $("#problemSubMenu").attr("data-loadUrl");
    $.get(url,
    function(data, status){
        if(status == "success"){
            $(".problems, .problems-link").remove();
            console.log(data);
            var ps = data.problems
            for(var i in ps){
                var prob_obj = ps[i].problem;
                console.log(prob_obj.title);
                appendProb(prob_obj.problem_id);
                var prob_id = "#prob"+prob_obj.problem_id;
                updateProblem(prob_obj.problem_id, prob_obj, ps[i].resource, ps[i].testcases);

                var s = $(prob_id+" .loadUrl").attr('data-loadUrl').replace('/0/','/'+prob_obj.problem_id+'/');
                $(prob_id+" .loadUrl").attr('data-loadUrl', s);
                s = $(prob_id+" form").attr('action').replace('/0/','/'+prob_obj.problem_id+'/');
                $(prob_id+" form").attr('action', s);
                // s = $(prob_id+" a[name=helper_file]").attr('href').replace('0',prob_obj.problem_id);
                // $(prob_id+" a[name=helper_file]").attr('href',s)
                
                // new algo of replacing 0
                x = $(prob_id+" a[name=helper_file]").attr('href').replace('/0/','/'+prob_obj.problem_id+'/');
                $(prob_id+" a[name=helper_file]").attr('href',x);

                x = $(prob_id+" a[name=solution_file]").attr('href').replace('/0/','/'+prob_obj.problem_id+'/');
                $(prob_id+" a[name=solution_file]").attr('href',x);
            }
        }
        else{
            console.log("Some Error Occurred");
        }
    });
}

function reloadProblem(elem){
    // console.log("reloadProblemsCalled");

    var url = elem.parent().parent().attr('data-loadUrl');
    $.get(url,
    function(data, status){
        if(status == "success"){
            var prob_id = data.problem.problem_id;
            updateProblem(prob_id, data.problem, data.resource, data.testcases);
        }
        else{
            console.log("Some Error Occurred");
        }
    });
}

function EditButtonClick(elem){
    // console.log("editButtonCalled");
    var pid = "#"+elem.parent().parent().parent().attr('id');
    var rval = $(pid+" input").prop('disabled');

    var elem = elem.find("> span");
    if (elem.hasClass('glyphicon-pencil')){
        elem.removeClass('glyphicon-pencil');
        elem.addClass('glyphicon-ok');

        $(pid+" input").attr('disabled',!rval);
        $(pid+" textarea").attr('disabled',!rval);
    }
    else{
        var frm = $(pid+" form");
        frm.validate();
        var formData = new FormData(frm[0]);
        // console.log(frm[0]);

        var tbId = pid+ ' tbody[name ="testcase_info"]';

        jsonObj = [];
        $(tbId).find('tr').each(function(){
            
            item ={};

            item["visibility"] = "off";
            var tableData = $(this).find('input');
            var tableArr =tableData.serializeArray();
            $(tableArr).each(function(i, field){
                 item[field.name] = field.value;
            });

            // var $tds = $(this).find('td');
            // item["testcase_id"] = $tds.eq(0).children("input").attr("value");
            // item["visibility"] = $tds.eq(3).children("input").attr("checked");
            // item["marks"] = $tds.eq(4).children("input").attr("value");

            jsonObj.push(item);
        });

        console.log(jsonObj);
        console.log(JSON.stringify(jsonObj));
        formData.append("testcases",JSON.stringify(jsonObj));
        // console.log(formData);

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

                    frm.attr('action',frm.attr('action').replace('0',data.r_id));
                    var div = frm.parent().parent();
                    div.attr('data-loadUrl',div.attr('data-loadUrl').replace('0',data.r_id));

                    if(data.to_redirect){
                        window.location.href=data.url;
                    }
                    else{
                        if(pid=="#details"){
                            loadHome();
                        }
                        else{
                            // console.log("reloadProblemCalled1");
                            reloadProblem(elem);
                        }
                    }
                },
                error: function (data) {
                    console.log('An error occurred.');
                    console.log(data);
                },
            });

            elem.removeClass('glyphicon-ok');
            elem.addClass('glyphicon-pencil');

            $(pid+" input").attr('disabled',!rval);
            $(pid+" textarea").attr('disabled',!rval);
        }
    }
}

function SideNavClick(elem){
    var toShowDiv = elem.attr("href");
    if(elem.hasClass("problems-link")){
        console.log("problems-link clicked");
        reloadProblem($(toShowDiv+" form"));
    }
    else if(elem.attr('id') == "link-details"){
        loadHome();
    }

    $("#list-nav .active").toggleClass("active");
    $(this).parent().toggleClass("active");

    var vis = $("#content :visible");
    vis.addClass('hidden');

    $(toShowDiv).find("*").removeClass('hidden');
    $(toShowDiv).removeClass('hidden');
}


function appendProb(problem_no){
    $('<li/>').append($('<a/>',{
        id : "link"+problem_no,
        href : "#prob"+problem_no,
        "class" : "side-nav-link problems-link",
        text : "Problem "+problem_no,
        on : {
            click : function(){
                SideNavClick($(this));
            }
        }
    })).insertBefore($("#add-button"));

//    var vis = $("#content :visible");
//    vis.addClass('hidden');

    $('<div/>',{
        id: "prob"+problem_no,
        "class" : "panel panel-primary nav-content problems hidden",
        html : $("#problem-form").html()
    }).appendTo($("#content"));

    $("#prob"+problem_no+" .edit-btn").on("click", function(){
        EditButtonClick($(this));
    });

//    $("#list-nav .active").toggleClass("active");
//    $("#link"+problem_no).parent().toggleClass("active");
}

function addNewProblem(url){
    var problem_no = $("#problemSubMenu").children().length;
    appendProb(problem_no);
}
