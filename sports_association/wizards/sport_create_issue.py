from odoo import fields, models, api
class SportCreateIssue(models.TransientModel):
    _name = 'sport.create.issue'
    _description = 'Create Issue'
    
    name=fields.Text(string='Name')
    #Añado como valor por defecto el active_id de la clínica de origen. 
    # Si partimos de una selección de varias clínicas, tendrá el valor de la primera seleccionada
    clinic_id=fields.Many2one('sport.clinic',string='Clinic', default=lambda self: self.env.context.get('active_id'))
    
    def action_create_issue(self):
        # Recuperamos las clínicas de origen
        active_ids=self.env.context.get('active_ids')
        clinics=self.env['sport.clinic'].browse(active_ids)
        for clinic in clinics:
            issue=self.env['sport.issue'].create({
                # Como el nombre debe ser único, le añado el nombre de la clínica para el caso de selección múltiple
                'name':self.name+' - '+clinic.name,
                'clinic_id':clinic.id,
            })

        return {
            'name': 'Issue',
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
            'res_model': 'sport.issue',
            'res_id': issue.id,
            'target': 'current',
        }

