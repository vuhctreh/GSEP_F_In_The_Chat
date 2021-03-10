""" Incorporates all functions that are used to test the functionality of the
    web application (UNIT TESTING)
"""

from django.test import SimpleTestCase, TestCase, Client
from django.template.loader import render_to_string
from app.models import CafeTable, CoffeeUser, Message, Task

client = Client()


class HealthEndpointTests(SimpleTestCase):
    """ Unit tests regarding the status of the web application """

    def test_health_status_is_up(self):
        """ Testing whether the status of the web application is 200 """
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '{"status": "UP"}')


class LogInTests(TestCase):
    """ Unit tests for the login page """

    def test_login_view_status_code(self):
        """ Testing the status of the login page (if it's 200) """
        response = self.client.get('')  # login page
        self.assertEqual(response.status_code, 200)

    def test_csrf(self):
        """ Testing whether a csrf token exists """
        response = self.client.get('')
        self.assertContains(response, 'csrfmiddlewaretoken')


class SignUpTests(TestCase):
    """ Unit tests for the sign up page """

    def test_signup_view_status_code(self):
        """ Testing the status of the signup page (if it's 200) """
        response = self.client.get('/signup')
        self.assertEqual(response.status_code, 200)

    def test_csrf(self):
        """ Testing whether a csrf token exists """
        response = self.client.get('/signup')
        self.assertContains(response, 'csrfmiddlewaretoken')


class PrivacyPolicyTests(TestCase):
    """ Unit tests for the privacy policy page """

    def test_privacy_policy_view_status_code(self):
        """ Testing the status of the privacy policy page (if it's 200) """
        response = self.client.get('/privacy')
        self.assertEqual(response.status_code, 200)


class TermsTests(TestCase):
    """ Unit tests for the terms and conditions page """

    def test_tandc_view_status_code(self):
        """ Testing the status of the terms and conditions page
        (if it's 200) """
        response = self.client.get('/terms')
        self.assertEqual(response.status_code, 200)


class TablesViewTests(TestCase):
    """ Unit tests for the tables view page """

    def setUp(self):
        """ Setting up 2 tables with users for testing purposes """
        table = CafeTable.objects.create(table_id='Test',
                                         university='Test uni')
        table2 = CafeTable.objects.create(table_id='Test 2',
                                          university='Test uni')
        user = CoffeeUser.objects.create_user(
            email='test@test.com', first_name='testf', last_name='testl',
            university='Test uni', is_staff=False, password='123'
        )
        user.cafe_table_ids.add(table)
        self.client.login(email='test@test.com', password='123')

    def test_tables_view_status_code(self):
        """ Testing the status of the created tables (if it's 200) """
        response = self.client.get('/table_view')
        self.assertEqual(response.status_code, 200)

    def test_tables_view_content(self):
        """ Testing whether the status of the table content page is OK
            and whether the content is the expected values
        """
        response = self.client.get('/table_view')
        response_html = response.content.decode()
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Test' in response_html)
        self.assertFalse('Test 2' in response_html)


class InTableTests(TestCase):
    """ Unit tests for the table chat page """

    def setUp(self):
        """ Setting up the content of the tables for testing purposes """
        table = CafeTable.objects.create(table_id='Test',
                                         university='Test uni')
        table2 = CafeTable.objects.create(table_id='Test 2',
                                          university='Test uni')
        user = CoffeeUser.objects.create_user(
            email='test@test.com', first_name='testf', last_name='testl',
            university='Test uni', is_staff=False, password='123'
        )
        user.cafe_table_ids.add(table)
        self.client.login(email='test@test.com', password='123')

    def test_in_table_view_correct(self):
        """ Testing if the content of specific table is correct """
        response = self.client.get('/tables/1')
        response_html = response.content.decode()
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response_html, render_to_string('denied.html'))
        self.assertTrue('testf testl' in response_html)  # names

    def test_csrf(self):
        """ Check to see whether a csrf token exists """
        response = self.client.get('/tables/1')
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_topic_valid_post_data(self):
        """ Adding new message content and testing to see if it's correctly
        read """
        data = {
            'message_content': 'Test msg',
        }
        response = self.client.post('/tables/1', data)
        response_html = response.content.decode()
        self.assertTrue(Message.objects.exists())

    def test_new_topic_empty_post_data(self):
        """ Testing to see whether an emtpy message content is correctly
        identified """
        data = {
            'message_content': '',
        }
        response = self.client.post('/tables/1', data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Message.objects.exists())

    def test_in_table_view_not_part_table(self):
        """ Testing to see if a wrong table is correctly identified """
        response = self.client.get('/tables/2')
        response_html = response.content.decode()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_html, render_to_string('denied.html'))

    def test_in_table_view_not_exist_table(self):
        """ Testing to see if a non existant table is correctly identified """
        response = self.client.get('/tables/3')
        response_html = response.content.decode()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_html, render_to_string('denied.html'))


