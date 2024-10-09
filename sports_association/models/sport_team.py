from odoo import models, fields, api, Command
class SportTeam(models.Model):
    _name = 'sport.team'
    _description = 'Sport Team'
    
    name=fields.Char(string='Name',required=True)
    sport_id=fields.Many2one('sport',string='Sport')
    player_ids=fields.One2many('sport.player','team_id',string='Players')
    players_count=fields.Integer(string='Players Count',compute='_compute_players_count',store=True)
    league_id=fields.Many2one('sport.league',string='League')
    
    def action_populate_young_players(self):
        # Buscar jugadores menores de 30 años y que no tengan equipo, y los añade al equipo actual
        for record in self:
            players=self.env['sport.player'].search([('age','<',30),('team_id','=',False)])
            for player in players:
                record.player_ids=[Command.link(player.id)]

    @api.depends('player_ids')            
    def _compute_players_count(self):
        for record in self:
            record.players_count=len(record.player_ids)
        
        
    