""" Functions used for Unit Testing our web application """

from django.test import SimpleTestCase, TestCase, Client
from django.template.loader import render_to_string
from app.models import CafeTable, CoffeeUser, Message, Report, Task

client = Client()


class LogInTests(TestCase):
    """ Unit tests for login page """

    def test_login_view_status_code(self):
        """ Testing whether the status of the login page is OK
        (if it's reachable) """
        resp = self.client.get('')  # login page
        self.assertEqual(resp.status_code, 200)

    def test_csrf(self):
        """ Testing whether a csrf token exists for security """
        resp = self.client.get('')
        self.assertContains(resp, 'csrfmiddlewaretoken')

    def test_template(self):
        """ Testing the correct template is rendered """
        resp = self.client.get('')
        self.assertTemplateUsed(resp, 'login.html')


class SignUpTests(TestCase):
    """ Unit tests for signup page """

    def test_signup_view_status_code(self):
        """ Testing whether the status of the signup page is OK
        (if it's reachable) """
        resp = self.client.get('/signup')
        self.assertEqual(resp.status_code, 200)

    def test_csrf(self):
        """ Testing whether a csrf token exists for security """
        resp = self.client.get('/signup')
        self.assertContains(resp, 'csrfmiddlewaretoken')

    def test_template(self):
        """ Testing the correct template is rendered """
        resp = self.client.get('/signup')
        self.assertTemplateUsed(resp, 'sign_up.html')


class PrivacyPolicyTests(TestCase):
    """ Unit tests for privacy policy page """

    def test_privacy_policy_view_status_code(self):
        """ Testing whether the status of the privacy policy page is OK
        (if it's reachable) """
        resp = self.client.get('/privacy')
        self.assertEqual(resp.status_code, 200)


