from odoo import models, fields

class SportLeague(models.Model):
    _name = 'sport.league'
    _description = 'Sport League'
    
    name=fields.Char(string='Name',required=True)
    start_date=fields.Datetime(string='Start Date')
    end_date=fields.Datetime(string='End Date')
    sport_id=fields.Many2one('sport',string='Sport')
    sport_league_team_ids=fields.One2many('sport.league.team','league_id',string='League Teams')


    #Ejemplo de One2many: cada liga puede tener varios equipos
    team_ids=fields.One2many('sport.team','league_id',string='Teams')

    #Asigna un punto a cada equipo de la liga por cada partido ganado
    def action_set_score(self):
        for record in self.sport_league_team_ids:
            record.points=self.env['sport.match'].search_count([('sport_id','=',self.sport_id.id),('winner_id','=',record.team_id.id)])
            
    
class SportLeagueTeam(models.Model):
    _name = 'sport.league.team'
    _description = 'Sport League Team'
    _order='points desc'
    
    league_id=fields.Many2one('sport.league',string='League')
    team_id=fields.Many2one('sport.team',string='Team')
    #puntos que lleva el equipo en la liga (solo pertece a una liga a la vez)
    points=fields.Integer(string='Points')
    
