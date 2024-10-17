from odoo import fields, models, api
class SportPlayerCreateIssue(models.TransientModel):
    _name = 'sport.player.create.issue'
    _description = 'Create Issue'
    
    name=fields.Text(string='Name')
    #Añado como valor por defecto el active_id del jugador de origen. 
    # Si partimos de una selección de varios jugadores, tendrá el valor del primero seleccionado
    player_id=fields.Many2one('sport.player',string='Player', default=lambda self: self.env.context.get('active_id'))
    
    def action_player_create_issue(self):
        # Recuperamos los jugadores de origen
        active_ids=self.env.context.get('active_ids')
        players=self.env['sport.player'].browse(active_ids)
        for player in players:
            issue=self.env['sport.issue'].create({
                # Como el nombre debe ser único, le añado el nombre del jugador para el caso de selección múltiple
                'name':self.name+' - '+player.name,
                'player_id':player.id,
            })

        return {
            'name': 'Issue',
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
            'res_model': 'sport.issue',
            'res_id': issue.id,
            'target': 'current',
        }