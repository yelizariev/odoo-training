# -*- coding: utf-8 -*-

import logging
import os
import sys
import time
from jinja2 import Environment, FileSystemLoader
from odoo import http
from odoo.http import request
import datetime

reload(sys)
sys.setdefaultencoding('utf8')

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
templateLoader = FileSystemLoader(searchpath=BASE_DIR + "/templates")
env = Environment(loader=templateLoader)


class MainController(http.Controller):
    # 系统主界面
    @http.route('/ws_training/index', type='http', auth='public', csrf=False)
    def index(self, **kwargs):
        course_model = http.request.env['ws.training.course']
        course_list = course_model.sudo().search([])
        data_list = []
        for obj in course_list:
            data_list.append({'teacher': obj.teacher_id.name,
                              'course': obj.name})
            print data_list
        template = env.get_template("index.html")
        return template.render(data=data_list)

    @http.route('/ws_training/list', type='http', auth='public', csrf=False)
    def list(self, **post):
        template_list = env.get_template("attend_school_list.html")
        source = request.env['ws.training.course']
        training_attend_list = source.sudo().search_read([], ['name', 'time_start', 'teacher_id'])
        for attend_list in training_attend_list:
            attend_list['time_start'] = time.strftime("%Y-%m-%d",
                                                      time.strptime(attend_list['time_start'], "%Y-%m-%d %H:%M:%S"))
        data = {
            'training_attend_list': training_attend_list
        }
        html = template_list.render(data=data)
        return html

    @http.route('/ws_training/body', type='http', auth='public')
    def mobile_task_body(self, **post):
        template_list = env.get_template("course_detil.html")
        sup_task_list = [
            {'id': 'sup_name_course', 'sup_name': u'课程名称'},
            {'id': 'sup_teacher_course', 'sup_name': u'讲师'},
            {'id': 'sup_start_course', 'sup_name': u'开始时间'},
            {'id': 'sup_end_course', 'sup_name': u'结束时间'}
        ]
        post = post or {}
        task_id = post.get('task_id')
        user_id = request.session.uid
        source_1 = request.env['ws.training.course']
        course_detail_list = source_1.sudo().search_read([('id', '=', task_id)])
        this_description = course_detail_list[0]['description']
        for index in sup_task_list:
            if index['id'] == 'sup_name_course':
                index['name'] = course_detail_list[0]['name']
            elif index['id'] == 'sup_teacher_course':
                index['name'] = course_detail_list[0]['teacher_id'][1]
            elif index['id'] == 'sup_start_course':
                index['name'] = course_detail_list[0]['time_start']
            else:
                index['name'] = course_detail_list[0]['time_end']
        data = {
            'sup_task_list': sup_task_list,
            'this_description': this_description,
            'user_id': user_id,
            'course_id': task_id
        }
        html = template_list.render(data=data)
        return html

    # 签到
    @http.route('/w/a', type='http', auth='public', csrf=False)
    def index(self, **kwargs):
        course_model = http.request.env['ws.training.attend']
        # 先select判断是否存在，在的话不操作，不在的话插入数据
        user_id = kwargs.get('user_id')
        course_id = kwargs.get('course_id')
        try:
            record_count = course_model.sudo().search_count(
                [('user_id', '=', int(user_id)), ('course_id', '=', int(course_id))])
            if record_count < 1:
                vals = {
                    'user_id': user_id,
                    'course_id': course_id,
                    'attend_time': datetime.datetime.now(),
                    'description': ''
                }
                # 通过模型方法insert一条记录
                course_model.sudo().create(vals=vals)
                return http.Response('登记成功', 200)
        except:
            return http.Response('登记失败', 500)
        return http.Response('您已登记', 200)
