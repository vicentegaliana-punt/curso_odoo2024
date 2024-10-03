from odoo import models, fields, api
from datetime import date
class SportPlayer(models.Model):
    _name = 'sport.player'
    _description = 'Sport Player'
    
    name=fields.Char(string='Name',required=True)
    birth_date=fields.Date(string='Birth Date')
    age=fields.Integer(string='Age',compute='_compute_age',store=True)
    starter=fields.Boolean(string='Starter')
    team_id=fields.Many2one('sport.team',string='Team')
    sport_id=fields.Char(string='Sport',related='team_id.sport_id.name')

    #Obtiene la edad de un jugador a partir de su fecha de nacimiento y la fecha actual
    @api.depends('birth_date')
    def _compute_age(self):
        for record in self:
            today=date.today()
            if isinstance(record.birth_date,date):
                if today.year-record.birth_date.year>0:
                    age=today.year-record.birth_date.year-((today.month,today.day)<(record.birth_date.month,record.birth_date.day))
                else:
                    age=0
            else:
                age=0
            record.age=age

    def action_make_starter(self):
        self.starter=True

    def action_make_substitute(self):
        self.starter=False
