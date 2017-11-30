from django.db import models

from django.contrib.auth.models import User

class My_User(models.Model):
    user = models.OneToOneField(User)
    user_section = models.CharField(max_length=50)
    active_member = models.BooleanField()


class Final_Exam(models.Model):
    section_full_title = models.CharField(max_length=200)
    order = models.IntegerField()


class Week(models.Model):
    week_order = models.IntegerField()
    week_title = models.CharField(max_length=600)
    week_start_date = models.DateField()
    semester = models.CharField(max_length=200, default='2017Spring')


class Topic(models.Model):
    topic_order = models.IntegerField()
    topic_title = models.CharField(max_length=200)
    topic_date = models.DateField()
    week_id = models.ForeignKey(Week)


class Section(models.Model):
    section_title = models.CharField(max_length=600)


class Item(models.Model):
    item_order = models.IntegerField()
    item_content = models.CharField(max_length=400)
    topic = models.ForeignKey(Topic)
    type = models.CharField(max_length=40, default="simple_expand")
    expand = models.BooleanField(default=False)


class SubItem(models.Model):
    subItem_order = models.IntegerField()
    subItem_title = models.CharField(max_length=400)
    subItem_category = models.CharField(max_length=200, default='PDF')
    subItem_link = models.CharField(max_length=400)
    subItem_function = models.CharField(max_length=300)
    item = models.ForeignKey(Item)
    show = models.BooleanField(default=True)


class QuizQuestion(models.Model):
    python_code = models.TextField(default='')
    questionText = models.TextField()
    candidateAnswer1 = models.CharField(max_length=200)
    candidateAnswer2 = models.CharField(max_length=200)
    candidateAnswer3 = models.CharField(max_length=200)
    candidateAnswer4 = models.CharField(max_length=200)
    correctAnswer = models.CharField(max_length=200)
    repeat = models.IntegerField(default=1)
    subItem = models.ForeignKey(SubItem)
    quizType = models.CharField(max_length=100, default='multiple4')
    author_id = models.IntegerField(default=-1)


class Saved_Questions(models.Model):
    question_content = models.TextField()
    time_stamp = models.DateTimeField(default=None)
    user = models.ForeignKey(User)



class Lesson_items(models.Model):
    lesson_item_text = models.TextField()
    lesson_item_stop_after = models.BooleanField(default=False)
    lesson_item_append_at_once = models.BooleanField(default=False)
    lesson_item_duration = models.IntegerField()
    item = models.ForeignKey(Item)


class Assignments(models.Model):
    assignment_title = models.CharField(max_length=300)
    assignment_short_title = models.CharField(max_length=100, default='')
    assignment_order = models.IntegerField(default=1)
    assignment_due_date_time = models.DateTimeField(blank=True, null=True)
    assignment_date_tbd = models.BooleanField(default=0)


class Student_assignment_answers(models.Model):
    student = models.ForeignKey(User)
    assignment = models.ForeignKey(Assignments)
    question_python_generated_id = models.CharField(max_length=200)
    student_answer = models.TextField()
    last_submit_date_time = models.DateTimeField(blank=True, null=True)


class Assignment_question(models.Model):
    python_code = models.TextField(default='')
    parent_question_id = models.IntegerField(default=-1)
    repeat = models.IntegerField(default=1)
    title = models.TextField()
    element_type = models.CharField(max_length=200)
    element_style = models.CharField(max_length=300, default='')
    # The type could be multiple4, multiple2, input, for now we can limit to multiple4
    question_order = models.IntegerField()
    question_detail_id = models.IntegerField()
    assignment = models.ForeignKey(Assignments)



class Assignment_answer(models.Model):
    answer_python_code = models.TextField()
    answer_element_type = models.CharField(max_length=100)
    answer_element_style = models.CharField(max_length=300)
    placeholder = models.CharField(max_length=200, default='')
    question = models.ForeignKey(Assignment_question)


class Assignment_question_mltiple4(models.Model):
    python_code = models.TextField(default='')
    candidateAnswer1 = models.CharField(max_length=200)
    candidateAnswer2 = models.CharField(max_length=200)
    candidateAnswer3 = models.CharField(max_length=200)
    candidateAnswer4 = models.CharField(max_length=200)
    correctAnswer = models.CharField(max_length=200)
    assignment_question_id = models.ForeignKey(Assignment_question)


class Audio_play_history(models.Model):
    user_id = models.ForeignKey(User)
    audio_id = models.CharField(max_length=50)
    action = models.CharField(max_length=100)
    time_seconds = models.FloatField()
    date_time = models.DateTimeField(blank=True, null=True)