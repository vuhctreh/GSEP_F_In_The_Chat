""" Placeholder """

from django.test import SimpleTestCase, TestCase, Client
from django.template.loader import render_to_string
from app.models import CafeTable, CoffeeUser, Message, Report, Task

client = Client()


class LogInTests(TestCase):
    """ Placeholder """

    def test_login_view_status_code(self):
        """ Placeholder """
        response = self.client.get('')  # login page
        self.assertEqual(response.status_code, 200)

    def test_csrf(self):
        """ Placeholder """
        response = self.client.get('')
        self.assertContains(response, 'csrfmiddlewaretoken')


class SignUpTests(TestCase):
    """ Placeholder """

    def test_signup_view_status_code(self):
        """ Placeholder """
        response = self.client.get('/signup')
        self.assertEqual(response.status_code, 200)

    def test_csrf(self):
        """ Placeholder """
        response = self.client.get('/signup')
        self.assertContains(response, 'csrfmiddlewaretoken')


class PrivacyPolicyTests(TestCase):
    """ Placeholder """

    def test_privacy_policy_view_status_code(self):
        """ Placeholder """
        response = self.client.get('/privacy')
        self.assertEqual(response.status_code, 200)


class TermsTests(TestCase):
    """ Placeholder """

    def test_tandc_view_status_code(self):
        """ Placeholder """
        response = self.client.get('/terms')
        self.assertEqual(response.status_code, 200)


class TablesViewTests(TestCase):
    """ Placeholder """

    def setUp(self):
        """ Placeholder """
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
        """ Placeholder """
        response = self.client.get('/table_view')
        self.assertEqual(response.status_code, 200)

    def test_tables_view_content(self):
        """ Placeholder """
        response = self.client.get('/table_view')
        response_html = response.content.decode()
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Test' in response_html)
        self.assertFalse('Test 2' in response_html)


class InTableTests(TestCase):
    """ Placeholder """

    def setUp(self):
        """ Placeholder """
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
        """ Placeholder """
        response = self.client.get('/tables/1')
        response_html = response.content.decode()
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response_html, render_to_string('denied.html'))
        self.assertTrue('testf testl' in response_html)  # names

    def test_csrf(self):
        """ Placeholder """
        response = self.client.get('/tables/1')
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_topic_valid_post_data(self):
        """ Placeholder """
        data = {
            'message_content': 'Test msg',
        }
        response = self.client.post('/tables/1', data)
        response_html = response.content.decode()
        self.assertTrue(Message.objects.exists())

    def test_new_topic_empty_post_data(self):
        """ Placeholder """
        data = {
            'message_content': '',
        }
        response = self.client.post('/tables/1', data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Message.objects.exists())

    def test_in_table_view_not_part_table(self):
        """ Placeholder """
        response = self.client.get('/tables/2')
        response_html = response.content.decode()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_html, render_to_string('denied.html'))

    def test_in_table_view_not_exist_table(self):
        """ Placeholder """
        response = self.client.get('/tables/3')
        response_html = response.content.decode()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_html, render_to_string('denied.html'))


class DashboardTests(TestCase):
    """ Placeholder """

    def setUp(self):
        """ Placeholder """
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
        """ Placeholder """
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)


class EditInfoTests(TestCase):
    """ Placeholder """

    def setUp(self):
        """ Placeholder """
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
        """ Placeholder """
        response = self.client.get('/dashboard/edit_info')
        self.assertEqual(response.status_code, 200)

    def test_csrf(self):
        """ Placeholder """
        response = self.client.get('/dashboard/edit_info')
        self.assertContains(response, 'csrfmiddlewaretoken')
    
    def test_template(self):
        response = self.client.get('/dashboard/edit_info')
        self.assertTemplateUsed(response, 'edit_info.html')

    def test_changin_info(self):
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
    """ Placeholder """

    def setUp(self):
        """ Placeholder """
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
        """ Placeholder """
        response = self.client.get('/set_tasks')
        self.assertEqual(response.status_code, 200)

    def test_csrf(self):
        """ Placeholder """
        response = self.client.get('/set_tasks')
        self.assertContains(response, 'csrfmiddlewaretoken')
    
    def test_template(self):
        response = self.client.get('/set_tasks')
        self.assertTemplateUsed(response, 'set_tasks.html')

    def task_in_db_test(self):
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
    """ Placeholder """

    def setUp(self):
        """ Placeholder """
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
        """ Tests if the page is reachable """
        response = self.client.get('/view_tasks')
        self.assertEqual(response.status_code, 200)
    
    def task_exists_in_db_test(self):
        self.assertTrue(Report.objects.count(), 1)
    
    def template_connection_test(self):
        response = self.client.get('/view_tasks')
        self.assertTemplateUsed(response, 'view_tasks.html')
    
    def right_tasks_displayed_test(self):
        response = self.client.get('/view_tasks')
        self.assertContains(response, 'tasktest')
        self.assertNotContains(response, 'tasktestNO')
        # Tasks only from the correct tables are displayed

class ReportingTests(TestCase):

    def setUp(self):
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
        """ Tests if the page is reachable """
        response = self.client.get('/report')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'report.html')

    def test_csrf(self):
        """ Placeholder """
        response = self.client.get('/report')
        self.assertContains(response, 'csrfmiddlewaretoken')

    def create_report_test(self):
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
    """ Placeholder """

    def test_health_status_is_up(self):
        """ Placeholder """
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '{"status": "UP"}')

class PrivacyAndTermsTests(SimpleTestCase):
    """
    Tests the Terms and Conditions and Privacy Policy pages to ensure they're up and working
    """
    def privacy_policy_status_is_up(self):
        response = self.client.get('/privacy')
        self.assertEqual(response.status_code, 200)
    
    def tos_status_is_up(self):
        response = self.client.get('/terms')
        self.assertEqual(response.status_code, 200)