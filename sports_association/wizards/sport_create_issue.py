from odoo import fields, models, api
class SportCreateIssue(models.TransientModel):
    _name = 'sport.create.issue'
    _description = 'Create Issue'
    
    name=fields.Text(string='Name')
    clinic_id=fields.Many2one('sport.clinic',string='Clinic')
    def action_create_issue(self):
        issue=self.env['sport.issue'].create({
            'description':self.description,
            'clinic_id':self.clinic_id.id
        })
        return issue.action_open_issue_form()