class DashboardTests(TestCase):
    """ Unit tests for the dashboard page """

    def setUp(self):
        """ Setting up tables with content for unit testing """
        table = CafeTable.objects.create(table_id='Test',
                                         university='Test uni')
        table2 = CafeTable.objects.create(table_id='Test 2',
                                          university='Test uni')
        user = CoffeeUser.objects.create_user(
            email='test@test.com', first_name='testf', last_name='testl',
            university='Test uni', is_staff=False, password='123'
        )
        user.cafe_table_ids.add(table)
        self.client.login(email='test@test.com', password='123')

    def test_status_code(self):
        """ Testing the status of the dashboard page (if it's 200) """
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)


class EditInfoTests(TestCase):
    """ Unit tests for the edit information page """

    def setUp(self):
        """ Setting up tables with content for unit testing """
        table = CafeTable.objects.create(table_id='Test',
                                         university='Test uni')
        table2 = CafeTable.objects.create(table_id='Test 2',
                                          university='Test uni')
        user = CoffeeUser.objects.create_user(
            email='test@test.com', first_name='testf', last_name='testl',
            university='Test uni', is_staff=False, password='123'
        )
        user.cafe_table_ids.add(table)
        self.client.login(email='test@test.com', password='123')

    def test_status_code(self):
        """ Testing the status of the edit info page (if it's 200) """
        response = self.client.get('/dashboard/edit_info')
        self.assertEqual(response.status_code, 200)

    def test_csrf(self):
        """ Checking whether a csrf token exists """
        response = self.client.get('/dashboard/edit_info')
        self.assertContains(response, 'csrfmiddlewaretoken')


class SetTaskTests(TestCase):
    """ Unit tests for the set task page """

    def setUp(self):
        """ Setting up tables with content for unit testing """
        table = CafeTable.objects.create(table_id='Test',
                                         university='Test uni')
        table2 = CafeTable.objects.create(table_id='Test 2',
                                          university='Test uni')
        user = CoffeeUser.objects.create_user(
            email='test@test.com', first_name='testf', last_name='testl',
            university='Test uni', is_staff=True, password='123'
        )
        user.cafe_table_ids.add(table)
        self.client.login(email='test@test.com', password='123')

    def test_status_code(self):
        """ Testing the status of the set tasks page (if it's 200) """
        response = self.client.get('/set_tasks')
        self.assertEqual(response.status_code, 200)

    def test_csrf(self):
        """ Checking whether a csrf token exists """
        response = self.client.get('/set_tasks')
        self.assertContains(response, 'csrfmiddlewaretoken')


class ViewTaskTests(TestCase):
    """ Unit tests for the view tasks page """

    def setUp(self):
        """ Setting up tables with content for unit testing """
        table = CafeTable.objects.create(table_id='Test',
                                         university='Test uni')
        table2 = CafeTable.objects.create(table_id='Test 2',
                                          university='Test uni')
        user = CoffeeUser.objects.create_user(
            email='test@test.com', first_name='testf', last_name='testl',
            university='Test uni', is_staff=False, password='123'
        )
        user.cafe_table_ids.add(table)
        self.client.login(email='test@test.com', password='123')
        task = Task.objects.create(task_name="tasktest", table_id=table,
                                   created_by=user, task_content="lol",
                                   points=1)

    def test_status_code(self):
        """ Testing the status of the view tasks page (if it's 200) """
        response = self.client.get('/view_tasks')
        self.assertEqual(response.status_code, 200)
