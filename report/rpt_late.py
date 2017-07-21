# -*- coding: utf-8 -*-
#@作者：cky

from odoo import api, fields, models, tools

class TrainingLateReport(models.Model):
    _name = "report.ws.traininglate"
    _description = u"培训出勤统计表"
    _auto = False
    _order = 'date desc'

    date = fields.Datetime(string= u'日期', readonly=True)
    user_id = fields.Many2one('res.users', string=u'学员', readonly=True)
    course_id = fields.Many2one('ws.training.course', string=u'课程', readonly=True)
    singe_state = fields.Selection([('belate', u'迟到'), ('absenteeism', u'缺勤'), (' normal', u'正常')], string=u'签到')
    qty = fields.Integer(u'数量')
    class_id = fields.Many2one('ws.training.class', u'班级')

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self._cr, 'report_ws_traininglate')
        self._cr.execute("""
                    CREATE OR REPLACE VIEW report_ws_traininglate AS (
                        SELECT attend_time as date,
                                        MIN(l.id) AS id,
                                        COUNT(*) AS qty,
                                        course_id,
                                        l.user_id user_id,
                                        ww.class_id class_id,
                                        singe_state
                                FROM ws_training_attend l
                                left join (
                                     select case when wl.user_id is not null then wl.user_id end user_id ,
                                     wl.class_id class_id
                                     from ws_training_class_users wl
                                     left join ws_training_class wt on wl.class_id = wt.id
                                ) ww on ww.user_id = l.user_id
                                GROUP BY attend_time,course_id,state,l.user_id,singe_state, ww.class_id)
        """)
