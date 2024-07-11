import requests
from odoo import models, fields, api

class MoodleConnector(models.Model):
    _name = 'moodle.connector'
    _description = 'Moodle Connector'

    name = fields.Char(string='Name', required=True)
    moodle_url = fields.Char(string='Moodle URL', required=True)
    moodle_token = fields.Char(string='Moodle Token', required=True)

    def call_moodle_api(self, function, params):
        url = f"{self.moodle_url}/webservice/rest/server.php"
        params.update({
            'wstoken': self.moodle_token,
            'moodlewsrestformat': 'json',
            'wsfunction': function,
        })
        response = requests.post(url, params=params)
        return response.json()

    def sync_students(self):
        students = self.env['op.student'].search([])
        for student in students:
            data = {
                'username': student.email,
                'firstname': student.name,
                'lastname': student.last_name,
                'email': student.email,
            }
            response = self.call_moodle_api('core_user_create_users', {'users': [data]})
            if 'exception' in response:
                self.env.cr.rollback()
                self.env['mail.message'].create({
                    'subject': 'Moodle Sync Error',
                    'body': response['message'],
                    'model': self._name,
                    'res_id': self.id,
                })
            else:
                self.env['mail.message'].create({
                    'subject': 'Moodle Sync Success',
                    'body': f"Student {student.name} synced successfully",
                    'model': self._name,
                    'res_id': self.id,
                })

    def sync_courses(self):
        courses = self.env['op.course'].search([])
        for course in courses:
            data = {
                'shortname': course.code,
                'fullname': course.name,
                'categoryid': 1,  # ID de categoría en Moodle
            }
            response = self.call_moodle_api('core_course_create_courses', {'courses': [data]})
            if 'exception' in response:
                self.env.cr.rollback()
                self.env['mail.message'].create({
                    'subject': 'Moodle Sync Error',
                    'body': response['message'],
                    'model': self._name,
                    'res_id': self.id,
                })
            else:
                self.env['mail.message'].create({
                    'subject': 'Moodle Sync Success',
                    'body': f"Course {course.name} synced successfully",
                    'model': self._name,
                    'res_id': self.id,
                })

    def sync_grades(self):
        grades = self.env['op.grade'].search([])
        for grade in grades:
            data = {
                'userid': grade.student_id.moodle_user_id,
                'courseid': grade.course_id.moodle_course_id,
                'grade': grade.value,
            }
            response = self.call_moodle_api('gradereport_user_get_grades_table', {'userid': data['userid']})
            if 'exception' in response:
                self.env.cr.rollback()
                self.env['mail.message'].create({
                    'subject': 'Moodle Sync Error',
                    'body': response['message'],
                    'model': self._name,
                    'res_id': self.id,
                })
            else:
                self.env['mail.message'].create({
                    'subject': 'Moodle Sync Success',
                    'body': f"Grade synced for student: {grade.student_id.name}",
                    'model': self._name,
                    'res_id': self.id,
                })
