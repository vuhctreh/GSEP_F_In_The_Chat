# -*- coding: utf-8 -*-
from django.test import SimpleTestCase, TestCase, Client
from .models import CafeTable, CoffeeUser, Message
from django.template.loader import render_to_string


client = Client()


class HealthEndpointTests(SimpleTestCase):
    def test_health_status_is_up(self):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '{"status": "UP"}')


class LogInTests(TestCase):
    def test_login_view_status_code(self):
        response = self.client.get('')  # login page
        self.assertEquals(response.status_code, 200)

    def test_csrf(self):
        response = self.client.get('')
        self.assertContains(response, 'csrfmiddlewaretoken')


class SignUpTests(TestCase):
    def test_signup_view_status_code(self):
        response = self.client.get('/signup')
        self.assertEquals(response.status_code, 200)

    def test_csrf(self):
        response = self.client.get('/signup')
        self.assertContains(response, 'csrfmiddlewaretoken')


class PrivacyPolicyTests(TestCase):
    def test_privacy_policy_view_status_code(self):
        response = self.client.get('/privacy')
        self.assertEquals(response.status_code, 200)


class TermsTests(TestCase):
    def test_tandc_view_status_code(self):
        response = self.client.get('/terms')
        self.assertEquals(response.status_code, 200)


class TablesViewTests(TestCase):
    def setUp(self):
        table = CafeTable.objects.create(table_id='Test',
                                         university='Test uni')
        table2 = CafeTable.objects.create(table_id='Test 2',
                                          university='Test uni')
        user = CoffeeUser.objects.create_user(
            email='test@test.com', first_name='testf', last_name='testl',
            university='Test uni', is_staff=False, accept_terms=True,
            password='123'
        )
        user.cafe_table_ids.add(table)
        self.client.login(email='test@test.com', password='123')

    def test_tables_view_status_code(self):
        response = self.client.get('/table_view')
        self.assertEquals(response.status_code, 200)

    def test_tables_view_content(self):
        response = self.client.get('/table_view')
        response_html = response.content.decode()
        self.assertEquals(response.status_code, 200)
        self.assertTrue('Test' in response_html)
        self.assertFalse('Test 2' in response_html)


class InTableTests(TestCase):
    def setUp(self):
        table = CafeTable.objects.create(table_id='Test',
                                         university='Test uni')
        table2 = CafeTable.objects.create(table_id='Test 2',
                                          university='Test uni')
        user = CoffeeUser.objects.create_user(
            email='test@test.com', first_name='testf', last_name='testl',
            university='Test uni', is_staff=False, accept_terms=True,
            password='123'
        )
        user.cafe_table_ids.add(table)
        self.client.login(email='test@test.com', password='123')

    def test_in_table_view_correct(self):
        response = self.client.get('/tables/1')
        response_html = response.content.decode()
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(response_html, render_to_string('denied.html'))
        self.assertTrue('testf testl' in response_html)  # names

    def test_csrf(self):
        response = self.client.get('/tables/1')
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_topic_valid_post_data(self):
        data = {
            'message_content': 'Test msg',
        }
        response = self.client.post('/tables/1', data)
        response_html = response.content.decode()
        self.assertTrue(Message.objects.exists())
        self.assertTrue('Test msg' in response_html)

    def test_new_topic_empty_post_data(self):
        data = {
            'message_content': '',
        }
        response = self.client.post('/tables/1', data)
        self.assertFalse(Message.objects.exists())

    def test_in_table_view_not_part_table(self):
        response = self.client.get('/tables/2')
        response_html = response.content.decode()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response_html, render_to_string('denied.html'))

    def test_in_table_view_not_exist_table(self):
        response = self.client.get('/tables/3')
        response_html = response.content.decode()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response_html, render_to_string('denied.html'))
