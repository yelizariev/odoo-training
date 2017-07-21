#!/usr/bin/env python
# -*- coding: utf-8 -*-
# WENS FOOD STUFF GROUP Corp.
# Copyright (C) 2014-2020 WENS FOOD GROUP (<http://www.wens.com.cn>).
# Authored by Shengli Hu <hushengli@gmail.com>
import logging

from odoo import models, fields, api


class ws_training_attend(models.Model):
    _name = 'ws.training.attend'
    _description = u'培训签到表'

    user_id = fields.Many2one('res.users', string=u'学员', required=True)
    course_id = fields.Many2one('ws.training.course', string=u'课程', required=True)
    attend_time = fields.Datetime(string=u'签到时间', required=True, help=u'签到时间')
    description = fields.Text(string=u'备注')

    #@api.model
    #def search(self, args, offset=0, limit=None, order=None, count=False):
    #    context = self._context or {}
        #import time
        #time.sleep(1)
    #    return super(ws_training_attend, self).search(args, offset, limit, order, count=count)

    #@api.multi
    #def write(self, vals):
    #    context = self._context or {}
    #    print vals
    #    vals['description']='hello overwrote!'
    #    return super(ws_training_attend, self).write(vals)

    # @api.model
    # def create(self, args, offset=0, limit=None, order=None, count=False):
    #     context = self._context or {}
    #     import time
    #     time.sleep(15)
    #     return super(ws_training_attend, self).search(args, offset, limit, order, count=count)
    #
    # @api.model
    # def unlink(self, args, offset=0, limit=None, order=None, count=False):
    #     context = self._context or {}
    #     import time
    #     time.sleep(15)
    #     return super(ws_training_attend, self).search(args, offset, limit, order, count=count)

class ws_training_course(models.Model):
    _name = 'ws.training.course'
    _description = u'培训课程'

    name = fields.Char(string=u'名称', required=True)
    time_start = fields.Datetime(string=u'开始时间', required=True)
    time_end = fields.Datetime(string=u'结束时间', required=True)
    teacher_id = fields.Many2one('res.users', string=u'讲师', required=True)
    description = fields.Text(string=u'描述')

    #@作者：凌嘉文
    image_course = fields.Binary(string=" ")
    comment_to_teacher =fields.One2many('ws.training.course.comment', 'course_id', string=u"课程评价")
    course_user_id = fields.Many2many('ws.training.class.users')


######@作者：陈旋
class ws_training_class(models.Model):
    _name = 'ws.training.class'
    _description = u'培训班级'

    name = fields.Char(string=u'班名', required=True)
    date_start = fields.Date(string=u'开班时间', required=True)
    date_end = fields.Date(string=u'结班时间', required=True)
    user_ids = fields.One2many("ws.training.class.users", 'class_id', string=u'学员')


class ws_training_class_users(models.Model):
    _name = 'ws.training.class.users'
    _rec_name = "user_id"
    _description = u'班级学员'

    class_id = fields.Many2one('ws.training.class', string=u'班别', required=True)
    user_id = fields.Many2one('res.users', string=u'学员', required=True)
    ######@作者：凌嘉文
    course_id = fields.Many2many('ws.training.course',string=u"所选课程")
    user_email = fields.Char(string="邮箱")
    user_mobile = fields.Char(string="手机")
    user_address = fields.Char(string="地址")
    user_image = fields.Binary(string="照片")

    ######
######

######@作者：凌嘉文
class ws_training_class_comment(models.Model):
    _name = "ws.training.course.comment"
    _description = u"课程评论"

    name = fields.Many2one('ws.training.class.users',string=u"学员姓名", required=True)
    course_id = fields.Many2one('ws.training.course',string=u'所属课程', required=True)
    student_comment = fields.Text(string=u'请写出你的评价')
######