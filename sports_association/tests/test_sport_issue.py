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
        # cls.issue2 = cls.env['sport.issue'].create({
        #     'name': 'Issue 2',
        # })

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