from odoo import models, fields

class SportMatch(models.Model):
    _name = 'sport.match'
    _description = 'Sport Match'

    name = fields.Char(string='Name', required=True)
    date = fields.Date(string='Date', required=True)
    sport_id = fields.Many2one('sport', string='Sport')
    team_ids = fields.Many2many('sport.team', string='Teams')
    result = fields.Char(string='Result')
    winner_id = fields.Many2one('sport.team', string='Winner')