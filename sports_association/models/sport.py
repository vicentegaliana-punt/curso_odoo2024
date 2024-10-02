from odoo import models, fields
class Sport(models.Model):
    _name = 'sport'
    _description = 'Sport'
    
    name=fields.Char(string='Name',required=True)
    description=fields.Text(string='Description')
    team_ids=fields.One2many('sport.team','sport_id',string='Teams')