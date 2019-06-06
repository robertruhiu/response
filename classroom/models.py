from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
import random
from separatedvaluesfield.models import SeparatedValuesField


class Subject(models.Model):
    name = models.CharField(max_length=30)
    image = models.CharField(max_length=300,blank=True, null=True)

    def __str__(self):
        return self.name

    def subjectimage(self):
        return self.image

class Quiz(models.Model):
    owner = models.IntegerField(blank=True)
    name = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='quizzes')

    def __str__(self):
        return self.name





class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField('Question', max_length=250)
    codesample = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField('Answer', max_length=255)
    is_correct = models.BooleanField('Correct answer', default=False)

    def __str__(self):
        return self.text


class Student(models.Model):
    user = models.IntegerField(blank=True)
    quizzes = models.ManyToManyField(Quiz, through='TakenQuiz')

    def get_unanswered_questions(self, quiz):
        answered_questions = self.quiz_answers \
            .filter(answer__question__quiz=quiz) \
            .values_list('answer__question__pk', flat=True)

        questions = quiz.questions.exclude(pk__in=answered_questions).order_by('text')
        return questions

    def __str__(self):
        return self.user


class TakenQuiz(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='taken_quizzes')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='taken_quizzes')
    score = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)


class StudentAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='quiz_answers')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='+')
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE)


class RandomQuiz(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='tempquiz')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='tempanswers')
    questions =SeparatedValuesField(null=True,max_length=150,token=',')
