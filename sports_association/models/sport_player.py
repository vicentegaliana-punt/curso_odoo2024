from odoo import models, fields, api
from datetime import date
class SportPlayer(models.Model):
    _name = 'sport.player'
    _description = 'Sport Player'
    _inherits = {'res.partner':'partner_id'}
    
    # partner_id = fields.Many2one('res.partner', string='Partner', required=True, ondelete='cascade')
    partner_id = fields.Many2one('res.partner', string='Partner', required=True, ondelete='restrict')
    # name=fields.Char(string='Name',copy=False)
    name=fields.Char(related='partner_id.name',inherited=True,readonly=False)

    # Añado el campo active. Por el hecho de tener este campo, automáticamente 
    # Odoo aportará funcionalidad para poder archivar / desarchivar jugadores
    active=fields.Boolean(string='Active',default=True,help='If unchecked, allow you to hide the player without removing it')

    birth_date=fields.Date(string='Birth Date',copy=False)
    age=fields.Integer(string='Age',compute='_compute_age',store=True,copy=False)
    starter=fields.Boolean(string='Starter', default=True)
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