class TermsTests(TestCase):
    """ Unit tests for terms and conditions page """

    def test_tandc_view_status_code(self):
        """ Testing whether the status of the terms & conditions page is OK
        (if it's reachable) """
        resp = self.client.get('/terms')
        self.assertEqual(resp.status_code, 200)


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
        """ Testing whether the status of the tables view page is OK
        (if it's reachable) """
        resp = self.client.get('/table_view')
        self.assertEqual(resp.status_code, 200)

    def test_tables_view_content(self):
        """ Testing to see whether the correct table name is displayed """
        resp = self.client.get('/table_view')
        response_html = resp.content.decode()
        self.assertEqual(resp.status_code, 200)
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
        resp = self.client.get('/tables/1')
        response_html = resp.content.decode()
        self.assertEqual(resp.status_code, 200)
        self.assertNotEqual(response_html, render_to_string('denied.html'))
        self.assertTrue('testf testl' in response_html)  # names

    def test_csrf(self):
        """ Testing whether a csrf token exists for security """
        resp = self.client.get('/tables/1')
        self.assertContains(resp, 'csrfmiddlewaretoken')

    def test_new_message_valid_post_data(self):
        """ Testing to see whether the inputted message content is correctly
        identified """
        data = {
            'message_content': 'Test msg',
        }
        self.client.post('/tables/1', data)
        self.assertTrue(Message.objects.exists())
        resp = self.client.get('/get_msgs/1')
        response_html = resp.content.decode()
        self.assertTrue('Test msg' in response_html)

    def test_new_message_empty_post_data(self):
        """ Testing to see if a message with no content is correctly
        identified """
        data = {
            'message_content': '',
        }
        resp = self.client.post('/tables/1', data)
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(Message.objects.exists())

    def test_upvote(self):
        """ Testing to see whether the inputted message content is correctly
        identified """
        data = {
            'message_content': 'Test msg',
        }
        self.client.post('/tables/1', data)
        msg = Message.objects.get(message_content='Test msg')
        self.client.get('/upvote/' + str(msg.id))
        resp = self.client.get('/get_msgs/1')
        response_html = resp.content.decode()
        self.assertTrue('1 Likes' in response_html)

    def test_in_table_view_not_part_table(self):
        """ Testing to see if incorrect table view is correctly identified
            and handled"""
        resp = self.client.get('/tables/2')
        response_html = resp.content.decode()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(response_html, render_to_string('denied.html'))

    def test_in_table_view_not_exist_table(self):
        """ Testing to see if non existent table view is correctly identified
            and handled"""
        resp = self.client.get('/tables/3')
        response_html = resp.content.decode()
        self.assertEqual(resp.status_code, 200)
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
        """ Testing whether the status of the dashboard page is OK
        (if it's reachable) """
        resp = self.client.get('/dashboard')
        self.assertEqual(resp.status_code, 200)

    def test_template(self):
        """ Testing the correct template is rendered """
        resp = self.client.get('/dashboard')
        self.assertTemplateUsed(resp, 'dashboard.html')

        # Check whether it's displaying the correct user
        response_html = resp.content.decode()
        self.assertTrue(CoffeeUser.objects.get(
            email='test@test.com').first_name in response_html)
        self.assertTrue(CoffeeUser.objects.get(
            email='test@test.com').last_name in response_html)

    def test_check_collectables(self):
        """ Testing the correct collectable is calculated """
        resp = self.client.get('/dashboard')
        response_html = resp.content.decode()
        self.assertTrue('Espresso' in response_html)
        self.assertTrue('Points till next collectable: 50' in response_html)


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
        """ Testing whether the status of the edit info page is OK
        (if it's reachable) """
        resp = self.client.get('/dashboard/edit_info')
        self.assertEqual(resp.status_code, 200)

    def test_csrf(self):
        """ Testing whether a csrf token exists for security """
        resp = self.client.get('/dashboard/edit_info')
        self.assertContains(resp, 'csrfmiddlewaretoken')

    def test_template(self):
        """ Testing whether the edit info page is used """
        resp = self.client.get('/dashboard/edit_info')
        self.assertTemplateUsed(resp, 'edit_info.html')

    def test_changing_info(self):
        """ Testing to see whether edits in the edit info page are correctly
        identified """
        data = {
            'first_name': 'testfirstname',
            'last_name': 'testlastname',
        }

        self.assertEqual(CoffeeUser.objects.get(
            email='test@test.com').first_name, 'testf')
        self.assertEqual(CoffeeUser.objects.get(
            email='test@test.com').last_name, 'testl')

        request = self.client.post('/dashboard/edit_info', data)

        self.assertEqual(CoffeeUser.objects.get(
            email='test@test.com').first_name, 'testfirstname')
        self.assertEqual(CoffeeUser.objects.get(
            email='test@test.com').last_name, 'testlastname')


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
        """ Testing whether the status of the set tasks page is OK
        (if it's reachable) """
        resp = self.client.get('/set_tasks')
        self.assertEqual(resp.status_code, 200)

    def test_csrf(self):
        """ Testing whether a csrf token exists for security """
        resp = self.client.get('/set_tasks')
        self.assertContains(resp, 'csrfmiddlewaretoken')

    def test_template(self):
        """ Testing whether set tasks page is successfully used """
        resp = self.client.get('/set_tasks')
        self.assertTemplateUsed(resp, 'set_tasks.html')

    def test_task_in_db(self):
        """ Testing to see if setting a new task is correctly registered """
        table = CafeTable.objects.get(id=1)
        data = {
            'task_name': 'f',
            'table_id': str(table.id),
            'task_content': 'fff',
            'points': 1,
            'recurrence_interval': 'n',
            'max_repeats': 0,
        }

        self.assertTrue(Task.objects.count() == 0)

        self.client.post('/set_tasks', data)

        self.assertTrue(Task.objects.count() == 1)


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
        user2 = CoffeeUser.objects.create_user(
            email='test2@test.com', first_name='testf', last_name='testl',
            university='Test uni', is_staff=True, password='123'
        )
        Task.objects.create(task_name="tasktest", table_id=table,
                            created_by=user2, task_content="lol", points=1)
        Task.objects.create(task_name="tasktestNTable", table_id=table2,
                            created_by=user2, task_content="lol", points=1)
        Task.objects.create(task_name="tasktestNUser", table_id=table2,
                            created_by=user, task_content="lol", points=1)
        user.cafe_table_ids.add(table)
        self.client.login(email='test@test.com', password='123')

    def test_status_code(self):
        """ Testing whether the status of the view tasks page is OK
        (if it's reachable) """
        resp = self.client.get('/view_tasks')
        self.assertEqual(resp.status_code, 200)

    def test_task_exists_in_db(self):
        """ Testing database to see if created task is correctly registered """
        self.assertTrue(Task.objects.count(), 1)

    def test_template_connection(self):
        """ Testing whether view tasks page template is used """
        resp = self.client.get('/view_tasks')
        self.assertTemplateUsed(resp, 'view_tasks.html')

    def test_right_tasks_displayed(self):
        """ Testing to see if only the tasks for the specific table are
        displayed """
        resp = self.client.get('/view_tasks')
        response_html = resp.content.decode()
        self.assertTrue('tasktest' in response_html)
        self.assertFalse('tasktestNTable' in response_html)
        self.assertFalse('tasktestNUser' in response_html)
        # Tasks only from the correct tables are displayed + cannot see own
        # tasks

    def test_complete_task(self):
        """ Tests points earn when task completed """
        self.client.get('/complete/1')
        resp = self.client.get('/view_tasks')
        response_html = resp.content.decode()
        user = CoffeeUser.objects.get(id=1)
        self.assertTrue(user.points == 3)
        self.assertFalse('tasktest' in response_html)


