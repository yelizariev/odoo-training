#!/usr/bin/env python
# -*- coding: utf-8 -*-
# WENS FOOD STUFF GROUP Corp.
# Copyright (C) 2014-2020 WENS FOOD GROUP (<http://www.wens.com.cn>).
# Authored by Shengli Hu <hushengli@gmail.com>
from odoo import tools, _
from odoo.modules.module import get_module_resource

# class EmployeeCategory(models.Model):
#
#     _name = "hr.employee.category"
#     _description = "Employee Category"
#
#     name = fields.Char(string="Employee Tag", required=True)
#     color = fields.Integer(string='Color Index')
#     employee_ids = fields.Many2many('hr.employee', 'employee_category_rel', 'category_id', 'emp_id', string='Employees')
#
#     _sql_constraints = [
#         ('name_uniq', 'unique (name)', "Tag name already exists !"),
#     ]
from odoo import models, fields, api
import logging
import os
from odoo.http import request
from jinja2 import Environment, FileSystemLoader
import datetime
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
templateLoader = FileSystemLoader(searchpath=BASE_DIR + "/templates")
env = Environment(loader=templateLoader)

######@作者：cky
class ws_training_attend(models.Model):
    _name = 'ws.training.attend'
    _description = u'培训签到表'

    user_id = fields.Many2one('res.users', string=u'学员', required=True)
    course_id = fields.Many2one('ws.training.course', string=u'课程', required=True)
    attend_time = fields.Datetime(string=u'签到时间', required=True, help=u'签到时间')
    state = fields.Text(string=u'备注')
    singe_state = fields.Selection([('belate', u'迟到'), ('absenteeism', u'缺勤'), (' normal', u'正常')], string=u'签到')

    @api.multi
    @api.onchange('attend_time')
    def time_singe(self):
        """
        :return: 
        """
        source_course = self.env['ws.training.course']
        for o in self:
            if o.course_id.id:
                course_obj = source_course.browse(o.course_id.id)
                if course_obj.time_end < o.attend_time:
                    o.singe_state = 'absenteeism'
                elif course_obj.time_start > o.attend_time:
                   o.singe_state = 'belate'
                else:
                    o.singe_state = 'normal'

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        context = self._context or {}
        return super(ws_training_attend, self).search(args, offset, limit, order, count=count)

    @api.multi
    def write(self, vals):
        context = self._context or {}
        return super(ws_training_attend, self).write(vals)

    @api.model
    def create(self, vals):

        return super(ws_training_attend, self).create(vals)
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
############
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
    get_module_resource


    @api.model
    def _default_image(self):
        image_path = get_module_resource('ws_training', 'static/src/img', 'default_image.png')
        return tools.image_resize_image_big(open(image_path, 'rb').read().encode('base64'))


    # category_ids = fields.Many2many('hr.employee.category', 'employee_category_rel', 'emp_id', 'category_id', string='Tags')
    class_id = fields.Many2one('ws.training.class', string=u'班别', required=True)
    user_id = fields.Many2one('res.users', string=u'学员', required=True)
    ######@作者：凌嘉文
    course_id = fields.Many2many('ws.training.course',string=u"所选课程")
    user_email = fields.Char(string="邮箱")
    user_mobile = fields.Char(string="手机")
    user_address = fields.Char(string="地址")

    user_image = fields.Binary("Photo", default=_default_image, attachment=True,
                          help="This field holds the image used as photo for the employee, limited to 1024x1024px.")
    image_medium = fields.Binary("Medium-sized photo", attachment=True,
                                 help="Medium-sized photo of the employee. It is automatically "
                                      "resized as a 128x128px image, with aspect ratio preserved. "
                                      "Use this field in form views or some kanban views.")
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