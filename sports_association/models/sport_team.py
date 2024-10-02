from odoo import models, fields
class SportTeam(models.Model):
    _name = 'sport.team'
    _description = 'Sport Team'
    
    name=fields.Char(string='Name',required=True)
    sport_id=fields.Many2one('sport',string='Sport')
    player_ids=fields.One2many('sport.player','team_id',string='Players')
    

        
    