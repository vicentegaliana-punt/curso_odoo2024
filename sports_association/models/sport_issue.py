from odoo import models, fields, Command
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
    color=fields.Integer(string='Color',default=0)
    user_id=fields.Many2one('res.users',string='User')
    secuence = fields.Integer(string='Secuence', default=10)
    solution = fields.Html(string='Solution')

    #Ejemplo de campo calculado no almacenado
    assigned=fields.Boolean(string='Assigned',compute='_compute_assigned',inverse='_inverse_assigned',search='_search_assigned')
    
    #Ejemplo de Many2one: cada incidencia pertenece a una clínica (una sola)
    clinic_id=fields.Many2one('sport.clinic',string='Clinic')
    #Ejemplo de Many2many: cada incidencia puede tener varios tags
    tag_ids=fields.Many2many('sport.issue.tag',string='Tags')

    #Ejemplo de campo float, nos vendrá bien para poder medir en la vista pivot
    cost = fields.Float('cost')

    #Ejemplo de campo relacional, vamos a almacenar en el campo user_phone el teléfono del usuario
    user_phone=fields.Char(string='User Phone',related='user_id.phone',store=True, readonly=False)

    #Ejemplo de campo one2many, cada incidencia puede tener varias acciones
    action_ids=fields.One2many('sport.issue.action','issue_id',string='Actions to do')

    def _compute_assigned(self):
        for record in self:
            record.assigned=bool(record.user_id)

    def _inverse_assigned(self):
        for record in self:
            if not record.assigned:
                record.user_id=False
            else:
                record.user_id=self.env.user.id

    def _search_assigned(self,operator,value):
        if operator=='=':
            if(value):
                return [('user_id','!=',False)]
            else:
                return [('user_id','=',False)]
        else:
            return []

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

    def action_create_tag_test(self):
        tag = self.env['sport.issue.tag'].create({'name':'Test Tag'})

    def action_copy_issue(self):
        for record in self:
            copy_issue=record.copy({'name':'Copia de '+record.name,'state':'draft'})
            
    def action_add_tags(self):
        #Crea y añade dos nuevas etiquetas a la incidencia
        for record in self:
            record.write({'tag_ids':[(0, 0, {'name':'New Tag 1'}),(0, 0, {'name':'New Tag 2'})]})
            

    def action_add_grave_urgente_tags(self):
        #Añade las etiquetas Grave y Urgente a la incidencia
        for record in self:
            # import pdb;pdb.set_trace()
            grave_tag=self.env['sport.issue.tag'].search([('name','=','Grave')],limit=1)
            urgente_tag=self.env['sport.issue.tag'].search([('name','=','Urgente')],limit=1)
            record.write({'tag_ids':[(4, grave_tag.id),(4, urgente_tag.id)]})

    def action_add_extrema_tag(self):
        #Crea y añade la etiqueta Extrema a la incidencia
        for record in self:
            record.tag_ids=[Command.create({'name':'Extrema'})]
            
    def action_add_all_tags(self):
        #Añade todas las etiquetas a la incidencia
        for record in self:
            tags=self.env['sport.issue.tag'].search([])
            #Cualquiera de las dos formas es válida:
            # record.write({'tag_ids':[(6, 0, tags.ids)]})
            record.tag_ids=[Command.set(tags.ids)]

    def action_remove_all_tags(self):
        #Quita sin borrar todas las etiquetas de la incidencia
        for record in self:
            record.tag_ids=[Command.clear()]