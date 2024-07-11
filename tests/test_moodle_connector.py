from odoo.tests.common import TransactionCase

class TestMoodleConnector(TransactionCase):

    def test_sync_students(self):
        connector = self.env['moodle.connector'].create({
            'name': 'Test Connector',
            'moodle_url': 'http://moodle.test',
            'moodle_token': 'testtoken',
        })
        result = connector.sync_students()
        self.assertTrue(result, 'Students synced successfully')

    def test_sync_courses(self):
        connector = self.env['moodle.connector'].create({
            'name': 'Test Connector',
            'moodle_url': 'http://moodle.test',
            'moodle_token': 'testtoken',
        })
        result = connector.sync_courses()
        self.assertTrue(result, 'Courses synced successfully')
