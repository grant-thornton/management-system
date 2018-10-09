# -*- coding: utf-8 -*-
# Copyright 2012 Savoir-faire Linux <http://www.savoirfairelinux.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, fields, _


def own_company(self):
    return self.env.user.company_id.id


class MgmtSystemSystem(models.Model):

    _name = 'mgmtsystem.system'
    _description = _('System')
    _order = 'name, code, notes'
    _inherit = ['mail.thread']

    name = fields.Char('System', required=True, track_visibility='onchange')
    company_id = fields.Many2one(
        'res.company', 'Company', default=own_company,
        track_visibility='onchange')
    code = fields.Char(string='Code', track_visibility='onchange')
    notes = fields.Char(string='Notes', track_visibility='onchange')
    active = fields.Boolean(default=True)

    @api.multi
    @api.depends('name', 'code')
    def name_get(self):
        result = []
        for vector in self:
            if vector.code:
                name = u"{}".format(vector.code)
            else:
                name = u"{}".format(vector.name)
            result.append((vector.id, name))
        return result

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        domain = []
        if name:
            domain = [
                '|', ('name', operator, name),
                ('code', operator, name)
            ]
        pos = self.search(domain + args, limit=limit)
        return pos.name_get()
