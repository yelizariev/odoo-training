# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools


class TrainingReport(models.Model):
    _name = "report.ws.training"
    _description = u"培训签到统计表"
    _auto = False
    _order = 'date desc'

    date = fields.Datetime(string='日期', readonly=True)
    attend_id = fields.Many2one('ws.training.attend', string='签到', readonly=True)
    user_id = fields.Many2one('res.users', string='学员', readonly=True)
    course_id = fields.Many2one('ws.training.course', string='课程', readonly=True)

    # average_price = fields.Float(string='Average Price', readonly=True, group_operator="avg")
    nbr_lines = fields.Integer(string='行数', readonly=True, oldname='nbr')

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self._cr, 'report_ws_training')
        self._cr.execute("""
            CREATE OR REPLACE VIEW report_ws_training AS (
                SELECT attend_time as date,
                        MIN(l.id) AS id,
                        COUNT(*) AS nbr_lines,
                        user_id,
                        course_id
                FROM ws_training_attend l
                GROUP BY attend_time,user_id,course_id
            )
        """)
