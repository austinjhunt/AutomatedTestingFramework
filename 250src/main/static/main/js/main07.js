$(document).ready(function()
{
    $(window).on('resize', function()
    {
        var win = $(this); //this = window

        if (win.width() < 820)
        {
            newSize = win.width()/820 * 24;

            $("#logo_text").css("font-size", newSize.toString() + "px");
        }
        else
        {
            $("#logo_text").html('For <span style="color: indianred;">Students</span>. By <span style="color: green;">Students</span>.')
        }
    });

    $("textarea").keydown(function(e)
    {
        if(e.keyCode === 9) {
            // tab was pressed
            // get caret position/selection
            var start = this.selectionStart;
            var end = this.selectionEnd;

            var $this = $(this);
            var value = $this.val();

            // set textarea value to: text before caret + tab + text after caret
            $this.val(value.substring(0, start)
                + "\t"
                + value.substring(end));

            // put caret at right position again (add one for the tab)
            this.selectionStart = this.selectionEnd = start + 1;

            // prevent the focus lose
            e.preventDefault();
        }
    });

    $("#login-pass").keydown(function(e)
    {
        if(e.keyCode === 13)
        {
            cosfc_login();
        }

    });


    $(".answer_area_input").keyup(function(e)
    {
        curr_list = e.currentTarget.id.split('_');
        question_id = curr_list[curr_list.length-1];

        button_after = document.getElementById("check_answer_button_" + question_id);

        if(e.which == 13)
        {
            checkAnswerInput1(question_id, button_after);
            e.preventDefault();
        }
    });

    $(document).keypress(function(e)
    {
        if(e.which == 13 )
        {
            if (canGoToNext)
            {
                curr_list = quizOpen_id.split('_');
                only_id = curr_list[curr_list.length-1];
                goToNextQuestion(only_id);
            }

            //if ($('#cc_input').length == 1)
            //    return;

            //console.log("enter page triggered!");

            //insert_after($('#main_div').children().last());
            //console.log("Before focus");
            //$('#cc_input').focus();
            //console.log("After focus");
        }
    });
});

// New stuff begin
//

