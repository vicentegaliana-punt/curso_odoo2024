from odoo import models, fields

class SportClinic(models.Model):
    _name = 'sport.clinic'
    _description = 'Sport Clinic'
    
    name=fields.Char(string='Name',required=True)
    phone=fields.Char(string='Phone')
    email=fields.Char(string='Email')
    available=fields.Boolean(string='Available')

    #Ejemplo de campo reservado company_id
    # company_id=fields.Many2one('res.company',string='Company')
    
    #Ejemplo de One2many: cada clínica puede atender varias incidencias
    issues_ids=fields.One2many('sport.issue','clinic_id',string='Issues')
    #Campo calculado que nos devolverá el número de incidencias que tiene la clínica
    issues_count=fields.Integer(string='Issues count',compute='_compute_issues_count')

    def _compute_issues_count(self):
        for record in self:
            record.issues_count=len(record.issues_ids)

    def action_check_assistance(self):
        # import pdb; pdb.set_trace()
        self.issues_ids.write({'assistance':True})
        # self.issues_ids.write({'assistance':True}) es equivalente a:
        # for record in self.issues_ids:
            # record.assistance=True
        # También ésto nos funcionaría igual:
        # for record in self.issues_ids:
            # record.write({'assistance':True})
        

    def action_change_description(self):
        for record in self.issues_ids:
            record.description=_('Changed by the clinic')

    
    # Smart button for issues
    def action_open_issues_related(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Issues',
            'res_model': 'sport.issue',
            'view_mode': 'tree,form',
            'domain': [('clinic_id', '=', self.id)],
        }