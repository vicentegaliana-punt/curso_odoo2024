from odoo import models, fields, api,_
from odoo.exceptions import ValidationError

class SportLeague(models.Model):
    _name = 'sport.league'
    _description = 'Sport League'
    
    name=fields.Char(string='Name',required=True)
    start_date=fields.Datetime(string='Start Date')
    end_date=fields.Datetime(string='End Date')
    sport_id=fields.Many2one('sport',string='Sport')
    sport_league_team_ids=fields.One2many('sport.league.team','league_id',string='League Teams')
    match_ids=fields.One2many('sport.match','league_id',string='Matches')
    matches_count=fields.Integer(compute='_compute_match_count',string='Match Count')

    # Función para calcular el número de partidos de la liga
    def _compute_match_count(self):
        for record in self:
            record.matches_count=len(record.match_ids)
            

    # Función para asegurar que la fecha de incio sea anterior a la fecha de fin
    @api.constrains('start_date','end_date')
    def _check_dates(self):
        for record in self:
            if record.start_date and record.end_date:
                if record.start_date > record.end_date:
                    raise ValidationError(_('End date must be greater than start date'))
        

    # Función que devuelve la parte de fecha de start_date en formato español
    def get_start_date(self):
        return self.start_date.strftime('%d/%m/%Y')


    #Ejemplo de One2many: cada liga puede tener varios equipos
    team_ids=fields.One2many('sport.team','league_id',string='Teams')

    #Asigna un punto a cada equipo de la liga por cada partido ganado
    def action_set_score(self):
        for record in self.sport_league_team_ids:
            record.points=self.env['sport.match'].search_count([('sport_id','=',self.sport_id.id),('winner_id','=',record.team_id.id)])
            
    #Creo el método cron para calcular los puntos de los equipos de la liga
    def _cron_set_score(self):
        leagues=self.search([])
        # Como estamos en la misma clase, no hemos necesitado hacer referencia a self.env, pero lo de abajo funcionaría igual
        # leagues=self.env['sport.league'].search([])
        for league in leagues:
            league.action_set_score()

    #Smart button for matches
    def action_view_matches(self):
        return {
            'name': _('Matches'),
            'type': 'ir.actions.act_window',
            'res_model': 'sport.match',
            'view_mode': 'tree,form',
            'domain': [('league_id','=',self.id)],
        }
    
class SportLeagueTeam(models.Model):
    _name = 'sport.league.team'
    _description = 'Sport League Team'
    _order='points desc'
    
    league_id=fields.Many2one('sport.league',string='League')
    team_id=fields.Many2one('sport.team',string='Team')
    #puntos que lleva el equipo en la liga (solo pertece a una liga a la vez)
    points=fields.Integer(string='Points')
    
