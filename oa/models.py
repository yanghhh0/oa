# -*- coding: utf-8 -*-


from django.db import models
from django.utils import timezone


# class ClassInfo(models.Model):
#     # 班级信息表  字段:班级名称
#     name = models.CharField(max_length=20)
#
#     def __str__(self):
#         return self.name
#
#
# class MajorInfo(models.Model):
#     # 专业信息表 字段：专业名称
#     name = models.CharField(max_length=20)
#
#     def __str__(self):
#         return self.name


class Teacher(models.Model):
    # 教师信息表 字段：教师编号，手机号，姓名，邮箱，密码
    uid = models.AutoField(null=False, primary_key=True)
    phone = models.CharField(max_length=11)
    name = models.CharField(max_length=15)
    email = models.EmailField(null=False)
    password = models.CharField(max_length=64)

    class Meta:
        db_table = 'teacher'

    def __str__(self):
        return self.uid


class Student(models.Model):
    # 学生信息表 字段：学号，密码，姓名，学院，专业，班级
    uid = models.BigIntegerField(primary_key=True)
    password = models.CharField(max_length=64)
    name = models.CharField(max_length=16)
    institute = models.CharField(max_length=32)
    major = models.CharField(max_length=32)
    cls = models.CharField(max_length=32)

    class Meta:
        db_table = 'student'

    def __str__(self):
        return self.uid


class Item(models.Model):
    # 课程信息表 字段:课程编号，课程名称，教师编号，课程其余信息
    uid = models.BigAutoField(null=False, primary_key=True)
    name = models.CharField(max_length=15)
    t_uid = models.BigIntegerField(null=False)

    class Meta:
        db_table = 'item'

    def __str__(self):
        return self.uid


class CheckInfo(models.Model):
    # 某次签到的信息
    check_id = models.BigAutoField(null=False, primary_key=True)
    t_uid = models.BigIntegerField(null=False)
    check_time = models.BigIntegerField(null=False)
    checked_count = models.IntegerField(null=False)
    total_count = models.IntegerField(null=False)
    item_id = models.BigIntegerField(null=False)

    class Meta:
        db_table = 'check_info'


class CheckRecord(models.Model):
    # 签到记录
    id = models.BigAutoField(primary_key=True, null=False)
    check_id = models.BigIntegerField(null=False)  # 签到id
    uid = models.BigIntegerField(null=False)  # 签到人id
    check_time = models.BigIntegerField(null=False)  # 签到时间
    check_type = models.IntegerField(null=False)  # 签到方式 1正常签到，2补签
    check_reason = models.TextField(max_length=256, null=True)  # 补签理由

    class Meta:
        db_table = 'check_record'
        unique_together = ('check_id', 'uid')


class StuItem(models.Model):
    # 名单详细
    id = models.BigAutoField(primary_key=True, null=False)
    item_id = models.BigIntegerField(null=False)
    stu_id = models.BigIntegerField(null=False)

    class Meta:
        db_table = 'stu_item'
        unique_together = ('item_id', 'stu_id')


class Course(models.Model):
    # 课程信息
    id = models.BigAutoField(primary_key=True, null=False)
    t_uid = models.BigIntegerField(null=False)
    # 格式为{‘startTime’: 'endTime',}
    time = models.JSONField(null=False)

    class Meta:
        db_table = 'course'


class StuCourse(models.Model):
    # 学生与课程的关系
    id = models.BigAutoField(primary_key=True, null=False)
    c_uid = models.BigIntegerField(null=False)
    uid = models.BigIntegerField(null=False)

    class Meta:
        db_table = 'stu_course'
        unique_together = ('c_uid', 'uid')
