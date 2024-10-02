from odoo import models, fields
from datetime import date
class SportPlayer(models.Model):
    _name = 'sport.player'
    _description = 'Sport Player'
    
    name=fields.Char(string='Name',required=True)
    birth_date=fields.Date(string='Birth Date')
    age=fields.Integer(string='Age',compute='_compute_age')
    team_id=fields.Many2one('sport.team',string='Team')

    #Obtiene la edad de un jugador a partir de su fecha de nacimiento y la fecha actual
    def _compute_age(self):
        for record in self:
            today=date.today()
            age=today.year-record.birth_date.year-((today.month,today.day)<(record.birth_date.month,record.birth_date.day))
            record.age=age