from odoo import models, fields
class SportIssue(models.Model):
    _name = 'sport.issue'
    _description = 'Sport Issue'
    
    name=fields.Char(string='Name',required=True)
    description=fields.Text(string='Description')
    date=fields.Datetime(string='Date')
    assistance=fields.Boolean(string='Assistance',help='Show if the issue is related to assistance')
    state=fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('done', 'Done'),
    ], string='State', default='draft')
    user_id=fields.Many2one('res.users',string='User')
    secuence = fields.Integer(string='Secuence', default=10)
    solution = fields.Html(string='Solution')
    #Ejemplo de Many2one: cada incidencia pertenece a una clínica (una sola)
    clinic_id=fields.Many2one('sport.clinic',string='Clinic')
    #Ejemplo de Many2many: cada incidencia puede tener varios tags
    tag_ids=fields.Many2many('sport.issue.tag',string='Tags')


    def action_open(self):
        #Para procesar un solo registro ésto estaría bien
        # self.ensure_one()
        # self.state='open'

        # Pero, ¿porque limitarnos? Es posible que queramos llamar 
        # este método desde otros métodos que sí estén procesando varios registros	
        # Así que es mejor dejarlo preparado
        # para que acepte y procese un recordset de uno o de varios registros
        # for record in self:
            # record.state='open'
            
        # Pero ésto tampoco sería lo ideal, es incluso mejor hacer uso de la función write
        # que es más eficiente y rápida
        self.write({'state':'open'})

    def action_done(self):
        self.write({'state':'done'})

    def action_draft(self):
        self.write({'state':'draft'})

    def action_open_all_issues(self):
        issues=self.env['sport.issue'].search([])
        issues.action_open()

    
