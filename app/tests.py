""" Functions used for Unit Testing our web application """

from django.test import SimpleTestCase, TestCase, Client
from django.template.loader import render_to_string
from app.models import CafeTable, CoffeeUser, Message, Report, Task

client = Client()


class LogInTests(TestCase):
    """ Unit tests for login page """

    def test_login_view_status_code(self):
        """ Testing whether the status of the login page is OK (if it's reachable) """
        response = self.client.get('')  # login page
        self.assertEqual(response.status_code, 200)

    def test_csrf(self):
        """ Testing whether a csrf token exists for security """
        response = self.client.get('')
        self.assertContains(response, 'csrfmiddlewaretoken')


class SignUpTests(TestCase):
    """ Unit tests for signup page """

    def test_signup_view_status_code(self):
        """ Testing whether the status of the signup page is OK (if it's reachable) """
        response = self.client.get('/signup')
        self.assertEqual(response.status_code, 200)

    def test_csrf(self):
        """ Testing whether a csrf token exists for security """
        response = self.client.get('/signup')
        self.assertContains(response, 'csrfmiddlewaretoken')


class PrivacyPolicyTests(TestCase):
    """ Unit tests for privacy policy page """

    def test_privacy_policy_view_status_code(self):
        """ Testing whether the status of the privacy policy page is OK (if it's reachable) """
        response = self.client.get('/privacy')
        self.assertEqual(response.status_code, 200)


class TermsTests(TestCase):
    """ Unit tests for terms and conditions page """

    def test_tandc_view_status_code(self):
        """ Testing whether the status of the terms & conditions page is OK (if it's reachable) """
        response = self.client.get('/terms')
        self.assertEqual(response.status_code, 200)


class TablesViewTests(TestCase):
    """ Unit tests for table view page """

    def setUp(self):
        """ Setting up test tables with content for testing """
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
        """ Testing whether the status of the tables view page is OK (if it's reachable) """
        response = self.client.get('/table_view')
        self.assertEqual(response.status_code, 200)

    def test_tables_view_content(self):
        """ Testing to see whether the correct table name is displayed """
        response = self.client.get('/table_view')
        response_html = response.content.decode()
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Test' in response_html)
        self.assertFalse('Test 2' in response_html)


class InTableTests(TestCase):
    """ Unit tests for table content pages """

    def setUp(self):
        """ Setting up test tables with content for testing """
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
        """ Testing to see whether the correct table content is displayed """
        response = self.client.get('/tables/1')
        response_html = response.content.decode()
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response_html, render_to_string('denied.html'))
        self.assertTrue('testf testl' in response_html)  # names

    def test_csrf(self):
        """ Testing whether a csrf token exists for security """
        response = self.client.get('/tables/1')
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_topic_valid_post_data(self):
        """ Testing to see whether the inputted message content is correctly identified """
        data = {
            'message_content': 'Test msg',
        }
        response = self.client.post('/tables/1', data)
        response_html = response.content.decode()
        self.assertTrue(Message.objects.exists())

    def test_new_topic_empty_post_data(self):
        """ Testing to see if a message with no content is correctly identified """
        data = {
            'message_content': '',
        }
        response = self.client.post('/tables/1', data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Message.objects.exists())

    def test_in_table_view_not_part_table(self):
        """ Testing to see if incorrect table view is correctly identified
            and handled 
        """
        response = self.client.get('/tables/2')
        response_html = response.content.decode()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_html, render_to_string('denied.html'))

    def test_in_table_view_not_exist_table(self):
        """ Testing to see if non existent table view is correctly identified
            and handled 
        """
        response = self.client.get('/tables/3')
        response_html = response.content.decode()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_html, render_to_string('denied.html'))


class DashboardTests(TestCase):
    """ Unit tests for dashboard page """

    def setUp(self):
        """ Setting up test tables with content for testing """
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
        """ Testing whether the status of the dashboard page is OK (if it's reachable) """
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)


class EditInfoTests(TestCase):
    """ Unit tests for edit info page """

    def setUp(self):
        """ Setting up test tables with content for testing """
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
        """ Testing whether the status of the edit info page is OK (if it's reachable) """
        response = self.client.get('/dashboard/edit_info')
        self.assertEqual(response.status_code, 200)

    def test_csrf(self):
        """ Testing whether a csrf token exists for security """
        response = self.client.get('/dashboard/edit_info')
        self.assertContains(response, 'csrfmiddlewaretoken')
    
    def test_template(self):
        """ Testing whether the edit info page is used """
        response = self.client.get('/dashboard/edit_info')
        self.assertTemplateUsed(response, 'edit_info.html')

    def test_changin_info(self):
        """ Testing to see whether edits in the edit info page are correctly identified """
        data = {
            'first_name': 'testfirstname',
            'last_name': 'testlastname',
            'add_table_id': 69,
        }

        self.assertEqual(CoffeeUser.objects.get(email='test@test.com').first_name, 'testf')
        self.assertEqual(CoffeeUser.objects.get(email='test@test.com').last_name, 'testl')
        self.assertContains(CoffeeUser.objects.get(email='test@test.com').cafe_table_ids, 69)

        request = self.client.post('/dashboard/edit_info', data)

        self.assertEqual(CoffeeUser.objects.get(email='test@test.com').first_name, 'testfirstname')
        self.assertEqual(CoffeeUser.objects.get(email='test@test.com').last_name, 'testlastname')


