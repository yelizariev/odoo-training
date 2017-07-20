# -*- coding: utf-8 -*-
{
    'name': 'WENS Training',
    'version': '1.0',
    'author': 'Yu Xia & Xianhuo Wong',
    'summary': u'温氏培训',
    'sequence': 30,
    'description': u"""
        签到与课程管理
    """,
    'category': 'WENS',
    'website': 'http://wmp.wens.com.cn',
    'images': [],
    'depends': ['base'],
    'data': [
        'views/view_training_attend.xml',
        'views/view_training_course.xml',
        'views/rpt_view_ws_training.xml',
        'views/menus.xml',

    ],
    'demo': [

    ],
    'qweb': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}