class ReportingTests(TestCase):
    """ Unit tests for reports page """

    def setUp(self):
        """ Setting up test tables with content for testing """
        table = CafeTable.objects.create(table_id='Test',
                                         university='Test uni')
        self.user = CoffeeUser.objects.create_user(
            email='test@test.com', first_name='testf', last_name='testl',
            university='Test uni', is_staff=False, password='123'
        )
        self.user.cafe_table_ids.add(table)
        self.client.login(email='test@test.com', password='123')

    def test_status_code(self):
        """ Testing whether the status of the report page is OK
        (if it's reachable) """
        resp = self.client.get('/report')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'report.html')

    def test_csrf(self):
        """ Testing whether a csrf token exists for security """
        resp = self.client.get('/report')
        self.assertContains(resp, 'csrfmiddlewaretoken')

    def test_create_report(self):
        """ Testing whether a created report is managed correctly """

        table = CafeTable.objects.get(id=1)

        self.client.get('/report')

        data = {
            'title': 'TestReport-213943',
            'category': "Other",
            'detail': 'fff',
            'table_id': str(table.id),
        }

        self.assertEqual(Report.objects.count(), 0)

        resp = self.client.post('/report', data)

        # Check request is successful
        self.assertTrue(resp.status_code, 200)

        # Check object created in database
        self.assertEqual(Report.objects.count(), 1)


class ProfileTests(TestCase):
    """ Unit tests for profile page """

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
        """ Testing whether the status of the profile page is OK
        (if it's reachable) """
        resp = self.client.get('/profile_page/1')
        self.assertEqual(resp.status_code, 200)

    def test_profile_not_exist_user(self):
        """ Testing to see if non existent user is correctly identified
            and handled"""
        resp = self.client.get('/profile_page/8')
        response_html = resp.content.decode()
        self.assertEqual(response_html, render_to_string(
            'profile_nonexistent.html'))

    def test_template(self):
        """ Testing the correct template is rendered """
        resp = self.client.get('/profile_page/1')
        self.assertTemplateUsed(resp, 'profile_page.html')

    def test_profile_content(self):
        """ Testing correct user is displayed """
        resp = self.client.get('/profile_page/1')
        response_html = resp.content.decode()
        self.assertTrue(CoffeeUser.objects.get(
            email='test@test.com').first_name in response_html)
        self.assertTrue(CoffeeUser.objects.get(
            email='test@test.com').last_name in response_html)


class HealthEndpointTests(SimpleTestCase):
    """ Unit tests for overall web application status"""

    def test_health_status_is_up(self):
        """ Testing whether the application as a whole is reachable """
        resp = self.client.get('/health')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, '{"status": "UP"}')


class ActiveUsersTest(TestCase):
    """ Unit test for function calculating number of active users."""

    def setUp(self):
        """ Setting up test tables with content for testing """
        user = CoffeeUser.objects.create_user(
            email='test@test.com', first_name='testf', last_name='testl',
            university='Test uni', is_staff=False, password='123'
        )
        self.client.login(email='test@test.com', password='123')

    def test_active_users(self):
        """ Testing to see if number of active users is correct """
        resp = self.client.get('/table_view')
        response_html = resp.content.decode()
        self.assertTrue('Users in Cafe: 1' in response_html)
