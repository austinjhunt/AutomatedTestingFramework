from django.shortcuts import render
import functionsFromDB

import cStringIO

import base64

from PIL import Image

#import Image

from django.shortcuts import render, redirect

from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import authenticate, login, logout

# Create your views here.
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.template import RequestContext, loader

import datetime


from main.models import Week, Topic, Item, SubItem, QuizQuestion, Lesson_items, Assignments, \
    Assignment_question_mltiple4, Assignment_question, Final_Exam, Assignment_answer, Student_assignment_answers, \
    Audio_play_history, User, My_User, Section, Saved_Questions

import calendar

from random import shuffle
from random import randint
from random import seed
from random import choice
from random import sample


import random
import json

class Question:
    def __init__(self, _questionText):
        self.id = ''
        self.questionText = _questionText
        self.listOfCandidates = []
        self.correctAnswer = ''
        self.questionType = ''

class SubItemClass:
    def __init__(self, _id, _title, _category, _show, _link):
        self.id = _id
        self.title = _title
        self.category = _category
        self.questions = []
        self.show = _show
        self.link = _link


class MyItem:
    def __init__(self):
        self.id = -1
        self.type = None
        self.value = None
        self.subType = None
        self.subItems = []
        self.expand = None


@csrf_exempt
def page_not_found(request):
    template = loader.get_template('main/home.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))

def twos_comp(val, bits):
    """compute the 2's compliment of int value val"""

    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val                         # return positive value as is


def addTwoBinaries(binary1, binary2, result_length):
    value1_int = int(binary1[2:], 2)
    value2_int = int(binary2[2:], 2)
    ans = value1_int + value2_int
    ans_binary = bin(ans)
    if ans > 31:
        ans_binary = ans_binary[:2] + ans_binary[3:]

    while len(ans_binary) != (result_length + 2):
        ans_binary = ans_binary[0:2] + '0' + ans_binary[2:]

    return ans_binary

def checkIfOverflow(value1, value2):
    ans = int(value1, 2) + int(value2, 2)
    if ans > 31:
        return 'Yes (an overflow will occur)'
    else:
        return 'No overflow'

def returnCorrectValues(_specialText, _placeholderValues):

    currSplit = _specialText.split(',')


    if  currSplit[1] == 'eval':

        # Replace each ^variableName with its value
        #
        for num in range(2, len(currSplit)):
            if '^' in currSplit[num]:
                currSplit[num] = _placeholderValues[currSplit[num].replace('^', '')]

        # Concatenate all elements in list to then evaluate
        #
        expression = ''
        for num in range(2, len(currSplit)):
            expression = expression + str(currSplit[num])

        _placeholderValues[currSplit[0]] = eval(expression)
        return


    if currSplit[1] == 'checkOverflowUnsigned':
        if '^' in currSplit[2]:
            modifiedValue1 = int(_placeholderValues[currSplit[2].replace('^', '')], 2)
        if '^' in currSplit[3]:
            modifiedValue2 = int(_placeholderValues[currSplit[3].replace('^', '')], 2)
        ans = modifiedValue1 + modifiedValue2
        ans_binary = bin(ans)
        if ans > 31:
            _placeholderValues[currSplit[0]] = 'Yes (an overflow will occur)'
        else:
            _placeholderValues[currSplit[0]] = 'No overflow'

    if currSplit[1] == 'addTwoBinaries':
        if '^' in currSplit[2]:
            modifiedValue1 = int(_placeholderValues[currSplit[2].replace('^', '')], 2)
        if '^' in currSplit[3]:
            modifiedValue2 = int(_placeholderValues[currSplit[3].replace('^', '')], 2)
        ans = modifiedValue1 + modifiedValue2
        ans_binary = bin(ans)
        if ans > 31:
            ans_binary = ans_binary[:2] + ans_binary[3:]

        while len(ans_binary) != len(_placeholderValues[currSplit[2].replace('^', '')]):
            ans_binary = ans_binary[0:2] + '0' + ans_binary[2:]

        _placeholderValues[currSplit[0]] = ans_binary
        return

    if currSplit[1] == 'hexFromBinary':
        if '^' in currSplit[2]:
            modifiedValue = _placeholderValues[currSplit[2].replace('^', '')]
        _placeholderValues[currSplit[0]] = hex(int(modifiedValue, 2))

    if currSplit[1] == 'binaryFromHex':
        if '^' in currSplit[2]:
            modifiedValue = _placeholderValues[currSplit[2].replace('^', '')]
        _placeholderValues[currSplit[0]] = bin(int(modifiedValue, 16))
        return

    if currSplit[1] == 'decimalFromTwosComplement':
        if '^' in currSplit[2]:
            modifiedValue = _placeholderValues[currSplit[2].replace('^', '')]

        _placeholderValues[currSplit[0]] =  twos_comp(int(modifiedValue[2:], 2), len(modifiedValue) - 2)

    if currSplit[1] == 'decimalFromSignMagnitude':
        if '^' in currSplit[2]:
            modifiedValue = _placeholderValues[currSplit[2].replace('^', '')]
        ans_decimal = int(modifiedValue[3:], 2)
        if modifiedValue[2] == '1':
            ans_decimal = ans_decimal * -1
        _placeholderValues[currSplit[0]] = ans_decimal
        return

    if(currSplit[1] == 'decimal'):
        if '^' in currSplit[2]:
            modifiedValue = _placeholderValues[currSplit[2].replace('^', '')]

        value = 0
        for num, el in enumerate(modifiedValue[2:][::-1]):
            value = value + (int(el) * (2**num))

        _placeholderValues[currSplit[0]] = value
        return

    if currSplit[1] == 'randHex':
        _placeholderValues[currSplit[0]] = hex(randint(int(currSplit[2]), int(currSplit[3])))
        return

    if(currSplit[1] == 'randBinary' and len(currSplit) == 4):
        _placeholderValues[currSplit[0]] = bin(randint(int(currSplit[2]), int(currSplit[3])))
        return

    if(currSplit[1] == 'randDecimal'):
        _placeholderValues[currSplit[0]] = randint(int(currSplit[2]), int(currSplit[3]))
        return

    if currSplit[1] == 'binaryTwosComplementFromDecimal':
        # Example: ***ans,binaryTwosComplementFromDecimal,^v1,6***
        #
        if '^' in currSplit[2]:
            decimal_value = _placeholderValues[currSplit[2].replace('^', '')]
        else:
            decimal_value = currSplit[2]

        _placeholderValues[currSplit[0]] = functionsFromDB.binaryTwosComplementFromDecimal(_decimal_value=decimal_value, _bitstring_length=int(currSplit[3]))

def convert_simple_line_c_to_mips(_one_line):
    # First we separate by spaces
    #
    my_comps = _one_line.split(' ')

    # We use [:-1] to get rid of the semi-colon
    #
    if my_comps[0] == 'int':
        return 'addi $' + my_comps[1] + ', $zero, ' + my_comps[3][:-1]
    elif my_comps[3] == '+' and my_comps[4][:-1].isdigit():
        return 'addi $' + my_comps[0].replace('\t', '') + ", $" + my_comps[2] + ", " + my_comps[4][:-1]
    elif my_comps[3] == '-' and my_comps[4][:-1].isdigit():
        return 'addi $' + my_comps[0].replace('\t', '') + ", $" + my_comps[2] + ", -" + my_comps[4][:-1]
    elif my_comps[3] == '+' and not my_comps[4][:-1].isdigit():
        return 'add $' + my_comps[0].replace('\t', '') + ", $" + my_comps[2] + ", $" + my_comps[4][:-1]
    elif my_comps[3] == '-' and not my_comps[4][:-1].isdigit():
        return 'sub $' + my_comps[0].replace('\t', '') + ", $" + my_comps[2] + ", $" + my_comps[4][:-1]

def cofc_convert_binary_to_hex(_binary_value):
    return hex(int(_binary_value, 2))

def cofc_convert_decimal_to_unsigned_binary_with_length(_decimal_value, _length_of_binary):
    ans_binary = bin(_decimal_value)
    while len(ans_binary) < (_length_of_binary + 2):
        ans_binary = ans_binary[0:2] + '0' + ans_binary[2:]

    # Remove MSB
    if len(ans_binary) > (_length_of_binary + 2):
        ans_binary = ans_binary[0:2] + ans_binary[3:]

    return ans_binary

def cofc_convert_decimal_to_unsigned_binary(_decimal_value):
    return bin(_decimal_value)

def cofc_convert_binary_to_decimal(_binary_value):
    return int(_binary_value[2:], 2)

def cofc_convert_hexadecimal_to_decimal(_hexadecimal_value):
    return int(_hexadecimal_value, 16)

def cofc_convert_hexadecimal_to_binary(_hexadecimal_value):
    return bin(int(_hexadecimal_value, 16))

def cofc_convert_decimal_to_sign_magnitude(_decimal_value, _length_of_binary):
    ans_binary = bin(int(abs(_decimal_value)))
    # Then we make it x number of bits where x is the 4th parameters in our list
    #
    while len(ans_binary) != (_length_of_binary + 2):
        ans_binary = ans_binary[0:2] + '0' + ans_binary[2:]
        # Finally, we make the MSB 1 if the number is negative, otherwise do nothing
        #
    if _decimal_value < 0:
        ans_binary = ans_binary[0:2] + '1' + ans_binary[3:]

    return ans_binary

def cofc_generate_random_decimal(_starting_value, _ending_value):
    return randint(int(_starting_value), int(_ending_value))

def cofc_generate_random_binary(_starting_value, _ending_value, _length_of_binary):
    binarySequence = bin(randint(_starting_value, _ending_value))
    while len(binarySequence) != (_length_of_binary + 2) and _length_of_binary != 0:
        binarySequence = binarySequence[0:2] + '0' + binarySequence[2:]
    return binarySequence

def cofc_generate_random_hexadecimal(_starting_value, _ending_value):
    return hex(randint(_starting_value, _ending_value))

def cofc_decimal_to_ones_complement(_decimal_value, _length_of_binary):
    # First we get the binary of the "positive" version of the number
    #
    ans_binary = bin(int(abs(_decimal_value)))
    # Then we make it x number of bits where x is the 4th parameters in our list
    #
    while len(ans_binary) != (_length_of_binary + 2):
        ans_binary = ans_binary[0:2] + '0' + ans_binary[2:]
        # If the number is negative, we flip all bits
        #
    if _decimal_value < 0:
        ans_binary = ans_binary.replace('0', 'x')
        ans_binary = ans_binary.replace('1', '0')
        ans_binary = ans_binary.replace('x', '1')
        ans_binary = '0' + ans_binary[1:]

    return ans_binary

def cofc_decimal_to_twos_complement(_decimal_value, _length_of_binary):
    return functionsFromDB.binaryTwosComplementFromDecimal(_decimal_value=_decimal_value, _bitstring_length=_length_of_binary)

def cofc_ones_complement_to_decimal(_ones_complement_binary):
    # First we check if it's positive; if it is, we simply convert to decimal
    #
    if _ones_complement_binary[2] == '0':
        ans_decimal = int(_ones_complement_binary[2:], 2)
    else:
        # First we swap the 0s with 1s and vice versa
        #
        _ones_complement_binary = _ones_complement_binary.replace('0', 'x')
        _ones_complement_binary = _ones_complement_binary.replace('1', '0')
        _ones_complement_binary = _ones_complement_binary.replace('x', '1')

        # Now we convert to decimal
        #
        ans_decimal = int(_ones_complement_binary[2:], 2) * -1

    return ans_decimal

def cofc_twos_complement_to_decimal(_tows_complement_binary):
    return twos_comp(int(_tows_complement_binary[2:], 2), len(_tows_complement_binary) - 2)


def execute_function(_function_name, _list_of_arguments):
    if _function_name == 'twosComplementToDecimal':
        return cofc_twos_complement_to_decimal(_list_of_arguments[0])

    if _function_name == 'onesComplementToDecimal':
        return cofc_ones_complement_to_decimal(_list_of_arguments[0])

    if _function_name == 'decimalToTwosComplement':
        return cofc_decimal_to_twos_complement(_list_of_arguments[0], int(_list_of_arguments[1]))

    if _function_name == 'decimalToOnesComplement':
        return cofc_decimal_to_ones_complement(_list_of_arguments[0], int(_list_of_arguments[1]))

    if _function_name == 'randDecimal':
        return cofc_generate_random_decimal(_list_of_arguments[0], _list_of_arguments[1])

    if _function_name == 'decimalToSignMagnitude':
        return cofc_convert_decimal_to_sign_magnitude(int(_list_of_arguments[0]), int(_list_of_arguments[1]))

    if _function_name == 'randBinary':
        return cofc_generate_random_binary(int(_list_of_arguments[0]), int(_list_of_arguments[1]), int(_list_of_arguments[2]))

    if _function_name == 'randHex':
        return cofc_generate_random_hexadecimal(int(_list_of_arguments[0]), int(_list_of_arguments[1]))

    if _function_name == 'hexToBinary':
        return cofc_convert_hexadecimal_to_binary(_list_of_arguments[0])

    if _function_name == 'hexToDecimal':
        return cofc_convert_hexadecimal_to_decimal(_list_of_arguments[0])

    if _function_name == 'binaryToDecimal':
        return cofc_convert_binary_to_decimal(_list_of_arguments[0])

    if _function_name == 'decimalToUnsigned':
        return cofc_convert_decimal_to_unsigned_binary(int(_list_of_arguments[0]))

    if _function_name == 'binaryToHex':
        return cofc_convert_binary_to_hex(_list_of_arguments[0])



all_registers = ["s0", "s1", "s2", "s3", "s4", "s5", "s6", "s7",
                 "t0", "t1", "t2", "t3", "t4", "t5", "t6", "t7"]

all_registers_s = ["s0", "s1", "s2"]

all_registers_mapping = {"s0": cofc_decimal_to_twos_complement(16, 5), "s1": cofc_decimal_to_twos_complement(17, 5),
                         "s2": cofc_decimal_to_twos_complement(18, 5), "s3": cofc_decimal_to_twos_complement(19, 5),
                         "s4": cofc_decimal_to_twos_complement(20, 5), "s5": cofc_decimal_to_twos_complement(21, 5),
                         "s6": cofc_decimal_to_twos_complement(22, 5), "s7": cofc_decimal_to_twos_complement(23, 5),
                         "t0": cofc_decimal_to_twos_complement(8, 5), "t1": cofc_decimal_to_twos_complement(9, 5),
                         "t2": cofc_decimal_to_twos_complement(10, 5), "t3": cofc_decimal_to_twos_complement(11, 5),
                         "t4": cofc_decimal_to_twos_complement(12, 5), "t5": cofc_decimal_to_twos_complement(13, 5),
                         "t6": cofc_decimal_to_twos_complement(14, 5), "t7": cofc_decimal_to_twos_complement(15, 5)}


class Mips_instruction:
    def __init__(self, _inst_name, _inst_op, _inst_fun, _inst_type):
        self.inst_name = _inst_name
        self.inst_op = _inst_op
        self.inst_fun = _inst_fun
        self.inst_type = _inst_type
    def get_mips_inst(self, rs, rt, rd, imm):
        if self.inst_type == "R":
            return self.inst_name + " $" + rd + ", $" + rs + ", $" + rt
        elif self.inst_type == "I":
            if self.inst_name == "sw" or self.inst_name == "lw":
                return self.inst_name + " $" + rt + ", " + str(imm) + "($" + rs + ")"
            else:
                return self.inst_name + " $" + rt + ", $" + rs + ", " + str(imm)

    def get_binary_inst(self, rs, rt, rd, imm):
        if self.inst_type == "R":
            return self.inst_op + ' ' + all_registers_mapping[rs][2:] + ' ' + all_registers_mapping[rt][2:] + ' ' + all_registers_mapping[rd][2:] + ' 00000 ' + self.inst_fun
        elif self.inst_type == "I":
            return self.inst_op + ' ' + all_registers_mapping[rs][2:] + ' ' + all_registers_mapping[rt][2:] + ' ' + cofc_decimal_to_twos_complement(imm, 16)[2:]

all_instructions = [Mips_instruction("add", "000000", "100000", "R"),
                    Mips_instruction("sub", "000000", "100010", "R"),
                    Mips_instruction("addi", "001000", "", "I"),
                    Mips_instruction("and", "000000", "100100", "R"),
                    Mips_instruction("andi", "001100", "", "I"),
                    Mips_instruction("or", "000000", "100101", "R"),
                    Mips_instruction("ori", "001101", "", "I"),
                    Mips_instruction("slt", "000000", "101010", "R"),
                    Mips_instruction("slti", "001010", "", "I"),
                    Mips_instruction("lw", "100011", "", "I"),
                    Mips_instruction("sw", "101011", "", "I")]

@csrf_exempt
def my_questions(request):

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')


    if request.is_ajax() and (request.POST.get('btnType') == 'delete_saved_question_student'):
        Saved_Questions.objects.get(id=request.POST.get('question_id')).delete()
        data = {'Result': 'Deleted'}
        return render_to_json_response(data)


    template = loader.get_template('main/my_questions.html')

    # here, we return all unique semesters
    #
    all_questions = Saved_Questions.objects.filter(user_id=request.user.id)

    print(request.user.id)
    print(all_questions)

    context = {
        "all_questions": all_questions,
    }
    return HttpResponse(template.render(context))

@csrf_exempt
def structure(request):
    if request.is_ajax() and (request.POST.get('btnType') == 'get_topics'):
        all_topics = Topic.objects.filter(week_id_id=request.POST.get('week_id'))

        all_topics_sent = []

        for topic in all_topics:
            curr_topic = {}
            curr_topic['title'] = topic.topic_title
            curr_topic['id'] = topic.id
            all_topics_sent.append(curr_topic)

        data = {'all_topics_sent': all_topics_sent}
        return render_to_json_response(data)

    if request.is_ajax() and (request.POST.get('btnType') == 'get_weeks'):
        all_weeks = Week.objects.filter(semester=request.POST.get('semester'))

        all_weeks_sent = []

        for week in all_weeks:
            curr_week = {}
            curr_week['title'] = week.week_title
            curr_week['id'] = week.id
            all_weeks_sent.append(curr_week)

        data = {'all_weeks_sent': all_weeks_sent}
        return render_to_json_response(data)


    template = loader.get_template('main/structure.html')

    # here, we return all unique semesters
    #
    all_semesters = Week.objects.all()

    my_set = set()

    for sem in all_semesters:
        my_set.add(sem.semester)

    all_semesters = list(my_set)

    context = {
        "all_semesters": all_semesters,
    }
    return HttpResponse(template.render(context))

class Question_Answer_Class:
    def __init__(self, _question):
        self.question = _question

    def add_answer(self, _answer):
        self.answer = _answer

class Answer_Class:
    def __init__(self, _element_type, _element_style, _id, _repeat_value, _python_generated_id):
        self.element_type = _element_type
        self.element_style = _element_style
        self.id = _id
        self.repeat_value = _repeat_value
        self.python_generated_id = _python_generated_id
        self.existing_value = ''
        self.placeholder = ''

    def set_placeholder(self, _placeholder):
        self.placeholder = _placeholder

    def set_existing_value(self, _existing_value):
        self.existing_value = _existing_value

class Question_Class:
    def __init__(self, _question_title, _element_type, _element_style, _id):
        self.question_title = _question_title
        self.element_type = _element_type
        self.element_style = _element_style
        self.id = _id

@csrf_exempt
def update_password(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')

    if request.is_ajax() and request.user.is_authenticated() and (request.POST.get('btnType') == 'update_password'):
        request.user.set_password(request.POST.get('password'))
        request.user.save()
        data = {'res': 'it worked and auth'}
        return render_to_json_response(data)

    template = loader.get_template('main/change_pass.html')
    context = {
        "full_name": request.session['full_name'],
    }
    return HttpResponse(template.render(context))

@csrf_exempt
def assigment_id_method(request, assignment_id):

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
        #return csci250_login(request)

    if request.is_ajax() and request.user.is_authenticated() and (request.POST.get('btnType') == 'csci_logout'):
        logout(request)
        data = {'res': 'it worked and auth'}
        return render_to_json_response(data)

    if request.is_ajax() and request.user.is_authenticated() and (request.POST.get('btnType') == 'csci_save_answers'):
        all_answers_sent = json.loads(request.POST.get('all_answers'))

        for ans_id in all_answers_sent:
            # Try to get entry if already exists
            #
            try:
                student_answers = Student_assignment_answers.objects.get(student_id=int(request.user.id),
                                                                         assignment_id=int(assignment_id),
                                                                         question_python_generated_id=ans_id)

                student_answers.student_answer = all_answers_sent[ans_id]
                student_answers.last_submit_date_time=datetime.datetime.now()

                student_answers.save()

            except Student_assignment_answers.DoesNotExist:
                # Entry doesn't exist, if user answer is '' (or no answer, don't create a new record)
                #
                if all_answers_sent[ans_id] == '':
                    continue

                new_answer = Student_assignment_answers(student_id=int(request.user.id),
                                                        assignment_id=int(assignment_id),
                                                        question_python_generated_id=ans_id,
                                                        student_answer=all_answers_sent[ans_id],
                                                        last_submit_date_time=datetime.datetime.now())
                new_answer.save()

        data = {'res': 'it worked and auth'}
        return render_to_json_response(data)

    last_saved_date_time = None

    curr_assignment = Assignments.objects.get(id=assignment_id)

    all_questions_answers = Assignment_question.objects.order_by('question_order').filter(assignment_id=assignment_id)

    all_questions_answers_array = []

    seed(assignment_id)

    for curr_item in all_questions_answers:

        for rep_instance in range(curr_item.repeat):

            exec (curr_item.python_code)

            curr_question_text = ''

            myS = curr_item.title.split('***')

            # If there is no '***' in our question
            #
            if len(myS) == 1:
                curr_question_text = myS[0]
            else:
                # Loop through the number of things ***here*** in our question
                #
                for numOfVariables in range(len(myS) / 2):

                    if ',,' not in myS[numOfVariables * 2 + 1]:
                        myS[numOfVariables * 2 + 1] = '<span style="color: indianred;">' + str(eval(myS[numOfVariables * 2 + 1])) + '</span>'
                    elif myS[numOfVariables * 2 + 1].split(',,')[0] == '-1':
                        # We only execute the function here
                        # #
                        pass
                    else:
                        pass

                curr_question_text = ''.join(myS)

            new_question = Question_Class(curr_question_text,
                                          curr_item.element_type,
                                          curr_item.element_style,
                                          curr_item.id)

            new_question_answer = Question_Answer_Class(new_question)

            curr_answer = Assignment_answer.objects.get(question_id=curr_item.id)

            python_generated_id = 'answer_id_' + str(curr_answer.id) + '_repeat_' + str(rep_instance)

            new_answer = Answer_Class(curr_answer.answer_element_type,
                                      curr_answer.answer_element_style,
                                      curr_answer.id,
                                      rep_instance,
                                      python_generated_id)

            new_answer.set_placeholder(curr_answer.placeholder)

            # Check if there's already an existing answer, saved by the user previously
            #
            try:
                student_answers = Student_assignment_answers.objects.get(student_id=int(request.user.id),
                                                                         assignment_id=int(assignment_id),
                                                                         question_python_generated_id=python_generated_id)


                new_answer.set_existing_value(student_answers.student_answer)
                last_saved_date_time = student_answers.last_submit_date_time

            except Student_assignment_answers.DoesNotExist:
                new_answer.set_existing_value('')


            # Add answer to current 'question_answer' instance
            #
            new_question_answer.add_answer(new_answer)


            all_questions_answers_array.append(new_question_answer)


    # Here, we get all the saved answers from the database
    #



    template = loader.get_template('main/assignments_open.html')
    context = {
        "last_saved_date_time": last_saved_date_time,
        "full_name": request.session['full_name'],
        "assignment_num": curr_assignment.assignment_short_title,
        "curr_assignment": curr_assignment,
        "all_questions_answers_array": all_questions_answers_array,
    }
    return HttpResponse(template.render(context))

def index(request, _year = '2017', _semester = 'spring'):

    if request.is_ajax() and (request.POST.get('btnType') == 'save_question_student'):
        new_question_saved = Saved_Questions(question_content=request.POST.get('all_div_content'),
                                             time_stamp=request.POST.get('date_time'),
                                             user_id=request.user.id)
        new_question_saved.save()

        data = {'res': 'it worked!'}
        return render_to_json_response(data)


    if request.is_ajax() and (request.POST.get('btnType') == 'save_image'):

        #pic = cStringIO.StringIO()
        image_string = cStringIO.StringIO(base64.b64decode(request.POST['img_content']))
        image = Image.open(image_string)
        image.load()

        image = image.convert("RGB")

        print (image)

        image.save("aaa.jpg", image.format, quality=100)


        data = {'res': 'it worked and auth'}
        return render_to_json_response(data)

    if request.is_ajax() and request.user.is_authenticated() and (request.POST.get('btnType') == 'update_audio_history'):
        new_entry = Audio_play_history(user_id_id=request.user.id,
                                       audio_id=request.POST.get('audio_id'),
                                       action=request.POST.get('action'),
                                       time_seconds=request.POST.get('time_in_seconds'),
                                       date_time=request.POST.get('date_formatted'))
        new_entry.save()

        data = {'res': 'it worked and auth'}
        return render_to_json_response(data)

    if request.is_ajax() and request.user.is_authenticated() and (request.POST.get('btnType') == 'csci_logout'):
        logout(request)
        data = {'res': 'it worked and auth'}
        return render_to_json_response(data)

    semester_value = str(_year).lower() + str(_semester).lower()

    if request.is_ajax() and (request.POST.get('btnType') == 'get_lesson'):
        all_lesson_items = Lesson_items.objects.filter(item_id = request.POST.get('lesson_id'))

        all_lessons = []
        for el in all_lesson_items:
            curr_lesson_item = {}
            curr_lesson_item['text'] = el.lesson_item_text
            curr_lesson_item['stop_after'] = el.lesson_item_stop_after
            curr_lesson_item['append_at_once'] = el.lesson_item_append_at_once
            curr_lesson_item['duration'] = el.lesson_item_duration
            all_lessons.append(curr_lesson_item)

        data = {'allItemsSent': all_lessons}
        return render_to_json_response(data)

    if request.is_ajax() and (request.POST.get('btnType') == 'getQuestionsAnswers'):
        try:
            allItemsSent = []
            allQuestionsAnswers = QuizQuestion.objects.filter(subItem_id=request.POST.get('idSent'))

            for el in allQuestionsAnswers:
                for numOfRepetition in range(int(el.repeat)):

                    exec(el.python_code)

                    curr_question = {}
                    allCandidates = []

                    # This dictionary will maintain the current variables and their current values
                    #
                    placeholderValues = {}

                    # Replace placeholders with correct values
                    #
                    myS = el.questionText.split('***')


                    # If there is no '***' in our question
                    #
                    if len(myS) == 1:
                        curr_question['question'] = el.questionText
                    else:
                        # Loop through the number of things ***here*** in our question
                        #
                        for numOfVariables in range(len(myS)/2):

                            if myS[numOfVariables * 2 + 1].split(',')[0] == 'variable':
                                myS[numOfVariables * 2 + 1] = str(eval(myS[numOfVariables * 2 + 1].split(',')[1]))
                            elif ',,' not in myS[numOfVariables * 2 + 1]:
                                myS[numOfVariables * 2 + 1] = '<span style="color: indianred;">' + str(eval(myS[numOfVariables * 2 + 1])) + '</span>'
                            elif myS[numOfVariables * 2 + 1].split(',,')[0] == '-1':
                                # We only execute the function here
                                #
                                pass
                            else:
                                function_name = myS[numOfVariables * 2 + 1].split(',,')[1].split('(')[0]
                                list_of_arguments = myS[numOfVariables * 2 + 1].split(',,')[1][len(function_name)+1:-1].split(',')
                                placeholderValues[myS[numOfVariables * 2 + 1].split(',,')[0]] = execute_function(function_name, list_of_arguments)
                                myS[numOfVariables * 2 + 1] = str(placeholderValues[myS[numOfVariables * 2 + 1].split(',,')[0]])

                    curr_question['question'] = ''.join(myS)

                ######

                    myC = el.candidateAnswer1.split('***')
                    # The following if statement will be true if there is '***something***' in el.candidateAnswer1
                    #
                    if len(myC) == 3:
                        # Separate by double commas
                        #
                        all_components = myC[1].split(',,')

                        # If there's no double commas
                        #
                        if len(all_components) == 1:
                            allCandidates.append(eval(myC[1]))
                        else:
                            function_name = all_components[1].split('(')[0]
                            list_of_arguments = all_components[1][len(function_name)+1:-1].split(',')

                            # replace all ^something with values stored in placeholder
                            #
                            for num, argument in enumerate(list_of_arguments):
                                if '^' in argument:
                                    list_of_arguments[num] = placeholderValues[argument.replace('^', '')]

                            allCandidates.append(execute_function(function_name, list_of_arguments))

                    elif el.candidateAnswer1 != '':
                        allCandidates.append(el.candidateAnswer1)

                    ######

                    myC = el.candidateAnswer2.split('***')
                    # The following if statement will be true if there is '***something***' in el.candidateAnswer2
                    #
                    if len(myC) == 3:
                        # Separate by double commas
                        #
                        all_components = myC[1].split(',,')

                        # If there's no double commas
                        #
                        if len(all_components) == 1:
                            allCandidates.append(eval(myC[1]))
                        else:
                            function_name = all_components[1].split('(')[0]
                            list_of_arguments = all_components[1][len(function_name)+1:-1].split(',')

                            # replace all ^something with values stored in placeholder
                            #
                            for num, argument in enumerate(list_of_arguments):
                                if '^' in argument:
                                    list_of_arguments[num] = placeholderValues[argument.replace('^', '')]


                            allCandidates.append(execute_function(function_name, list_of_arguments))

                    elif el.candidateAnswer2 != '':
                        allCandidates.append(el.candidateAnswer2)

                    #####

                    myC = el.candidateAnswer3.split('***')
                    # The following if statement will be true if there is '***something***' in el.candidateAnswer3
                    #
                    if len(myC) == 3:
                        # Separate by double commas
                        #
                        all_components = myC[1].split(',,')

                        # If there's no double commas
                        #
                        if len(all_components) == 1:
                            allCandidates.append(eval(myC[1]))
                        else:
                            function_name = all_components[1].split('(')[0]
                            list_of_arguments = all_components[1][len(function_name)+1:-1].split(',')

                            # replace all ^something with values stored in placeholder
                            #
                            for num, argument in enumerate(list_of_arguments):
                                if '^' in argument:
                                    list_of_arguments[num] = placeholderValues[argument.replace('^', '')]


                            allCandidates.append(execute_function(function_name, list_of_arguments))

                    elif el.candidateAnswer3 != '':
                        allCandidates.append(el.candidateAnswer3)

                    ######

                    myC = el.candidateAnswer4.split('***')
                    # The following if statement will be true if there is '***something***' in el.candidateAnswer4
                    #
                    if len(myC) == 3:
                        # Separate by double commas
                        #
                        all_components = myC[1].split(',,')

                        # If there's no double commas
                        #
                        if len(all_components) == 1:
                            allCandidates.append(eval(myC[1]))
                        else:
                            function_name = all_components[1].split('(')[0]
                            list_of_arguments = all_components[1][len(function_name)+1:-1].split(',')

                            # replace all ^something with values stored in placeholder
                            #
                            for num, argument in enumerate(list_of_arguments):
                                if '^' in argument:
                                    list_of_arguments[num] = placeholderValues[argument.replace('^', '')]


                            allCandidates.append(execute_function(function_name, list_of_arguments))

                    elif el.candidateAnswer4 != '':
                        allCandidates.append(el.candidateAnswer4)

                    shuffle(allCandidates)
                    curr_question['all_candidates'] = allCandidates
                    curr_question['type'] = el.quizType
                    if el.quizType == 'input1':
                        curr_question['placeholder'] = el.candidateAnswer1

                    corrAns = el.correctAnswer.split('***')
                    # The following if statement will be true if there is '***something***' in el.correctAnswer
                    #
                    if len(corrAns) == 3:
                        # Separate by double commas
                        #
                        all_components = corrAns[1].split(',,')

                        # If there's no double commas
                        #
                        if len(all_components) == 1:
                            curr_question['correct_answer'] = eval(corrAns[1])
                        else:
                            function_name = all_components[1].split('(')[0]
                            list_of_arguments = all_components[1][len(function_name)+1:-1].split(',')

                            # replace all ^something with values stored in placeholder
                            #
                            for num, argument in enumerate(list_of_arguments):
                                if '^' in argument:
                                    list_of_arguments[num] = placeholderValues[argument.replace('^', '')]


                            curr_question['correct_answer'] = execute_function(function_name, list_of_arguments)
                            placeholderValues[all_components[0]] = curr_question['correct_answer']

                            #print(function_name, list_of_arguments, "correct answer", curr_question['correct_answer'])

                    else:
                        curr_question['correct_answer'] = el.correctAnswer

                    allItemsSent.append(curr_question)

            shuffle(allItemsSent)

            data = {'allItemsSent': allItemsSent}
            return render_to_json_response(data)
        except Exception as e:
            print e
            data = {'allItemsSent': 'Failed'}
            return render_to_json_response(data)

    all_final_exams = Final_Exam.objects.order_by('order').all()

    all_weeks = Week.objects.filter(semester=semester_value)

    all_unique_sections = My_User.objects.order_by().values('user_section').distinct()
    print(all_unique_sections)

    data_sent_test = []
    data_sent = []

    for curr_week in all_weeks:
        curr_item = []
        curr_item_class = []

        curr_item.append(curr_week.week_title)

        myTemp = MyItem()
        myTemp.type = "Week"
        myTemp.value = curr_week.week_title
        curr_item_class.append(myTemp)

        all_topics = Topic.objects.filter(week_id_id=curr_week.id).order_by('topic_date')

        for curr_topic in all_topics:

            curr_item.append(str(calendar.day_name[curr_topic.topic_date.weekday()]) + "(" + str(curr_topic.topic_date) + ")" + ": " + curr_topic.topic_title)

            myTemp = MyItem()
            myTemp.type = "Topic"
            myTemp.value = str(calendar.day_name[curr_topic.topic_date.weekday()]) + "(" + str(curr_topic.topic_date) + ")" + ": " + curr_topic.topic_title
            curr_item_class.append(myTemp)

            all_items = Item.objects.filter(topic_id=curr_topic.id)

            for curr_ent in all_items:
                myTemp = MyItem()
                myTemp.type = "Item"
                # interactive lesson
                #
                myTemp.subType = curr_ent.type
                # ends here
                myTemp.value = curr_ent.item_content
                myTemp.id = curr_ent.id
                myTemp.expand = curr_ent.expand

                all_sub_items = SubItem.objects.order_by('subItem_order').filter(item_id=curr_ent.id)
                for curr_sub_item in all_sub_items:
                    mySubItem = SubItemClass(_id=curr_sub_item.id, _title=curr_sub_item.subItem_title, _category=curr_sub_item.subItem_category, _show=curr_sub_item.show, _link=curr_sub_item.subItem_link)
                    myTemp.subItems.append(mySubItem)

                curr_item_class.append(myTemp)

        data_sent.append(curr_item)
        data_sent_test.append(curr_item_class)

    if request.user.is_authenticated():
        template = loader.get_template('main/home_in.html')
        context = {
            "data_sent": data_sent,
            "all_weeks": all_weeks,
            "data_sent_test": data_sent_test,
            "all_final_exams": all_final_exams,
            "full_name": request.session['full_name'],
        }
    else:
        template = loader.get_template('main/home.html')
        context = {
            "data_sent": data_sent,
            "all_weeks": all_weeks,
            "data_sent_test": data_sent_test,
            "all_final_exams": all_final_exams,
        }


    return HttpResponse(template.render(context, request))


@csrf_exempt
def grade_assignment_open(request, ass_id, section_id, student_id):

    if request.user.is_superuser:

        student_object = User.objects.get(id=student_id)
        student_name = student_object.first_name + ' ' + student_object.last_name

        ##
        curr_assignment = Assignments.objects.get(id=ass_id)
        assignment_title = curr_assignment.assignment_title

        all_questions_answers = Assignment_question.objects.order_by('question_order').filter(assignment_id=ass_id)

        all_questions_answers_array = []

        seed(ass_id)

        for curr_item in all_questions_answers:

            for rep_instance in range(curr_item.repeat):

                exec (curr_item.python_code)

                myS = curr_item.title.split('***')

                # If there is no '***' in our question
                #
                if len(myS) == 1:
                    curr_question_text = myS[0]
                else:
                    # Loop through the number of things ***here*** in our question
                    #
                    for numOfVariables in range(len(myS) / 2):

                        if ',,' not in myS[numOfVariables * 2 + 1]:
                            myS[numOfVariables * 2 + 1] = '<span style="color: indianred;">' + str(
                                eval(myS[numOfVariables * 2 + 1])) + '</span>'
                        elif myS[numOfVariables * 2 + 1].split(',,')[0] == '-1':
                            # We only execute the function here
                            # #
                            pass
                        else:
                            pass

                    curr_question_text = ''.join(myS)

                new_question = Question_Class(curr_question_text,
                                              curr_item.element_type,
                                              curr_item.element_style,
                                              curr_item.id)

                new_question_answer = Question_Answer_Class(new_question)

                curr_answer = Assignment_answer.objects.get(question_id=curr_item.id)

                python_generated_id = 'answer_id_' + str(curr_answer.id) + '_repeat_' + str(rep_instance)

                new_answer = Answer_Class(curr_answer.answer_element_type,
                                          curr_answer.answer_element_style,
                                          curr_answer.id,
                                          rep_instance,
                                          python_generated_id)

                new_answer.set_placeholder(curr_answer.placeholder)

                # Check if there's already an existing answer, saved by the user previously
                #
                try:
                    student_answers = Student_assignment_answers.objects.get(student_id=int(student_id),
                                                                             assignment_id=int(ass_id),
                                                                             question_python_generated_id=python_generated_id)

                    new_answer.set_existing_value(student_answers.student_answer)


                except Student_assignment_answers.DoesNotExist:
                    new_answer.set_existing_value('')

                # Add answer to current 'question_answer' instance
                #
                new_question_answer.add_answer(new_answer)

                all_questions_answers_array.append(new_question_answer)

        template = loader.get_template('main/grade_assignments_open.html')

        context = {
            "full_name": request.session['full_name'],
            "assignment_num": curr_assignment.assignment_short_title,
            "curr_assignment": curr_assignment,
            "assignment_title": assignment_title,
            "all_questions_answers_array": all_questions_answers_array,
            'student_name': student_name,
        }
        return HttpResponse(template.render(context))
    else:
        return csci250_login(request)


    #defined function to list sections
def grade_assignments_sections(request, ass_id):
    if request.user.is_superuser: #why does this conditional need to be here? if the user isn't superuser, then they
        #should not have the grade assignments option anyway

        all_sections = Section.objects.values('section_title','id')


        template = loader.get_template('main/grade_assignments_sections.html')

        context = {

            "all_sections" : all_sections,
        }

        return HttpResponse(template.render(context))

@csrf_exempt
def grade_assignments_students(request, ass_id, section_id):
    if request.user.is_superuser:
        #only want all_students to refer to students inside of section_id
        #so if student.user_section matches the section_title of section_id, then create this dictionary

        #get section title from section id;
        section = Section.objects.get(id=section_id).section_title
        print(section)


        # then get correct subset of students from my_user table
        correctStudents = My_User.objects.filter(user_section=section)

        all_students_list = []
        for student in correctStudents:
            student_dictionary = {}
            currentStudent = User.objects.get(id = student.user_id)
            student_dictionary['first_name'] = currentStudent.first_name
            student_dictionary['last_name'] = currentStudent.last_name
            student_dictionary['id'] = currentStudent.id
            all_students_list.append(student_dictionary)

        #by looking at the user_section field,
        # Then get these students' first and last name from the User table

        #all_students = User.objects.values('first_name', 'last_name','id')

        template = loader.get_template('main/grade_assignments_students.html')

        context = {
            "full_name": request.session['full_name'],
            "all_students": all_students_list,
        }
        return HttpResponse(template.render(context))
    else:
        return csci250_login(request)

@csrf_exempt
def grade_assignments(request):
    if request.user.is_superuser:
        all_assignments = Assignments.objects.order_by('assignment_order').all()
        template = loader.get_template('main/grade_assignments.html')

        context = {
            "full_name": request.session['full_name'],
            "all_assignments": all_assignments,
        }
        return HttpResponse(template.render(context))
    else:
        return csci250_login(request)

@csrf_exempt
def assignments(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')

    if request.is_ajax() and request.user.is_authenticated() and (request.POST.get('btnType') == 'csci_logout'):
        logout(request)
        data = {'res': 'it worked and auth'}
        return render_to_json_response(data)

    if request.user.is_authenticated():
        all_assignments = Assignments.objects.order_by('assignment_order').all()

        template = loader.get_template('main/assignments.html')

        context = {
            "full_name": request.session['full_name'],
            "all_assignments": all_assignments,
        }
        return HttpResponse(template.render(context))
    else:
        return csci250_login(request)


@csrf_exempt

def create_ass(request):
    if request.is_ajax() and (request.POST.get('btnType') == 'update_assignment'):
        # Check if title exists
        #
        try:
            data = {}
            curr_assignment = Assignments.objects.filter(assignment_title=request.POST.get('assignment_title'))

            all_questions = json.loads(request.POST.get('all_q'))

            #print len(all_questions)

            if len(curr_assignment) == 0:
                new_assignment = Assignments(assignment_title=request.POST.get('assignment_title'))
                new_assignment.save()

                for num, question in enumerate(all_questions):
                    print ('**')
                    print (question)
                    print ('**')
                    if question['question_type'] == 'title':
                        new_q = Assignment_question(question_title=question['question_title'],
                                                    question_type='title',
                                                    question_order=num,
                                                    question_detail_id=-1,
                                                    assignment_id=new_assignment.id)
                        new_q.save()

                    if question['question_type'] == 'multiple4':
                        new_m_q = Assignment_question_mltiple4(python_code=question['python_code'],
                                                               candidateAnswer1=question['choice_1'],
                                                               candidateAnswer2=question['choice_2'],
                                                               candidateAnswer3=question['choice_3'],
                                                               candidateAnswer4=question['choice_4'],
                                                               correctAnswer=question['correct_answer'])
                        new_m_q.save()

                        new_q = Assignment_question(question_title=question['question_title'],
                                                    question_type='multiple4',
                                                    question_order=num,
                                                    question_detail_id=new_m_q.id,
                                                    assignment_id=new_assignment.id)
                        new_q.save()

                return render_to_json_response(data)

                data['res'] = str(new_assignment.id)

            else:
                data['res'] = 'title exists... confusing'

        except Exception as e:
            data = {'res': e.message}

        return render_to_json_response(data)

    template = loader.get_template('main/create_assignment.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


def create_lesson(request):
    all_lesson_items_sent = []
    all_lesson_items = Lesson_items.objects.all()

    for lesson in all_lesson_items:
        all_lesson_items_sent.append(lesson)

    template = loader.get_template('main/create_lesson.html')
    context = {
        "all_items_sent": all_lesson_items_sent
    }
    return HttpResponse(template.render(context, request))


#def cisci250_assignment(request, _assignment_id):
    # verify that the student/user is logged in
    # we can ignore that for now
    #
    # fetch the assignment content from the database, using the variable _assignment_id


@csrf_exempt
def csci250_edit_quiz(request, _question_id):
    if request.is_ajax() and request.user.is_authenticated() and (request.POST.get('btnType') == 'csci_logout'):
        logout(request)
        data = {'res': 'it worked and auth'}
        return render_to_json_response(data)

    if request.is_ajax() and request.user.is_authenticated() and (request.POST.get('btnType') == 'csci_add_question'):
        curr_question = QuizQuestion.objects.get(id=request.POST.get('question_id'), author_id=request.user.id)
        curr_question.questionText=request.POST.get('question_text')
        curr_question.candidateAnswer1=request.POST.get('ans1_input')
        curr_question.candidateAnswer2=request.POST.get('ans2_input')
        curr_question.candidateAnswer3=request.POST.get('ans3_input')
        curr_question.candidateAnswer4=request.POST.get('ans4_input')
        curr_question.correctAnswer=request.POST.get('corr_ans_input')
        curr_question.quizType=request.POST.get('question_type')
        curr_question.python_code=request.POST.get('python_code')
        curr_question.repeat=request.POST.get('repeat_input')
        curr_question.subItem_id=request.POST.get('subitem_id')
        curr_question.save()

        data = {'id': str(curr_question.id)}
        return render_to_json_response(data)

    if request.is_ajax() and request.user.is_authenticated() and (request.POST.get('btnType') == 'csci_delete_question'):
        QuizQuestion.objects.get(id=request.POST.get('question_id'), author_id=request.user.id).delete()
        data = {'res': 'it worked'}
        return render_to_json_response(data)

    if request.is_ajax() and request.user.is_authenticated() and (request.POST.get('btnType') == 'csci_copy_question'):
        curr_question = QuizQuestion.objects.get(id=request.POST.get('question_id'), author_id=request.user.id)
        curr_question.pk = None
        curr_question.save()
        data = {'id': str(curr_question.id)}
        return render_to_json_response(data)


    curr_question_from_db = QuizQuestion.objects.get(author_id=request.user.id, id=_question_id)

    if request.is_ajax() and request.user.is_authenticated() and (request.POST.get('btnType') == 'getQuestionsAnswers'):
        allItemsSent = []

        try:

            for numOfRepetition in range(int(curr_question_from_db.repeat)):

                exec curr_question_from_db.python_code

                curr_question = {}
                allCandidates = []

                # This dictionary will maintain the current variables and their current values
                #
                placeholderValues = {}

                # Replace placeholders with correct values
                #
                myS = curr_question_from_db.questionText.split('***')

                # If there is no '***' in our question
                #
                if len(myS) == 1:
                    curr_question['question'] = curr_question_from_db.questionText
                else:
                    # Loop through the number of things ***here*** in our question
                    #
                    for numOfVariables in range(len(myS)/2):

                        if myS[numOfVariables * 2 + 1].split(',')[0] == 'variable':
                            myS[numOfVariables * 2 + 1] = str(eval(myS[numOfVariables * 2 + 1].split(',')[1]))
                        elif ',,' not in myS[numOfVariables * 2 + 1]:
                            myS[numOfVariables * 2 + 1] = '<span style="color: indianred;">' + str(eval(myS[numOfVariables * 2 + 1])) + '</span>'
                        elif myS[numOfVariables * 2 + 1].split(',,')[0] == '-1':
                            # We only execute the function here
                            #
                            pass
                        else:
                            function_name = myS[numOfVariables * 2 + 1].split(',,')[1].split('(')[0]
                            list_of_arguments = myS[numOfVariables * 2 + 1].split(',,')[1][len(function_name)+1:-1].split(',')
                            placeholderValues[myS[numOfVariables * 2 + 1].split(',,')[0]] = execute_function(function_name, list_of_arguments)
                            myS[numOfVariables * 2 + 1] = str(placeholderValues[myS[numOfVariables * 2 + 1].split(',,')[0]])

                    curr_question['question'] = ''.join(myS)
                ######

                myC = curr_question_from_db.candidateAnswer1.split('***')
                # The following if statement will be true if there is '***something***' in el.candidateAnswer1
                #
                if len(myC) == 3:
                    # Separate by double commas
                    #
                    all_components = myC[1].split(',,')

                    # If there's no double commas
                    #
                    if len(all_components) == 1:
                        allCandidates.append(eval(myC[1]))
                    else:
                        function_name = all_components[1].split('(')[0]
                        list_of_arguments = all_components[1][len(function_name)+1:-1].split(',')

                        # replace all ^something with values stored in placeholder
                        #
                        for num, argument in enumerate(list_of_arguments):
                            if '^' in argument:
                                list_of_arguments[num] = placeholderValues[argument.replace('^', '')]

                        allCandidates.append(execute_function(function_name, list_of_arguments))

                elif curr_question_from_db.candidateAnswer1 != '':
                    allCandidates.append(curr_question_from_db.candidateAnswer1)

                ######

                myC = curr_question_from_db.candidateAnswer2.split('***')
                # The following if statement will be true if there is '***something***' in el.candidateAnswer2
                #
                if len(myC) == 3:
                    # Separate by double commas
                    #
                    all_components = myC[1].split(',,')

                    # If there's no double commas
                    #
                    if len(all_components) == 1:
                        allCandidates.append(eval(myC[1]))
                    else:
                        function_name = all_components[1].split('(')[0]
                        list_of_arguments = all_components[1][len(function_name)+1:-1].split(',')

                        # replace all ^something with values stored in placeholder
                        #
                        for num, argument in enumerate(list_of_arguments):
                            if '^' in argument:
                                list_of_arguments[num] = placeholderValues[argument.replace('^', '')]


                        allCandidates.append(execute_function(function_name, list_of_arguments))

                elif curr_question_from_db.candidateAnswer2 != '':
                    allCandidates.append(curr_question_from_db.candidateAnswer2)

                #####

                myC = curr_question_from_db.candidateAnswer3.split('***')
                # The following if statement will be true if there is '***something***' in el.candidateAnswer3
                #
                if len(myC) == 3:
                    # Separate by double commas
                    #
                    all_components = myC[1].split(',,')

                    # If there's no double commas
                    #
                    if len(all_components) == 1:
                        allCandidates.append(eval(myC[1]))
                    else:
                        function_name = all_components[1].split('(')[0]
                        list_of_arguments = all_components[1][len(function_name)+1:-1].split(',')

                        # replace all ^something with values stored in placeholder
                        #
                        for num, argument in enumerate(list_of_arguments):
                            if '^' in argument:
                                list_of_arguments[num] = placeholderValues[argument.replace('^', '')]


                        allCandidates.append(execute_function(function_name, list_of_arguments))

                elif curr_question_from_db.candidateAnswer3 != '':
                    allCandidates.append(curr_question_from_db.candidateAnswer3)

                ######

                myC = curr_question_from_db.candidateAnswer4.split('***')
                # The following if statement will be true if there is '***something***' in el.candidateAnswer4
                #
                if len(myC) == 3:
                    # Separate by double commas
                    #
                    all_components = myC[1].split(',,')

                    # If there's no double commas
                    #
                    if len(all_components) == 1:
                        allCandidates.append(eval(myC[1]))
                    else:
                        function_name = all_components[1].split('(')[0]
                        list_of_arguments = all_components[1][len(function_name)+1:-1].split(',')

                        # replace all ^something with values stored in placeholder
                        #
                        for num, argument in enumerate(list_of_arguments):
                            if '^' in argument:
                                list_of_arguments[num] = placeholderValues[argument.replace('^', '')]


                        allCandidates.append(execute_function(function_name, list_of_arguments))

                elif curr_question_from_db.candidateAnswer4 != '':
                    allCandidates.append(curr_question_from_db.candidateAnswer4)

                shuffle(allCandidates)

                curr_question['all_candidates'] = allCandidates
                curr_question['type'] = curr_question_from_db.quizType
                if curr_question_from_db.quizType == 'input1':
                    curr_question['placeholder'] = curr_question_from_db.candidateAnswer1

                corrAns = curr_question_from_db.correctAnswer.split('***')
                # The following if statement will be true if there is '***something***' in el.correctAnswer
                #
                if len(corrAns) == 3:
                    # Separate by double commas
                    #
                    all_components = corrAns[1].split(',,')

                    # If there's no double commas
                    #
                    if len(all_components) == 1:
                        curr_question['correct_answer'] = eval(corrAns[1])
                    else:
                        function_name = all_components[1].split('(')[0]
                        list_of_arguments = all_components[1][len(function_name)+1:-1].split(',')

                        # replace all ^something with values stored in placeholder
                        #
                        for num, argument in enumerate(list_of_arguments):
                            if '^' in argument:
                                list_of_arguments[num] = placeholderValues[argument.replace('^', '')]

                        curr_question['correct_answer'] = execute_function(function_name, list_of_arguments)
                        placeholderValues[all_components[0]] = curr_question['correct_answer']
                else:
                    curr_question['correct_answer'] = curr_question_from_db.correctAnswer

                allItemsSent.append(curr_question)

            shuffle(allItemsSent)
            data = {'allItemsSent': allItemsSent}
            return render_to_json_response(data)

        except Exception as e:
            print (e)

    template = loader.get_template('main/edit_quiz.html')
    context = {
        'full_name': request.session['full_name'],
        'curr_question': curr_question_from_db,
        'my_is_superuser': request.user.is_superuser,
    }
    return HttpResponse(template.render(context, request))


@csrf_exempt
def csci250_schedule(request):
    all_weeks = Week.objects.all()
    data_sent_test = []
    data_sent = []

    for curr_week in all_weeks:
        curr_item = []
        curr_item_class = []

        curr_item.append(curr_week.week_title)

        myTemp = MyItem()
        myTemp.type = "Week"
        myTemp.id = curr_week.id
        myTemp.value = curr_week.week_title
        curr_item_class.append(myTemp)

        all_topics = Topic.objects.filter(week_id_id=curr_week.id)

        for curr_topic in all_topics:

            curr_item.append(str(calendar.day_name[curr_topic.topic_date.weekday()]) + "(" + str(curr_topic.topic_date) + ")" + ": " + curr_topic.topic_title)

            myTemp = MyItem()
            myTemp.type = "Topic"
            myTemp.id = curr_topic.id
            myTemp.value = str(calendar.day_name[curr_topic.topic_date.weekday()]) + "(" + str(curr_topic.topic_date) + ")" + ": " + curr_topic.topic_title
            curr_item_class.append(myTemp)

            all_items = Item.objects.filter(topic_id=curr_topic.id)

            for curr_ent in all_items:
                myTemp = MyItem()
                myTemp.type = "Item"
                myTemp.value = curr_ent.item_content
                myTemp.id = curr_ent.id
                myTemp.expand = curr_ent.expand

                all_sub_items = SubItem.objects.order_by('subItem_order').filter(item_id=curr_ent.id)
                for curr_sub_item in all_sub_items:
                    mySubItem = SubItemClass(_id=curr_sub_item.id, _title=curr_sub_item.subItem_title, _category=curr_sub_item.subItem_category, _show=curr_sub_item.show, _link=curr_sub_item.subItem_link)
                    myTemp.subItems.append(mySubItem)

                curr_item_class.append(myTemp)

        data_sent.append(curr_item)
        data_sent_test.append(curr_item_class)

    if not request.user.is_superuser:
        return redirect(index)
        data_sent = []
        all_weeks = []
        data_sent_test = []


    template = loader.get_template('main/change_schedule.html')
    context = {
        "data_sent": data_sent,
        "all_weeks": all_weeks,
        "data_sent_test": data_sent_test,
    }
    return HttpResponse(template.render(context, request))



@csrf_exempt
def csci250_sign_up(request):
    if request.is_ajax() and (request.POST.get('btnType') == 'csci_sign_up'):

        user = User.objects.create_user(request.POST.get('email'),
                                        request.POST.get('email'),
                                        request.POST.get('pass'))
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()

        my_user = My_User(user=user,
                          user_section=request.POST.get('section'),
                          active_member=True)
        my_user.save()

        data = {'res': 'User created!'}
        return render_to_json_response(data)


    template = loader.get_template('main/sign_up.html')
    context = {}
    return HttpResponse(template.render(context))

@csrf_exempt
def csci250_login(request):
    if request.is_ajax() and request.user.is_authenticated() and (request.POST.get('btnType') == 'csci_logout'):
        logout(request)
        data = {'res': 'it worked and auth'}
        return render_to_json_response(data)

    if request.is_ajax() and request.user.is_authenticated() and (request.POST.get('btnType') == 'csci_add_question'):
        try:
            new_entry = QuizQuestion(questionText=request.POST.get('question_text'),
                                     repeat=request.POST.get('repeat_input'),
                                     candidateAnswer1=request.POST.get('ans1_input'),
                                     candidateAnswer2=request.POST.get('ans2_input'),
                                     candidateAnswer3=request.POST.get('ans3_input'),
                                     candidateAnswer4=request.POST.get('ans4_input'),
                                     correctAnswer=request.POST.get('corr_ans_input'),
                                     subItem_id=request.POST.get('subitem_id'),
                                    quizType=request.POST.get('question_type'),
                                     python_code=request.POST.get('python_code'),
                                     author_id=request.user.id)
            new_entry.save()
            data = {'id': str(new_entry.id)}
            return render_to_json_response(data)

        except Exception as e:
            print e
            data = {'allItemsSent': 'Failed'}
            return render_to_json_response(data)

    if request.user.is_authenticated() and request.user.is_superuser:

        print ('here...')
        print (type(request.session['full_name']))
        print (request.session['full_name'])

        # Go to contributor page
        #
        template = loader.get_template('main/edit_quiz.html')
        #context = RequestContext(request,
        #                         {
        #                            'full_name': request.session['full_name'],
        #                            'my_is_superuser': request.user.is_superuser,
        #                         })

        context = {
            'full_name': request.session['full_name'],
            'my_is_superuser': request.user.is_superuser,
        }

        return HttpResponse(template.render(context))

    if request.user.is_authenticated() and not request.user.is_superuser:
        return index(request)

    if request.is_ajax() and (request.POST.get('btnType') == 'csci_login'):
        email = request.POST.get('email')
        password = request.POST.get('password')

        currUser = User.objects.filter(username=request.POST.get('email'))
        if len(currUser) == 0:
            data = {'res': 'Username does not exist'}
            return render_to_json_response(data)

        user = authenticate(username=email, password=password)

        print(user)

        if user is None:
            data = {'res': 'Incorrect U or P'}
        else:
            if user.is_active:
                data = {'res': 'it worked and auth'}
                login(request, user)
                request.session['user_id'] = str(user.id)
                request.session['user_email'] = user.username
                request.session['full_name'] = user.first_name + ' ' + user.last_name
            else:
                #print('user inactive - am confused')
                data = {'res': 'user inactive - look into more...'}

        return render_to_json_response(data)


    template = loader.get_template('main/login.html')
    context = {
    }
    return HttpResponse(template.render(context))


@csrf_exempt
def csci250_view_questions(request):
    if request.is_ajax() and request.user.is_authenticated() and (request.POST.get('btnType') == 'csci_logout'):
        logout(request)
        data = {'res': 'it worked and auth'}
        return render_to_json_response(data)

    if request.user.is_authenticated():
        allItemsSent = []

        curr_user_id = str(request.user.id)

        if curr_user_id[-1] == 'L':
            curr_user_id = curr_user_id[:-1]

        all_questions = QuizQuestion.objects.filter(author_id=int(curr_user_id)).order_by('-id')

        for el in all_questions:
            curr_question = {}
            allCandidates = []

            # This dictionary will maintain the current variables and their current values
            #
            placeholderValues = {}

            curr_question['question'] = el
            #curr_question['id'] = el.id
            #curr_question


            #shuffle(allCandidates)
            #curr_question['all_candidates'] = allCandidates
            #curr_question['type'] = el.quizType
            #if el.quizType == 'input1':
            #    curr_question['placeholder'] = el.candidateAnswer1

            #corrAns = el.correctAnswer.split('***')
            # The following if statement will be true if there is '***something***' in el.correctAnswer
            #
            #        curr_question['correct_answer'] = eval(corrAns[1])

            allItemsSent.append(el)

        #shuffle(allItemsSent)

        template = loader.get_template('main/view_questions.html')
        context = {
            'full_name': request.session['full_name'],
            'all_questions': allItemsSent,
            'my_is_superuser': request.user.is_superuser,
        }
        return HttpResponse(template.render(context, request))
    else:
        return redirect(index)



def render_to_json_response(context, **response_kwargs):
    data = json.dumps(context)
    response_kwargs['content_type'] = 'application/json'
    return HttpResponse(data, **response_kwargs)

