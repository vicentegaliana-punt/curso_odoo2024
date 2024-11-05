from odoo.tests import common
from odoo import fields, models

class TestSportIssue(common.TransactionCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Recupero un usuario (admin), ya que seguramente necesitaré usarlo en algún test
        # cls.user = cls.env.ref('base.user_admin')
        # Este sería el usuario actual
        cls.user= cls.env.user

        # Creo una incidencia
        cls.issue = cls.env['sport.issue'].create({
            'name': 'Issue 1',
        })
        cls.issue2 = cls.env['sport.issue'].create({
            'name': 'Issue 2',
        })

    # El método que comprueba los dos casos, solo me funciona bien si uso una incedencia diferente para cada caso
    # def test_compute_assigned(self):
    #     # Compruebo que el campo assigned se calcula correctamente en caso de que no exista un usuario asignado
    #     self.issue.user_id=False
    #     self.assertFalse(self.issue.assigned)
    #     # Compruebo que el campo assigned se calcula correctamente en caso de que exista un usuario asignado
    #     self.issue2.user_id=self.user_admin
    #     self.assertTrue(self.issue2.assigned)

    def test_compute_assigned(self):
        # Compruebo que el campo assigned se calcula correctamente en caso de que exista un usuario asignado
        self.issue.user_id=self.user
        self.assertTrue(self.issue.assigned)

    def test_compute_not_assigned(self):
        # Compruebo que el campo assigned se calcula correctamente en caso de que no exista un usuario asignado
        self.issue.user_id=False
        self.assertFalse(self.issue.assigned)

    def test_inverse_assigned(self):
        # Compruebo que el campo user_id se asigna correctamente en caso de que no exista un usuario asignado
        self.issue.assigned=False
        self.assertFalse(self.issue.user_id)
        # Compruebo que el campo user_id se asigna correctamente en caso de que exista un usuario asignado
        self.issue.assigned=True
        self.assertEqual(self.issue.user_id, self.user)

    def test_workflow(self):
        # Compruebo que el estado de la incidencia es 'draft' al crearla
        self.assertEqual(self.issue.state, 'draft')
        # Compruebo que el estado de la incidencia es 'open' al ejecutar el método action_open
        self.issue.action_open()
        self.assertEqual(self.issue.state, 'open')
        # Compruebo que el estado de la incidencia es 'done' al ejecutar el método action_done
        self.issue.action_done()
        self.assertEqual(self.issue.state, 'done')
        # Compruebo que el estado de la incidencia es 'draft' al ejecutar el método action_draft
        self.issue.action_draft()
        self.assertEqual(self.issue.state, 'draft')
        # Compruebo que se lanza una excepción al intentar cambiar el estado de la incidencia a 'done' sin fecha
        self.issue.date=False
        # se puede hacer de dos formas:
        # self.assertRaises(models.ValidationError, self.issue.action_done)
        # o bien:
        with self.assertRaises(models.ValidationError):
            self.issue.action_done()

    def test_action_open_all_issues(self):
        self.issue.state='draft'
        self.issue2.state='draft'
        # Compruebo que el estado de todas las incidencias es 'open' al ejecutar el método action_open_all_issues sobre cualquiera de ellas
        self.issue.action_open_all_issues()
        self.assertEqual(self.issue.state, 'open')
        self.assertEqual(self.issue2.state, 'open')

    def test_action_create_tag_test(self):
        # Compruebo que se crea una etiqueta al ejecutar el método action_create_tag_test
        self.issue.action_create_tag_test()
        self.assertTrue(self.env['sport.issue.tag'].search([('name', '=', 'Test Tag')]))


    def test_action_copy_issue(self):
        # Compruebo que se crea una copia de la incidencia al ejecutar el método action_copy_issue
        self.issue.action_copy_issue()
        self.assertTrue(self.env['sport.issue'].search([('name', '=', 'Copia de Issue 1'), ('state', '=', 'draft')]))

    def test_action_add_tags(self):
        # Compruebo que se añaden dos etiquetas a la incidencia al ejecutar el método action_add_tags
        self.issue.action_add_tags()
        self.assertTrue(self.issue.tag_ids.filtered(lambda r: r.name == 'New Tag 1'))
        self.assertTrue(self.issue.tag_ids.filtered(lambda r: r.name == 'New Tag 2'))
    
    def test_action_add_grave_urgente_tags(self):
        # Compruebo que se añaden las etiquetas Grave y Urgente a la incidencia al ejecutar el método action_add_grave_urgente_tags
        self.issue.action_add_grave_urgente_tags()
        self.assertTrue(self.issue.tag_ids.filtered(lambda r: r.name == 'Grave'))
        self.assertTrue(self.issue.tag_ids.filtered(lambda r: r.name == 'Urgente'))

    def test_action_add_extrema_tag(self):
        # Compruebo que se añade la etiqueta Extrema a la incidencia al ejecutar el método action_add_extrema_tag
        self.issue.action_add_extrema_tag()
        self.assertTrue(self.issue.tag_ids.filtered(lambda r: r.name == 'Extrema'))

    def test_action_add_all_tags(self):
        # Compruebo que se añaden todas las etiquetas a la incidencia al ejecutar el método action_add_all_tags
        self.issue.action_add_all_tags()
        self.assertEqual(len(self.issue.tag_ids), len(self.env['sport.issue.tag'].search([])))
    
    def test_action_remove_all_tags(self):
        # Compruebo que se eliminan todas las etiquetas de la incidencia al ejecutar el método action_remove_all_tags
        self.issue.action_remove_all_tags()
        self.assertFalse(self.issue.tag_ids)

    def test_check_cost(self):
        # Compruebo que se lanza una excepción al intentar asignar un coste negativo
        with self.assertRaises(models.ValidationError):
            self.issue.cost=-1
    
    #Este test no funciona porque @api.onchange solo funciona para cambios realizados en la interfaz, no para cambios realizados en el código
    # def test_onchange_clinic_id(self):
    #     # Compruebo que si se asigna a la incidencia la clínica 'Hospital Virgen de la Arrixaca', el campo assistance se pone a True
    #     clinicArrixaca=self.env['sport.clinic'].search([('name', '=', 'Hospital Virgen de la Arrixaca')])
    #     self.issue.clinic_id=clinicArrixaca
    #     self.assertTrue(self.issue.assistance)
