from odoo import fields, models
class SportIssuesToDone(models.TransientModel):
    _name = 'sport.issues.to.done'
    _description = 'Set sport issues state to done'
    
    # def _default_issue(self):
    #     return self.env['sport.issue'].browse(self.env.context.get('active_ids'))

    # issue_ids = fields.Many2many('sport.issue', string="Issues", default=_default_issue)

    def issues_to_done(self):
        # Recuperamos las incidencias de origen
        active_ids=self.env.context.get('active_ids')

        # Recupero las incidencias a partir de sus ids. Y para optimizar el código
        # , voy a filtrar por las que aún no están en estado done. Esto se puede hacer de varias maneras:
        # 1. Con search
        # issues=self.env['sport.issue'].search([('id','in',active_ids),('state','!=','done')])
        # 2. Con browse y filtered
        issues=self.env['sport.issue'].browse(active_ids)
        issues=issues.filtered(lambda issue: issue.state!='done')

        # Aquí puedo iterar sobre las incidencias y cambiar su estado a done
        # for issue in issues:
            # issue.write({'state': 'done'})

        # ... pero también puedo aprovecharme de que ya tengo un método que hace eso en el modelo sport.issue 
        issues.action_done() 
