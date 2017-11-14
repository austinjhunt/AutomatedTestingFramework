from django.shortcuts import render
import functionsFromDB

# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext, loader

from main.models import Week, Topic, Item, SubItem, QuizQuestion

import calendar

from random import shuffle
from random import randint

import json


class Question:
    def __init__(self, _questionText):
        self.id = ''
        self.questionText = _questionText
        self.listOfCandidates = []
        self.correctAnswer = ''
        self.questionType = ''


class SubItemClass:
    def __init__(self, _id, _title, _category):
        self.id = _id
        self.title = _title
        self.category = _category
        self.questions = []


class MyItem:
    def __init__(self):
        self.id = -1
        self.type = None
        self.value = None
        self.subType = None
        self.subItems = []


def page_not_found(request):
    template = loader.get_template('main/home.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))

def twos_comp(val, bits):
    """compute the 2's compliment of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val                         # return positive value as is

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


    if currSplit[1] == 'decimalFromOnesComplement':
        if '^' in currSplit[2]:
            modifiedValue = _placeholderValues[currSplit[2].replace('^', '')]

        # First we check if it's positive; if it is, we simply convert to decimal
        #
        if modifiedValue[2] == '0':
            ans_decimal = int(modifiedValue[2:], 2)
        else:
            # First we swap the 0s with 1s and vice versa
            #
            modifiedValue = modifiedValue.replace('0', 'x')
            modifiedValue = modifiedValue.replace('1', '0')
            modifiedValue = modifiedValue.replace('x', '1')

            # Now we convert to decimal
            #
            ans_decimal = int(modifiedValue[2:], 2) * -1

        _placeholderValues[currSplit[0]] = ans_decimal


    if currSplit[1] == 'decimalFromSignMagnitude':
        if '^' in currSplit[2]:
            modifiedValue = _placeholderValues[currSplit[2].replace('^', '')]
        ans_decimal = int(modifiedValue[3:], 2)
        if modifiedValue[2] == '1':
            ans_decimal = ans_decimal * -1
        _placeholderValues[currSplit[0]] = ans_decimal
        return

    if currSplit[1] == 'decimalFromHex':
        if '^' in currSplit[2]:
            modifiedValue = _placeholderValues[currSplit[2].replace('^', '')]
        _placeholderValues[currSplit[0]] = int(modifiedValue, 16)
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

    if(currSplit[1] == 'randBinary' and len(currSplit) == 5):
        binarySequence = bin(randint(int(currSplit[2]), int(currSplit[3])))
        while len(binarySequence) != (int(currSplit[4]) + 2):
            binarySequence = binarySequence[0:2] + '0' + binarySequence[2:]
        _placeholderValues[currSplit[0]] = binarySequence
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

    if currSplit[1] == 'binaryOnesComplementFromDecimal':
        if '^' in currSplit[2]:
            modifiedValue = _placeholderValues[currSplit[2].replace('^', '')]
            # First we get the binary of the "positve" version of the number
            #
            ans_binary = bin(int(abs(modifiedValue)))
            # Then we make it x number of bits where x is the 4th parameters in our list
            #
            while len(ans_binary) != (int(currSplit[3]) + 2):
                ans_binary = ans_binary[0:2] + '0' + ans_binary[2:]
            # If the number is negative, we flip all bits
            #
            if modifiedValue < 0:
                ans_binary = ans_binary.replace('0', 'x')
                ans_binary = ans_binary.replace('1', '0')
                ans_binary = ans_binary.replace('x', '1')
            ans_binary = '0' + ans_binary[1:]
            _placeholderValues[currSplit[0]] = ans_binary


    if currSplit[1] == 'binarySignMagnitudeFromDecimal':
        if '^' in currSplit[2]:
            modifiedValue = _placeholderValues[currSplit[2].replace('^', '')]
            # First we get the binary of the "positve" version of the number
            #
            ans_binary = bin(int(abs(modifiedValue)))
            # Then we make it x number of bits where x is the 4th parameters in our list
            #
            while len(ans_binary) != (int(currSplit[3]) + 2):
                ans_binary = ans_binary[0:2] + '0' + ans_binary[2:]
            # Finally, we make the MSB 1 if the number is negative, otherwise do nothing
            #
            if modifiedValue < 0:
                ans_binary = ans_binary[0:2] + '1' + ans_binary[3:]

            _placeholderValues[currSplit[0]] = ans_binary

    if(currSplit[1] == 'binary'):
        if '^' in currSplit[2]:
            modifiedValue = _placeholderValues[currSplit[2].replace('^', '')]
            _placeholderValues[currSplit[0]] = bin(int(modifiedValue))
        else:
            _placeholderValues[currSplit[0]] = bin(int(currSplit[2]))


def index(request):
    if request.is_ajax() and (request.POST.get('btnType') == 'getQuestionsAnswers'):
        try:
            allItemsSent = []
            allQuestionsAnswers = QuizQuestion.objects.filter(subItem_id=request.POST.get('idSent'))

            for el in allQuestionsAnswers:
                for numOfRepetition in range(int(el.repeat)):

                    exec(el.python_code)

                    curr_question = {}
                    allCandidates = []

                    placeholderValues = {}
                    # Replace placeholders with correct values
                    #
                    myS = el.questionText.split('***')

                    if len(myS) == 1:
                        curr_question['question'] = el.questionText
                    else:
                        for numOfVariables in range(len(myS)/2):
                            if myS[numOfVariables * 2 + 1].split(',')[0] == 'variable':
                                myS[numOfVariables * 2 + 1] = str(eval(myS[numOfVariables * 2 + 1].split(',')[1]))
                            #returnCorrectValues(myS[numOfVariables*2 + 1], placeholderValues)
                            #myS[numOfVariables*2 + 1] = str(placeholderValues[myS[numOfVariables*2 + 1].split(',')[0]])
                        curr_question['question'] = ''.join(myS)

                    ######

                    myC = el.candidateAnswer1.split('***')
                    if len(myC) == 3:
                        returnCorrectValues(myC[1], placeholderValues)
                        allCandidates.append(placeholderValues['can1Ans'])
                    elif el.candidateAnswer1 != '':
                        allCandidates.append(el.candidateAnswer1)

                    ######

                    myC = el.candidateAnswer2.split('***')
                    if len(myC) == 3:
                        returnCorrectValues(myC[1], placeholderValues)
                        allCandidates.append(placeholderValues['can2Ans'])
                    elif el.candidateAnswer2 != '':
                        allCandidates.append(el.candidateAnswer2)

                    #####

                    myC = el.candidateAnswer3.split('***')
                    if len(myC) == 3:
                        returnCorrectValues(myC[1], placeholderValues)
                        allCandidates.append(placeholderValues['can3Ans'])
                    elif el.candidateAnswer3 != '':
                        allCandidates.append(el.candidateAnswer3)
                    ######

                    myC = el.candidateAnswer4.split('***')
                    if len(myC) == 3:
                        returnCorrectValues(myC[1], placeholderValues)
                        allCandidates.append(placeholderValues['can4Ans'])
                    elif el.candidateAnswer4 != '':
                        allCandidates.append(el.candidateAnswer4)


                    shuffle(allCandidates)
                    curr_question['all_candidates'] = allCandidates
                    curr_question['type'] = el.quizType
                    if el.quizType == 'input1':
                        curr_question['placeholder'] = el.candidateAnswer1

                    corrAns = el.correctAnswer.split('***')
                    # This if statement will be true if there is '***something***' in el.correctAnswer
                    #
                    if len(corrAns) == 3:
                        #returnCorrectValues(corrAns[1], placeholderValues)
                        #curr_question['correct_answer'] = placeholderValues['ans']
                        curr_question['correct_answer'] = eval(corrAns[1])
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

    all_weeks = Week.objects.all()

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

        all_topics = Topic.objects.filter(week_id_id=curr_week.id)

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
                myTemp.value = curr_ent.item_content
                myTemp.id = curr_ent.id

                all_sub_items = SubItem.objects.order_by('subItem_order').filter(item_id=curr_ent.id)
                for curr_sub_item in all_sub_items:
                    mySubItem = SubItemClass(_id=curr_sub_item.id, _title=curr_sub_item.subItem_title, _category=curr_sub_item.subItem_category)
                    myTemp.subItems.append(mySubItem)

                curr_item_class.append(myTemp)

        data_sent.append(curr_item)
        data_sent_test.append(curr_item_class)

    template = loader.get_template('main/home.html')
    context = RequestContext(request,
                             {
                                 "data_sent": data_sent,
                                 "all_weeks": all_weeks,
                                 "data_sent_test": data_sent_test,
                             })
    return HttpResponse(template.render(context))


def render_to_json_response(context, **response_kwargs):
    data = json.dumps(context)
    response_kwargs['content_type'] = 'application/json'
    return HttpResponse(data, **response_kwargs)