function saveQuestion(e, question_id)
{
    var d = new Date();
    var date_formatted = d.getFullYear() + "-" +
        ("00" + (d.getMonth() + 1)).slice(-2) + "-" +
        ("00" + d.getDate()).slice(-2) + " " +
        ("00" + d.getHours()).slice(-2) + ":" +
        ("00" + d.getMinutes()).slice(-2) + ":" +
        ("00" + d.getSeconds()).slice(-2);

    $(e).prop('disabled', true);

    var all_div_content = $($("#id_" + question_id).html()).children();

    var new_div = all_div_content[1].innerHTML + all_div_content[2].innerHTML;

    var answer_div = '<div style="width: 100%; text-align: center; padding-top: 20px; margin-bottom: 20px; border-top: 1px lightgrey solid;">' + $(all_div_content[4]).children()[0].outerHTML + $(all_div_content[4]).children()[1].outerHTML + '</div>';

    new_div = new_div + answer_div;

    $.ajax(
        {
            type: "POST",

            data: {
                btnType: 'save_question_student',
                all_div_content: new_div,
                date_time: date_formatted,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (data)
            {
                $("#modal_feedback").modal("show");

                setTimeout(function()
                {
                    $("#modal_feedback").modal("hide");
                }, 1500);
            }
        });
}


//New stuff 10/30

function delete_saved_question_student(question_id)
{
    $("body").prepend("<div id=\"new_overlay\"></div>");

    $("#new_overlay").css({
        "position": "absolute",
        "background-color": "grey",
        //"width": $(document).width(),
        //"height": $(document).height(),
        "z-index": 99990,
        "opacity": .5,
    });

    $("#new_loader").css({
        "position": "absolute",
        "z-index": 99999,
        "display": "block",
        "visibility": "visible",
    });

    console.log(question_id)
    $.ajax(
        {
            type: "POST",

            data: {
                btnType: 'delete_saved_question_student',
                question_id: question_id,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (data)
            {
                //

                location.reload();
                //$("#new_overlay").remove();


                /* $("#modal_feedback").modal("show");

                 setTimeout(function()
                 {
                 $("#modal_feedback").modal("hide", function ()
                 {
                 location.reload();
                 });
                 }, 1500);*/

            }
        });


}

function create_topic(week_id)
{
    console.log(week_id);

    window.event.stopPropagation();
}

function display_inside(week_id)
{
    if  ($("#" + week_id + "_inside_id").css('display') == 'block')
    {
        $("#" + week_id + "_inside_id").css({'display': 'none'});
        return;
    }


    $("#" + week_id + "_inside_id").css({"display": "block"});
    $("#" + week_id + "_inside_id").html('');
    $("#" + week_id + "_inside_id").append("<button class='btn-success' style='font-size: large; padding: 10px; margin: 5px;' onclick='create_topic(\"" + week_id + "\");'>Add New Topic</button>");
    $("#" + week_id + "_inside_id").append("<button class='btn-success' style='font-size: large; padding: 10px; margin: 5px;'>Add Existing Topic</button>");
    $("#" + week_id + "_inside_id").append("<button class='btn-success' style='font-size: large; padding: 10px; margin: 5px;'>Delete Topic</button>");
    // Ajax to retrieve topics from week
    //
    $.ajax(
        {
            type: "POST",

            data: {
                btnType: 'get_topics',
                week_id: week_id,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (data)
            {
                for (var i = 0; i < data['all_topics_sent'].length; i++)
                {
                    $("#" + week_id + "_inside_id").append("<div style='background-color: aquamarine; border: 1px lightgrey solid; margin: 10px; font-size: x-large; padding: 10px; cursor: pointer;' onclick='display_inside(\"" + data['all_topics_sent'][i].id + "\")'>" + data['all_topics_sent'][i].title + "<div id='" + data['all_topics_sent'][i].id + "_inside_topic_id' style='display: none; text-align: left;'><button class='btn-success' style='font-size: large; padding: 10px;'>Add Topic</button></div></div>");
                    $("#" + week_id + "_inside_id").append("<button class='btn-success' style='font-size: large; padding: 10px; margin: 5px;'>Add New Topic</button>");
                    $("#" + week_id + "_inside_id").append("<button class='btn-success' style='font-size: large; padding: 10px; margin: 5px;'>Add Existing Topic</button>");
                    $("#" + week_id + "_inside_id").append("<button class='btn-success' style='font-size: large; padding: 10px; margin: 5px;'>Delete Topic</button>");
                }
            }
        });
}

function fetch_weeks(semester)
{
    $.ajax(
        {
            type: "POST",

            data: {
                btnType: 'get_weeks',
                semester: semester,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (data)
            {
                $("#all_weeks").html('');
                for (var i = 0; i < data['all_weeks_sent'].length; i++)
                {
                    $("#all_weeks").append("<div style='background-color: whitesmoke; border: 1px lightgrey solid; margin: 10px; font-size: x-large; padding: 10px; cursor: pointer;' onclick='display_inside(\"" + data['all_weeks_sent'][i].id + "\")'>" + data['all_weeks_sent'][i].title + "<div id='" + data['all_weeks_sent'][i].id + "_inside_id' style='display: none; text-align: left;'></div></div>");
                }
            }
        });
}

//
// New stuff end

var canGoToNext = false;

var allQuestions;

var quizOpen = false;
var quizOpen_id = '';

var correctAnswer = '';
var nextQuestionIndex = 0;

function expandHeight(e)
{
    e.style.height = "1px";
    e.style.height = (e.scrollHeight)+"px";
}

function goToNextQuestion(quizID)
{
    canGoToNext = false;

    $("#questionArea_id_" + quizID).html(allQuestions[nextQuestionIndex]['question']);
    correctAnswer = allQuestions[nextQuestionIndex]['correct_answer']

    $("#correctAnsMessage_id_" + quizID).css({"display": "none"});
    $("#incorrectAnsMessage_id_" + quizID).css({"display": "none"});

    $("#goToNext_id_" + quizID).css({"display": "none"});
    $("#save_id_" + quizID).css({"display": "none"});

    $("#save_id_" + quizID).prop('disabled', false);

    //$("#addToFavorites_id_" + quizID).css({"display": "none"});

    $("#answer_no_eval_id_" + quizID).css({"display": "none"});

    if (allQuestions[nextQuestionIndex]['type'] == 'no_input')
    {
        $("#check_answer_button_" + quizID).prop('disabled', false);
    }

    else if (allQuestions[nextQuestionIndex]['type'] == 'multiple4')
    {
        $("#multiple4_area_1_id_" + quizID).css({"display": "block"});
        $("#multiple4_area_2_id_" + quizID).css({"display": "block"});

        $("#input1_area_id_" + quizID).css({"display": "none"});

        $("#answer1Area_id_" + quizID).prop('disabled', false);
        $("#answer2Area_id_" + quizID).prop('disabled', false);
        $("#answer3Area_id_" + quizID).prop('disabled', false);
        $("#answer4Area_id_" + quizID).prop('disabled', false);

        $("#answer1Area_id_" + quizID).text(allQuestions[nextQuestionIndex]['all_candidates'][0]);
        $("#answer2Area_id_" + quizID).text(allQuestions[nextQuestionIndex]['all_candidates'][1]);
        $("#answer3Area_id_" + quizID).text(allQuestions[nextQuestionIndex]['all_candidates'][2]);
        $("#answer4Area_id_" + quizID).text(allQuestions[nextQuestionIndex]['all_candidates'][3]);
    }
    else if (allQuestions[nextQuestionIndex]['type'] == 'input1')
    {
        $("#answer_area_input_" + quizID).prop('disabled', false);

        $("#answer_area_input_" + quizID).val('');
        $("#answer_area_input_" + quizID).attr("placeholder", allQuestions[nextQuestionIndex]['placeholder']);

        $("#check_answer_button_" + quizID).prop('disabled', false);

        $("#multiple4_area_1_id_" + quizID).css({"display": "none"});
        $("#multiple4_area_2_id_" + quizID).css({"display": "none"});

        $("#input1_area_id_" + quizID).css({"display": "block"});
    }
    else if (allQuestions[nextQuestionIndex]['type'] == 'multiple2')
    {
        $("#answer1Area_id_" + quizID).prop('disabled', false);
        $("#answer2Area_id_" + quizID).prop('disabled', false);

        $("#multiple4_area_1_id_" + quizID).css({"display": "block"});

        $("#input1_area_id_" + quizID).css({"display": "none"});

        $("#multiple4_area_2_id_" + quizID).css({"display": "none"});
        $("#answer1Area_id_" + quizID).text(allQuestions[nextQuestionIndex]['all_candidates'][0]);
        $("#answer2Area_id_" + quizID).text(allQuestions[nextQuestionIndex]['all_candidates'][1]);
    }
}

function checkAnswerInput1(quizID, thisObject)
{
    nextQuestionIndex = nextQuestionIndex + 1;

    $("#score_bar_id_" + quizID).width(((100/allQuestions.length) * nextQuestionIndex).toString() + "%");

    if (allQuestions[nextQuestionIndex-1]['type'] == 'no_input')
    {
        //console.log("#answer_no_eval_id_" + quizID);
        $("#answer_no_eval_id_" + quizID).css({"display": "block"});
        $("#answer_no_eval_id_" + quizID).text(correctAnswer);
        soundHandle = document.getElementById('soundHandle_correct');
        soundHandle.play();
    }
    else if ($("#answer_area_input_" + quizID).val() == correctAnswer)
    {
        $("#correctAnsMessage_id_" + quizID).css({"display": "block"});
        soundHandle = document.getElementById('soundHandle_correct');
        soundHandle.play();
    }
    else
    {
        $("#incorrectAnsMessage_id_" + quizID).css({"display": "block"});
        soundHandle = document.getElementById('soundHandle_incorrect');
        soundHandle.play();

        $("#corrAnswerPH_id_" + quizID).text(correctAnswer);
    }

    if (nextQuestionIndex < allQuestions.length)
    {
        canGoToNext = true;
        $("#goToNext_id_" + quizID).css({"display": "inline-block"});
        $("#save_id_" + quizID).css({"display": "inline-block"});
        //$("#addToFavorites_id_" + quizID).css({"display": "inline-block"});
    }

    $("#answer_area_input_" + quizID).prop('disabled', true);
    $(thisObject).prop('disabled', true);
}

function checkAnswer(e, quizID)
{
    nextQuestionIndex = nextQuestionIndex + 1;

    $("#score_bar_id_" + quizID).width(((100/allQuestions.length) * nextQuestionIndex).toString() + "%");

    if ($(e).text() == correctAnswer)
    {
        $("#correctAnsMessage_id_" + quizID.toString()).css({"display": "block"});
        soundHandle = document.getElementById('soundHandle_correct');
        soundHandle.play();
    }
    else
    {
        $("#incorrectAnsMessage_id_" + quizID.toString()).css({"display": "block"});
        soundHandle = document.getElementById('soundHandle_incorrect');
        soundHandle.play();

        $("#corrAnswerPH_id_" + quizID.toString()).text(correctAnswer);
    }

    if (nextQuestionIndex < allQuestions.length)
    {
        canGoToNext = true;
        $("#goToNext_id_" + quizID.toString()).css({"display": "inline-block"});
        $("#save_id_" + quizID.toString()).css({"display": "inline-block"});
        //$("#addToFavorites_id_" + quizID.toString()).css({"display": "inline-block"});
    }

    $("#answer1Area_id_" + quizID.toString()).prop('disabled', true);
    $("#answer2Area_id_" + quizID.toString()).prop('disabled', true);
    $("#answer3Area_id_" + quizID.toString()).prop('disabled', true);
    $("#answer4Area_id_" + quizID.toString()).prop('disabled', true);
}

function getQuestionsPreview(all_questions)
{
    $("#id_preview").collapse("show");
    console.log(all_questions);

}

function expand_pdf(num)
{
    $("#id_" + num.toString()).collapse("toggle");
}

function getQuestions(num)
{
    if (quizOpen == false)
    {


        $("#score_bar_id_" + num).width(0);

        $("#answer_area_input_" + num).prop('disabled', false);

        $("#check_answer_button_" + num).prop('disabled', false);
        $("#answer_area_input_" + num).val('');

        $("#input1_area_id_" + num.toString()).css({"display": "none"});

        $("#multiple4_area_1_id_" + num.toString()).css({"display": "none"});
        $("#multiple4_area_2_id_" + num.toString()).css({"display": "none"});
        $("#answer_no_eval_id_" + num.toString()).css({"display": "none"});

        nextQuestionIndex = 0;

        $("#correctAnsMessage_id_" + num.toString()).css({"display": "none"});
        $("#incorrectAnsMessage_id_" + num.toString()).css({"display": "none"});
        $("#goToNext_id_" + num.toString()).css({"display": "none"});

        $("#answer1Area_id_" + num.toString()).prop('disabled', false);
        $("#answer2Area_id_" + num.toString()).prop('disabled', false);
        $("#answer3Area_id_" + num.toString()).prop('disabled', false);
        $("#answer4Area_id_" + num.toString()).prop('disabled', false);


        //$("#id_" + num.toString()).toggle('show');
        //return;

        // Make an ajax call to get the questions and answers
        //
        $.ajax(
            {
                type: "POST",
                data: {
                    btnType: 'getQuestionsAnswers',
                    idSent: num,
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                },
                success: function (data)
                {
                    console.log(data);

                    //console.log(data);

                    allQuestions = data['allItemsSent'];

                    //console.log(allQuestions);

                    $("#questionArea_id_" + num.toString()).html(allQuestions[0]['question']);
                    correctAnswer = allQuestions[0]['correct_answer'];

                    if (allQuestions[0]['type'] == 'no_input')
                    {
                        $("#input1_area_id_" + num.toString()).css({"display": "block"});
                        $("#answer_area_input_" + num.toString()).css({"display": "none"});
                    }


                    if (allQuestions[0]['type'] == 'multiple2')
                    {
                        $("#multiple4_area_1_id_" + num.toString()).css({"display": "block"});
                        $("#answer1Area_id_" + num.toString()).text(allQuestions[0]['all_candidates'][0]);
                        $("#answer2Area_id_" + num.toString()).text(allQuestions[0]['all_candidates'][1]);
                    }

                    if (allQuestions[0]['type'] == 'multiple4')
                    {
                        $("#multiple4_area_1_id_" + num.toString()).css({"display": "block"});
                        $("#multiple4_area_2_id_" + num.toString()).css({"display": "block"});
                        $("#answer1Area_id_" + num.toString()).text(allQuestions[0]['all_candidates'][0]);
                        $("#answer2Area_id_" + num.toString()).text(allQuestions[0]['all_candidates'][1]);
                        $("#answer3Area_id_" + num.toString()).text(allQuestions[0]['all_candidates'][2]);
                        $("#answer4Area_id_" + num.toString()).text(allQuestions[0]['all_candidates'][3]);
                    }

                    if (allQuestions[0]['type'] == 'input1')
                    {
                        $("#input1_area_id_" + num.toString()).css({"display": "block"});
                        $("#answer_area_input_" + num.toString()).attr("placeholder", allQuestions[0]['placeholder']);
                    }

                    quizOpen = true;
                    quizOpen_id = "#id_" + num.toString();

                    $("#id_" + num.toString()).collapse("show");

                    //console.log("#id_" + num.toString());
                    //$("#id_" + num.toString()).toggle('show');
                }
            });
    }
    else
    {
        $(quizOpen_id).collapse("hide");
        quizOpen = false;

        // If you're trying to open another quiz, open current quiz
        //
        if (quizOpen_id != ("#id_" + num.toString()))
        {
            getQuestions(num);
        }
    }
}

var question_type = 'multiple4';

var specialElementHandlers = {
    '#editor': function (element, renderer) {
        return true;
    }
};

var full_name;
var assignment_num;
var student_name;

function submit_answers()
{
    var children_divs = $("#all_questions_div").children();

    var all_questions_answers = [];

    for (var i = 0; i < children_divs.length; i++)
    {
        // if this is a question/answer element (nor hr or something else)
        //
        if ($(children_divs[i]).is('div') == true)
        {
            if (typeof $(children_divs[i]).attr('id') != 'undefined')
            {
                var div_id_string = $(children_divs[i]).attr('id').toString();
                if (div_id_string.indexOf("question") != -1)
                {
                    var questions_answer = {};

                    // we first get the id of the question
                    //
                    question_id = div_id_string.split("_")[2];

                    questions_answer["id"] = question_id;
                    questions_answer["question"] = $($(children_divs[i]).children()[0]).text();

                    if ($($(children_divs[i]).children()[1]).val() == '')
                        questions_answer["answer"] = 'No Answer';
                    else
                        questions_answer["answer"] = $($(children_divs[i]).children()[1]).val();

                    all_questions_answers.push(questions_answer)
                }
            }
        }
    }

    console.log(all_questions_answers);
}


// At first, we'll pass 1 (third argument) until we're done looping through all the questions
// Then, we'll pass 0 and loop again to add the asnwers
//
function to_be_determined(dd, i, is_question)
{
    html2canvas($("#all_questions_pdf"),
        {
            onrendered: function(canvas)
            {
                var dataURL = canvas.toDataURL(/*'image/jpeg'*/);

                curr_obj = {};
                curr_obj['image'] = dataURL;
                curr_obj['width'] = 520;
                curr_obj['style'] = 'centerme';

                if (i == 0 && !is_question)
                {
                    curr_obj['pageBreak'] = 'before';
                }

                dd['content'].push(curr_obj);

                if (dd['content'].length == allQuestions.length || dd['content'].length == (allQuestions.length * 2))
                {
                    $("#all_questions_pdf").empty();
                    if (is_question)
                    {
                        i = 0;
                        my_div = $("<div style=\"font-family: 'Lane - Narrow'; font-size: xx-large; margin: 5px; border: .5px solid lightgrey; padding: 20px; line-height: 120%;\">").html('Answer to Question ' + (i+1).toString() + ') ' + allQuestions[i]['correct_answer']);
                        $("#all_questions_pdf").append(my_div);

                        to_be_determined(dd, i, false);
                    }
                    else
                    {
                        style_obj_l1 = {};
                        style_obj_l1['alignment'] = 'center';

                        style_obj_l2 = {};
                        style_obj_l2['centerme'] = style_obj_l1;

                        dd['styles'] = style_obj_l2;

                        //console.log(JSON.stringify(dd));

                        var d = new Date();
                        var date_formatted =
                            d.getFullYear() + "-" +
                            ("00" + (d.getMonth() + 1)).slice(-2) + "-" +
                            ("00" + d.getDate()).slice(-2) + " " +
                            ("00" + d.getHours()).slice(-2) + ":" +
                            ("00" + d.getMinutes()).slice(-2) + ":" +
                            ("00" + d.getSeconds()).slice(-2);

                        $('#logo_loading').text('Almost done...');
                        pdfMake.createPdf(dd).download('Practice_' + date_formatted.toString().replace(' ', '_'), function() {$('#logo_loading').text(full_name + '.');}); //full_name.replace(' ', '') + parseInt(Math.random()*100).toString());
                    }
                }
                else
                {
                    $("#all_questions_pdf").empty();
                    i = i + 1;

                    //console.log(i);

                    if (is_question)
                    {
                        $('#logo_loading').text('Adding Question ' + i.toString());

                        my_div = $("<div style=\"font-family: 'Lane - Narrow'; font-size: xx-large; margin: 5px; border: .5px solid lightgrey; padding: 20px; line-height: 120%;\">").html('Question ' + (i + 1).toString() + ') ' + allQuestions[i]['question']);
                    }
                    else
                    {
                        $('#logo_loading').text('Adding Answer ' + i.toString());
                        my_div = $("<div style=\"font-family: 'Lane - Narrow'; font-size: xx-large; margin: 5px; border: .5px solid lightgrey; padding: 20px; line-height: 120%;\">").html('Answer to Question ' + (i + 1).toString() + ') ' + allQuestions[i]['correct_answer']);
                    }
                    $("#all_questions_pdf").append(my_div);

                    var elements = document.getElementsByClassName('my_code');

                    for (var el_counter = 0; el_counter < elements.length; el_counter++)
                    {
                        var element = elements[el_counter];
                        element.style.fontSize = "36px";
                    }

                    to_be_determined(dd, i, is_question);
                }
            }
        });
}

function generatePDF(num, section_title, sub_title)
{
    pdfMake.fonts = {
        Lane: {
            normal: 'LANENAR_.ttf',
        }
    };

    var start_dd = {
        header: function() {
            return {
                columns: [
                    {
                        alignment: 'center',
                        text: section_title
                    }
                ],
                margin: [30, 20]
            };
        },

        footer: function(page, pages) {
            return {
                columns: [
                    sub_title,
                    {
                        alignment: 'right',
                        text: [
                            'Generated by ' + full_name + '. Page ',
                            { text: page.toString() },
                            ' of ',
                            { text: pages.toString() }
                        ]
                    }
                ],
                margin: [30, 0]
            };
        },
        content: [],
        pageSize: 'Letter',
        defaultStyle:
            {
                font: 'Lane'
            }
    };

    $.ajax(
        {
            type: "POST",
            data: {
                btnType: 'getQuestionsAnswers',
                idSent: num,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function (data)
            {
                allQuestions = data['allItemsSent'];

                //console.log(allQuestions);
                //return;

                var i = 0;
                $("#all_questions_pdf").empty();
                my_div = $("<div style=\"font-family: 'Lane - Narrow'; border: .5px solid lightgrey; font-size: xx-large; margin: 5px; padding: 20px; line-height: 120%;\">").html('Question ' + (i+1).toString() + ') ' + allQuestions[i]['question']);
                $("#all_questions_pdf").append(my_div);

                var elements = document.getElementsByClassName('my_code');

                for (var el_counter = 0; el_counter < elements.length; el_counter++)
                {
                    var element = elements[el_counter];
                    element.style.fontSize = "36px";
                }

                to_be_determined(start_dd, i, true);
            }
        });
}

function save_for_later()
{
    var children_divs = $("#all_questions_div").children();

    var all_answers_sent = {};

    for (var i = 0; i < children_divs.length; i++)
    {
        if ($(children_divs[i]).is('div') == true)
        {
            if (typeof $(children_divs[i]).attr('id') != 'undefined')
            {
                var div_id_string = $(children_divs[i]).attr('id').toString();

                if (div_id_string.indexOf("question") != -1)
                {

                    //to_be_printed = to_be_printed + question_counter.toString() + ') ' + $($(children_divs[i]).children()[0]).text().trim() + '\n';


                    answer_id = $($(children_divs[i]).children()[1]).attr('id');

                    var elementType = $($(children_divs[i]).children()[1]).prop('nodeName');
                    //console.log(elementType);


                    if (elementType == 'INPUT')
                        answer_text = $($(children_divs[i]).children()[1]).val();
                    else
                        answer_text = $($(children_divs[i]).children()[1]).html();

                    all_answers_sent[answer_id] = answer_text

                    //if ($($(children_divs[i]).children()[1]).val() == '')
                    //    to_be_printed = to_be_printed + 'No Answer'
                    //else
                    //    to_be_printed = to_be_printed + $($(children_divs[i]).children()[1]).val();

                    //to_be_printed = to_be_printed + '\n\n*************\n\n'
                }
            }
        }
    }

    $.ajax(
        {
            type: "POST",

            data: {
                btnType: 'csci_save_answers',
                all_answers: JSON.stringify(all_answers_sent),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (data)
            {

                //console.log(data);
                location.reload();
                //document.location.href="/";
            }
        });

}


function generate_pdf_assignment(names_array, current_index, curr_dd, _is_assignment)
{
    curr_element = $("#" + names_array[current_index]).clone();

    $("#question_inside").empty();
    $("#question_inside").append(curr_element);

    $(curr_element.children()[1]).css({"font-size": "25px"});
    $(curr_element.children()[1]).css({"color": "indianred"});

    html2canvas($("#all_questions_pdf"),
        {
            onrendered: function(canvas)
            {
                $('#logo_loading').text('Adding Question ' + current_index.toString());

                var dataURL = canvas.toDataURL(/*'image/jpeg'*/);

                curr_obj = {};
                curr_obj['image'] = dataURL;
                curr_obj['width'] = 520;
                curr_obj['style'] = 'centerme';
                curr_dd['content'].push(curr_obj);

                if (current_index == (names_array.length - 1))
                {
                    $('#logo_loading').text('Almost done!');

                    style_obj_l1 = {};
                    style_obj_l1['alignment'] = 'center';

                    style_obj_l2 = {};
                    style_obj_l2['centerme'] = style_obj_l1;

                    curr_dd['styles'] = style_obj_l2;

                    var d = new Date();
                    var date_formatted =
                        d.getFullYear() + "-" +
                        ("00" + (d.getMonth() + 1)).slice(-2) + "-" +
                        ("00" + d.getDate()).slice(-2) + " " +
                        ("00" + d.getHours()).slice(-2) + ":" +
                        ("00" + d.getMinutes()).slice(-2) + ":" +
                        ("00" + d.getSeconds()).slice(-2);


                    //console.log(JSON.stringify(curr_dd));
                    $("#question_inside").empty();

                    curr_file_name = 'Practice_' + date_formatted.toString().replace(' ', '_');

                    if (_is_assignment)
                        curr_file_name = assignment_num + '_' + student_name.replace(" ", "_");

                    pdfMake.createPdf(curr_dd).download(curr_file_name,
                        function () {
                            $('#logo_loading').text(full_name);
                        });
                }
                else
                {
                    generate_pdf_assignment(names_array, current_index + 1, curr_dd, _is_assignment);
                }
            }

        });
}

function save_assignment_pdf(is_assignment)
{
    pdfMake.fonts = {
        Lane: {
            normal: 'LANENAR_.ttf'
        }
    };

    var start_dd = {
        header: function() {
            return {
                columns: [
                    {
                        alignment: 'center',
                        text: assignment_name
                    }
                ],
                margin: [30, 20]
            };
        },

        footer: function(page, pages) {
            return {
                columns: [
                    "Due " + assignment_due_date,
                    {
                        alignment: 'right',
                        text: [
                            student_name + '. Page ',
                            { text: page.toString() },
                            ' of ',
                            { text: pages.toString() }
                        ]
                    }
                ],
                margin: [30, 0]
            };
        },
        content: [],
        pageSize: 'Letter',
        defaultStyle:
            {
                font: 'Lane'
            }
    };

    var children_divs = $("#all_questions_div").children();

    var d = new Date();
    var n = d.toString();

    var to_be_printed = full_name + '. ' + n + "\n\n*************\n\n";

    all_ids = [];

    for (var i = 0; i < children_divs.length; i++)
    {
        if ($(children_divs[i]).is('div') == true)
        {
            if (typeof $(children_divs[i]).attr('id') != 'undefined')
            {
                var div_id_string = $(children_divs[i]).attr('id').toString();
                if (div_id_string.indexOf("question") != -1)
                {
                    // Here, what we'll do is store the id's of all questions in an array
                    //
                    all_ids.push(div_id_string);
                }
            }
        }
    }

    generate_pdf_assignment(all_ids, 0, start_dd, is_assignment);

    var docDefinition =
        {
            content: to_be_printed,
            defaultStyle:
                {
                    font: 'Lane'
                }
        };

    //pdfMake.createPdf(docDefinition).download(assignment_num + '_' + full_name.replace(" ", "_"));

    //pdfMake.createPdf(docDefinition).open();


    //doc.text('Hello world! asdfj asdf hello world hello woeld hellow whleod aheleo asdfj wowe rsfd l fds', 10, 10);
    //doc.save('a4.pdf');
}

function cosfc_login()
{
    $.ajax(
        {
            type: "POST",

            data: {
                btnType: 'csci_login',
                email: $('#login-email').val(),
                password: $('#login-pass').val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (data)
            {
                //console.log(data);
                //console.log(data);
                //location.reload();
                document.location.href="/";
            }
        });
}

function add_curr_question()
{
    $.ajax(
        {
            type: "POST",

            data: {
                btnType: 'csci_add_question',
                question_id: $('input[name=question_id_input]').val(),
                python_code: $('#python_code').val(),
                question_text: $('#question_text').val(),
                question_type: $('input[name=question_type_input]').val(),
                ans1_input: $('input[name=ans1_input]').val(),
                ans2_input: $('input[name=ans2_input]').val(),
                ans3_input: $('input[name=ans3_input]').val(),
                ans4_input: $('input[name=ans4_input]').val(),
                corr_ans_input: $('input[name=corr_ans_input]').val(),
                repeat_input: $('input[name=repeat_input]').val(),
                subitem_id: $('input[name=subitem_id]').val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (data)
            {
                //console.log(data);
                window.location = '/admin/' + data['id'] + '/';
            }
        });

}

function copy_question()
{
    $.ajax(
        {
            type: "POST",
            data: {
                btnType: 'csci_copy_question',
                question_id: $('input[name=question_id_input]').val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (data)
            {
                window.location = '/admin/' + data['id'] + '/';
            }
        });
}

function delete_question()
{
    $.ajax(
        {
            type: "POST",
            data: {
                btnType: 'csci_delete_question',
                question_id: $('input[name=question_id_input]').val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (data)
            {
                window.location = '/admin';
            }
        });
}

function take_screenshot_question()
{
    html2canvas($("#id_take_screen"),
        {
            onrendered: function(canvas)
            {
                theCanvas = canvas;

                var dataURL = canvas.toDataURL();
                //console.log(dataURL);

                var res = dataURL.split(",")[1];
                console.log(res);

                $.ajax(
                    {
                        type: "POST",

                        data: {
                            btnType: 'save_image',
                            img_content: res,
                            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                        },
                        success: function (data)
                        {
                            console.log('saved');
                            //location.reload();
                        }
                    });

                /*canvas.toBlob(function(blob)
                 {


                 saveAs(blob, "Dashboard.png");
                 });*/
            }
        });
}

function update_password()
{
    console.log($('#login-pass-1').val());

    $.ajax(
        {
            type: "POST",

            data: {
                btnType: 'update_password',
                password: $('#login-pass-1').val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (data)
            {
                location.reload();
            }
        });
}

function cosfc_signup()
{
    // We first get the values that we'll pass to an ajax
    //
    first_name = $("#first_name").val();
    last_name = $("#last_name").val();
    section = $("#section_list option:selected").text();
    email = $("#sign_up_email").val();
    pass = $("#sign_up_pass").val();

    $.ajax(
        {
            type: "POST",

            data: {
                btnType: 'csci_sign_up',
                first_name: first_name,
                last_name: last_name,
                section: section,
                email: email,
                pass: pass,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (data)
            {
                window.location = '/login';
            }
        });
}

function csci_logout()
{
    $.ajax(
        {
            type: "POST",

            data: {
                btnType: 'csci_logout',
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (data)
            {
                //console.log(data);
                location.reload();

                //window.location = '/questions';
            }
        });
}

function add_question_multiple4()
{
    $('#div_multiple').css({"display": "block"});
    $('#second_two_multiple').css({"display": "block"});
}

function add_question_multiple2()
{
    $('#div_multiple').css({"display": "block"});
    $('#second_two_multiple').css({"display": "none"});
}

function add_question_input1()
{
    $('#div_multiple').css({"display": "none"});
}

function preview_question(question_id)
{
    console.log(question_id);
}

function showText(target, messages, index, interval, message_index, append_at_once)
{
    var message = messages[message_index];

    if (message.append_at_once)
    {
        $(target).append(message.text);
        $(target).scrollTop($(target)[0].scrollHeight);

        if (message.stop_after)
        {
            my_arr = my_arr.slice(message_index+1, messages.length);
            return message_index; //messages.slice(message_index+1,messages.length);
        }

        if (message_index < messages.length -1)
        {
            setTimeout(
                function ()
                {
                    showText(target, messages, 0, messages[message_index+1].duration, message_index+1, messages[message_index+1].append_at_once);
                },
                messages[message_index+1].duration);
        }
    }
    else if (index < message.text.length)
    {
        $(target).append(message.text[index++]);
        $(target).scrollTop($(target)[0].scrollHeight);

        setTimeout(
            function ()
            {
                showText(target, messages, index, message.duration, message_index, append_at_once);
            },
            message.duration);
    }
    else if (message_index < messages.length - 1)
    {
        if (message.stop_after)
        {
            my_arr = my_arr.slice(message_index+1, messages.length);
            return message_index; //messages.slice(message_index+1,messages.length);
        }

        console.log(message_index);
        showText(target, messages, 0, messages[message_index+1].duration, message_index+1, messages[message_index+1].append_at_once);
    }
}

var my_arr = [];

function answer_clicked()
{
    showText('#sub_item_id_25', my_arr, 0, false, 0);
}

var lesson_open = false;

function add_lesson_item_below(e)
{
    $(e).parent().parent().after('<div style="background-color: lightgoldenrodyellow; border: solid 1px lightgrey; padding: 10px; border-radius: 5px; margin: 15px;"> \
                                    <div style="padding-bottom: 0px; margin-bottom: 0px;"> \
                                        <span style="color: black; font-size: larger; text-transform: uppercase;">Display at once:</span><input name="question_type_input" spellcheck="false" style="margin-left: 10px; width: 8%; padding: 10px; font-size: large;"/> \
                                        <span style="margin-left: 20px; text-transform: uppercase; color: black; font-size: larger;">Stop after:</span><input name="question_type_input" spellcheck="false" style="margin-left: 10px; width: 8%; padding: 10px; font-size: large;"/> \
                                        <span style="margin-left: 20px; text-transform: uppercase; color: black; font-size: larger;">Duration:</span><input name="question_type_input" spellcheck="false" style="margin-left: 10px; width: 6%; padding: 10px; font-size: large;"/> \
                                        <span style="margin-left: 20px; text-transform: uppercase; color: black; font-size: larger;">ID:</span><input name="question_type_input" spellcheck="false" style="margin-left: 10px; width: 6%; padding: 10px; font-size: large;" disabled/> \
                                        <textarea onfocus="expandHeight(this);" onkeydown="expandHeight(this);" rows="30" id="python_code" spellcheck="false" style="border-radius: 10px; margin-bottom: 5px; font-size: larger; width: 100%;"></textarea> \
                                    </div> \
                                    <div> \
                                        <button class="btn-success" style="border-radius: 5px; font-size: larger; padding: 5px; padding-left: 10px; padding-right: 10px;" onclick="$(this).parent().parent().remove();">Delete above</button> \
                                        <button class="btn-success" style="border-radius: 5px; font-size: larger; padding: 5px; padding-left: 10px; padding-right: 10px;" onclick="add_lesson_item_below(this);">Add Below</button> \
                                    </div> \
                                </div>');
}

function delete_above(e)
{
    $(e).parent().prev().remove();
    $(e).parent().remove();
}

function add_questions_div(e)
{
    $(e).after('<div> ' +
        '<button class="btn-primary" style="text-transform: uppercase; padding: 5px; margin: 5px;" onclick="add_multiple_choice_4(this)">Add Multiple Choice (4)</button> ' +
        '<button class="btn-primary" style="text-transform: uppercase; padding: 5px; margin: 5px;" onclick="add_main_title(this);">Add Main Question Title</button> ' +
        '<button class="btn-primary" style="text-transform: uppercase; padding: 5px; margin: 5px;" onclick="delete_above(this);">Delete Above</button>' +
        '</div>');
}

function add_multiple_choice_4(e)
{
    $(e).parent().after('<div id="multiple4_question" style="width: 100%;">' +
        '<textarea style="width: 100%; padding: 10px; font-size: larger; margin: 5px;" placeholder="Question Title..." />' +
        '<textarea style="width: 100%; padding: 10px; font-size: larger; margin: 5px;" placeholder="Python Code..." />' +
        '<div style="text-align: center;">' +
        '<input name="question_id_input" style="width: 23%; margin: 5px; padding: 10px; font-size: larger;"  placeholder="Choice 1" />' +
        '<input name="question_id_input" style="width: 23%; margin: 5px; padding: 10px; font-size: larger;"  placeholder="Choice 2" />' +
        '<input name="question_id_input" style="width: 23%; margin: 5px; padding: 10px; font-size: larger;"  placeholder="Choice 3" />' +
        '<input name="question_id_input" style="width: 23%; margin: 5px; padding: 10px; font-size: larger;"  placeholder="Choice 4" />' +
        '</div>' +
        '<div style="text-align: center;"><input name="question_id_input" style="width: 23%; margin: 5px; padding: 10px; font-size: larger;" placeholder="Correct Answer"/></div>' +
        '</div>');

    add_questions_div($(e).parent().next());
}

function add_main_title(e)
{
    $(e).parent().after('<div id="title_question" style="width: 100%;">' +
        '<textarea style="width: 100%; padding: 10px; font-size: larger; margin: 5px;" placeholder="Question Title..."/>' +
        '</div>');
    add_questions_div($(e).parent().next());
}

function update_db()
{
    assignment_title = $('#beginning_of_page').children()[0].value;

    curr_el = $('#beginning_of_page').next().next();

    all_questions_to_be_sent = [];

    while (curr_el.attr('id') != 'update_div')
    {
        curr_question = {};
        if( curr_el.attr('id') == 'title_question')
        {
            curr_question['question_title'] = curr_el.children()[0].value;

            curr_question['question_type'] = 'title';

            all_questions_to_be_sent.push(curr_question);
        }
        if (curr_el.attr('id') == 'multiple4_question')
        {
            curr_question['question_title'] = curr_el.children()[0].value;

            curr_question['question_type'] = 'multiple4';

            curr_question['python_code'] = curr_el.children()[1].value;

            curr_question['choice_1'] = $(curr_el.children()[2]).children()[0].value;
            curr_question['choice_2'] = $(curr_el.children()[2]).children()[1].value;
            curr_question['choice_3'] = $(curr_el.children()[2]).children()[2].value;
            curr_question['choice_4'] = $(curr_el.children()[2]).children()[3].value;

            curr_question['correct_answer'] = $(curr_el.children()[3]).children()[0].value;

            all_questions_to_be_sent.push(curr_question);
        }


        curr_el = curr_el.next();
    }

    var json_string = JSON.stringify(all_questions_to_be_sent);

    console.log(json_string);
    console.log(all_questions_to_be_sent);

    //return;

    $.ajax(
        {
            type: "POST",

            data: {
                btnType: 'update_assignment',
                assignment_title: assignment_title,
                all_q: json_string,
                all_b: [4, 1, 10],
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (data)
            {
                console.log(data);

                /*for (i = 0; i < data['allItemsSent'].length; i++) {
                 console.log(data['allItemsSent'][i].text)
                 my_arr.push(data['allItemsSent'][i])
                 }

                 showText('#sub_item_id_25', my_arr, 0, false, 0);
                 lesson_open = true;*/
            }
        });

    console.log(all_questions_to_be_sent);
}

function expand_lesson()
{
    // Get items from databse, do an ajax call
    //
    if (lesson_open == false)
    {
        my_arr = [];
        $('#sub_item_id_34').empty();
        $.ajax(
            {
                type: "POST",

                data: {
                    btnType: 'get_lesson',
                    lesson_id: 34,
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                },
                success: function (data)
                {
                    console.log(data);

                    for (i = 0; i < data['allItemsSent'].length; i++)
                    {
                        console.log(data['allItemsSent'][i].text)
                        my_arr.push(data['allItemsSent'][i])
                    }

                    showText('#sub_item_id_34', my_arr, 0, false, 0);
                    lesson_open = true;
                }
            });
    }
    else
    {
        lesson_open = false;
    }
}