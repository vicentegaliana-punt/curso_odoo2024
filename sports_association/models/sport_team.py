from odoo import models, fields, Command
class SportTeam(models.Model):
    _name = 'sport.team'
    _description = 'Sport Team'
    
    name=fields.Char(string='Name',required=True)
    sport_id=fields.Many2one('sport',string='Sport')
    player_ids=fields.One2many('sport.player','team_id',string='Players')
    
    def action_populate_young_players(self):
        for record in self:
            players=self.env['sport.player'].search([('age','<',30)])
            record.player_ids=[Command.set(players.ids)]
        
        
        
    