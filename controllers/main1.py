# -*- coding: utf-8 -*-

import logging
import cStringIO
import qrcode
import os
import sys
import time
import json
from jinja2 import Environment, FileSystemLoader
from odoo import http
from odoo.http import request, Response
import datetime

reload(sys)
sys.setdefaultencoding('utf8')

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
templateLoader = FileSystemLoader(searchpath=BASE_DIR + "/templates")
env = Environment(loader=templateLoader)


class MainController(http.Controller):
    # # 系统主界面
    # @http.route('/ws_training/index', type='http', auth='public', csrf=False)
    # def index(self, **kwargs):
    #     course_model = http.request.env['ws.training.course']
    #     course_list = course_model.sudo().search([])
    #     data_list = []
    #     for obj in course_list:
    #         data_list.append({'teacher': obj.teacher_id.name,
    #                           'course': obj.name})
    #         print data_list
    #     template = env.get_template("index.html")
    #     return template.render(data=data_list)

    # 展示二维码的页面
    @http.route('/w/qrcode_html', type='http', auth='public', csrf=False)
    def qrcode_html(self, **kwargs):
        qrcode_page = env.get_template("qrcode.html")
        return qrcode_page.render()

    @http.route('/ws_training/guide', type='http', auth='public', csrf=False)
    def guide_list(self, **post):
        template_list = env.get_template("guide.html")
        data = {
        }
        html = template_list.render(data=data)
        return html

    # 登录页面
    @http.route('/ws_training/log', type='http', auth='public', csrf=False)
    def sign_in(self, **post):
        template_list = env.get_template("attend_sign_in.html")
        html = template_list.render()
        return html

    # 课程列表页面
    @http.route('/ws_training/list', type='http', auth='public', csrf=False)
    def list(self, **post):
        template_list = env.get_template("attend_school_list.html")
        source = request.env['ws.training.course']
        training_attend_list = source.sudo().search_read([], ['name', 'time_start', 'teacher_id', 'id'])
        # 每个course增加一个当前签到人数的字段
        for course_item in training_attend_list:
            course_item['time_start'] = time.strftime("%Y-%m-%d",
                                                      time.strptime(course_item['time_start'], "%Y-%m-%d %H:%M:%S"))
            course_item['attend_count'] = str(request.env['ws.training.attend'].sudo().search_count(
                [('course_id', '=', course_item['id'])]))
        data = {
            'training_attend_list': training_attend_list
        }
        print data
        html = template_list.render(data=data)
        return html

    # 课程详情页面
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

    # 签到接口
    @http.route('/w/a', type='http', auth='public', csrf=False)
    def index(self, **kwargs):
        if (time.time() - float(kwargs.get('timestamp'))) > 20:
            return http.Response('已过期', 200)
        course_model = http.request.env['ws.training.attend']
        # 先select判断是否存在，在的话不操作，不在的话插入数据
        user_id = kwargs.get('user_id')
        course_id = kwargs.get('course_id')
        try:
            record_count = course_model.sudo().search_count(
                [('user_id', '=', user_id), ('course_id', '=', course_id)])
            if record_count < 1:
                vals = {
                    'user_id': user_id,
                    'course_id': course_id,
                    'attend_time': datetime.datetime.now(),
                }
                # 通过模型方法insert一条记录
                course_model.sudo().create(vals=vals)
                return http.Response('登记成功', 200)
        except:
            return http.Response('登记失败', 500)
        return http.Response('您已登记', 200)

    # 生成二维码，每个二维码都有个有效期
    @http.route('/w/q', type='http', auth='public', csrf=False)
    def get_qrcode(self, **kwargs):
        qrcode_page = env.get_template("qrcode.html")
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data('http://10.20.113.107:8069/ws_training/log?timestamp=' + str(time.time()))
        qr.make(fit=True)
        img = qr.make_image()
        headers = [('Content-Type', 'image/png')]
        buffer = cStringIO.StringIO()
        img.save(buffer)
        img_buffer = buffer.getvalue()
        headers.append(('Content-Length', str(len(img_buffer))))
        response = request.make_response(img_buffer, headers)
        return response

    # 登录接口
    @http.route('/w/login', type='http', auth='public', csrf=False)
    def login(self, **kwargs):
        username = kwargs.get('username', '')
        password = kwargs.get('password', '')
        user_model = request.env['res.users'].sudo()
        response = {
            'msg': u'未知异常',
            'login_success': False
        }
        if user_model.search_count([('login', '=', username)]) < 1:
            response['msg'] = '用户不存在'
        elif user_model.search_count([('login', '=', username), ('password', '=', password)]) == 0:
            response['msg'] = '密码不正确'
        elif user_model.search_count([('login', '=', username), ('password', '=', password)]) > 0:
            response['msg'] = '登录成功'
            response['user_id'] = user_model.search([('login', '=', username), ('password', '=', password)])[0].id
            response['login_success'] = True
        return Response(json.dumps(response), status=200)

    # 我的课程页面：已开课，未开课
    @http.route('/ws_training/person', type='http', auth='public', csrf=False)
    def list(self, **kwargs):
        template_list = env.get_template("personal_course.html")
        user_id = kwargs.get('user_id')
        course_model = request.env['ws.training.course'].sudo()
        course_list = request.env['ws.training.class.users'].sudo().search_read([('user_id', '=', user_id)],
                                                                                ['course_id'])
        detail_course_list = []
        # 从课程表获得详细的课程信息
        for course in course_list:
            detail_course_list.append(course_model.search('id', '=', course[0]))
        had_started_course = []
        not_started_course = []
        # 获得未开课以及已开课的list
        for detail_course_item in detail_course_list:
            course_start_time = datetime.datetime.strptime(detail_course_item['time_start'], '%Y-%m-%d %H:%M:%S')
            if course_start_time > datetime.datetime.now():
                not_started_course.append(detail_course_item)
            else:
                had_started_course.append(detail_course_item)
        data = {'had_started_course': had_started_course,
                'not_started_course': not_started_course}
        html = template_list.render(data=data)
        return html

    # 课程基本信息，签到情况，评论
    @http.route('/ws_training/person', type='http', auth='public', csrf=False)
    def list(self, **kwargs):
        course_id = kwargs.get('course_id', 1)
        user_id = kwargs.get('user_id', 1)
        comment_model = request.env['ws.training.course.comment'].sudo()
        course_detail = request.env['ws.training.attend'].sudo().search_read([('id', '=', course_id)],
                                                                             ['name', 'time_start', 'teacher_id',
                                                                              'id'])[0]
        attend_detail = request.env['ws.training.course'].sudo().search_read([('user_id', '=', user_id),
                                                                              ('course_id', '=', course_id)],
                                                                             ['singe_state'])[0]
        # 从课程表获得详细的课程信息
        #html = template_list.render(data=data)
        return ''

    # 修改评论
    @http.route('/ws_training/person', type='http', auth='public', csrf=False)
    def list(self, **kwargs):
        course_id = kwargs.get('course_id', 1)
        user_id = kwargs.get('user_id', 1)
        comment = kwargs.get('comment', '默认好评')
        vals = {
            'name': user_id,
            'course_id': course_id,
            'student_comment': comment
        }
        comment_model = request.env['ws.training.course.comment'].sudo()
        comment_count = comment_model.search_count([('user_id', '=', user_id), ('course_id', '=', course_id)])
        if comment_count > 0:
            comment_model.write(vals=vals)
            return Response('新增评论成功', 200)
        elif comment_count == 0:
            comment_model.create(vals=vals)
            return Response('更新评论成功', 200)
        return Response('更新评论异常', 200)