class SetTaskTests(TestCase):
    """ Unit tests for set tasks page """

    def setUp(self):
        """ Setting up test tables with content for testing """
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
        """ Testing whether the status of the set tasks page is OK (if it's reachable) """
        response = self.client.get('/set_tasks')
        self.assertEqual(response.status_code, 200)

    def test_csrf(self):
        """ Testing whether a csrf token exists for security """
        response = self.client.get('/set_tasks')
        self.assertContains(response, 'csrfmiddlewaretoken')
    
    def test_template(self):
        """ Testing whether set tasks page is successfully used """
        response = self.client.get('/set_tasks')
        self.assertTemplateUsed(response, 'set_tasks.html')

    def task_in_db_test(self):
        """ Testing to see if setting a new task is correctly registered """
        data = {
            'task_name': 'Test-213943',
            'created_by': '',
            'table_id': '',
            'task_content': '',
            'points': '',
            'recurrence_interval': '',
            'max_repeats': '',
        }

        self.assertTrue(Task.objects.count(), 0)

        response = self.client.post('/set_tasks', data)

        self.assertTrue(Task.objects.count(), 1)
        self.assertTrue(Task.objects.filter(task_name='Test-213943').exists())

class ViewTaskTests(TestCase):
    """ Unit tests for view tasks page """

    def setUp(self):
        """ Setting up test tables with content for testing """
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
        task_should_not_be_displayed = Task.objects.create(task_name="tasktestNO", table_id=table2,
                                   created_by=user, task_content="lol",
                                   points=1)

    def test_status_code(self):
        """ Testing whether the status of the view tasks page is OK (if it's reachable) """
        response = self.client.get('/view_tasks')
        self.assertEqual(response.status_code, 200)
    
    def task_exists_in_db_test(self):
        """ Testing database to see if created task is correctly registered """
        self.assertTrue(Report.objects.count(), 1)
    
    def template_connection_test(self):
        """ Testing whether view tasks page template is used """
        response = self.client.get('/view_tasks')
        self.assertTemplateUsed(response, 'view_tasks.html')
    
    def right_tasks_displayed_test(self):
        """ Testing to see if only the tasks for the specific table are displayed """
        response = self.client.get('/view_tasks')
        self.assertContains(response, 'tasktest')
        self.assertNotContains(response, 'tasktestNO')
        # Tasks only from the correct tables are displayed

class ReportingTests(TestCase):
    """ Unit tests for reports page """

    def setUp(self):
        """ Setting up test tables with content for testing """
        table = CafeTable.objects.create(table_id='Test',
                                         university='Test uni')
        table2 = CafeTable.objects.create(table_id='Test 2',
                                          university='Test uni')
        self.user = CoffeeUser.objects.create_user(
            email='test@test.com', first_name='testf', last_name='testl',
            university='Test uni', is_staff=False, password='123'
        )
        self.user.cafe_table_ids.add(table)
        self.client.login(email='test@test.com', password='123')
    
    def test_status_code(self):
        """ Testing whether the status of the report page is OK (if it's reachable) """
        response = self.client.get('/report')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'report.html')

    def test_csrf(self):
        """ Testing whether a csrf token exists for security """
        response = self.client.get('/report')
        self.assertContains(response, 'csrfmiddlewaretoken')

    def create_report_test(self):
        """ Testing whether a created report is managed correctly """
        data = {
            'title': 'TestReport-213943',
            'category': '',
            'detail': '',
            'table_id': '',
            'flagged_by': '',
        }
        
        self.assertTrue(Report.objects.count(), 0)

        response = self.client.post('/report', data)

        # Check request is successful
        self.assertTrue(response.status_code, 200)

        # Check object created in database
        self.assertTrue(Report.objects.count(), 1)
        self.assertTrue(Report.objects.filter(title='TestReport-213943').exists())


class HealthEndpointTests(SimpleTestCase):
    """ Unit tests for overall web application status"""

    def test_health_status_is_up(self):
        """ Testing whether the application as a whole is reachable """
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '{"status": "UP"}')

class PrivacyAndTermsTests(SimpleTestCase):
    """ Unit tests for privacy, terms and conditions page """
    def privacy_policy_status_is_up(self):
        response = self.client.get('/privacy')
        self.assertEqual(response.status_code, 200)
    
    def tos_status_is_up(self):
        """ Testing whether the status of the privacy policy and 
            terms of service pages are OK (if they're reachable)  
        """
        response = self.client.get('/terms')
        self.assertEqual(response.status_code, 200)