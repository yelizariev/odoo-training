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

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        context = self._context or {}
        import time
        time.sleep(1)
        return super(ws_training_attend, self).search(args, offset, limit, order, count=count)

    @api.multi
    def write(self, vals):
        context = self._context or {}
        print vals
        vals['description']='hello overwrote!'
        return super(ws_training_attend, self).write(vals)

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
