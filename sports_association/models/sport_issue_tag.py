from odoo import models, fields

class SportIssueTag(models.Model):
    _name = 'sport.issue.tag'
    _description = 'Sport Issue Tag'

    name = fields.Char(string='name', required=True)
    #Ejemplo de Many2many: cada tag puede estar en varias incidencias
    issues_ids = fields.Many2many('sport.issue', string='Issues')
    color=fields.Integer(string='color',default=0)