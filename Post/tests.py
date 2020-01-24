from django.test import TestCase
from .models import Post, Reply
from django.test import Client
from django.urls import reverse, resolve
from .views import PostListView
from markdownx.utils import markdownify
from django.utils import timezone
import datetime
from django.contrib.auth.models import User

# ====================== MODEL TESTS ===================
content = """
    Business intelligence (BI) leverages software and services to transform data into actionable insights that inform an organization’s strategic and tactical business decisions. BI tools access and analyze data sets and present analytical findings in reports, summaries, dashboards, graphs, 
    charts and maps to provide users with detailed intelligence about the state of the business.The term busines o actionable insights that inform an organization’s
"""
class PostTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username= 'testuser', password='45rtyfj'
        )
        user.save()

        post = Post.objects.create(
            title="Nothing", content=content, created_on = timezone.now(),
            genre='GV', author = user
        )
        post.save()

    def test_post_title(self):
        post = Post.objects.get(pk=1)
        self.assertEquals(post.title, 'Nothing')

    def test_post_truncate_content_method(self):
        post = Post.objects.get(pk=1)
        self.assertNotEquals(len(post.truncate_content()), len(post.content))

    def test_post_get_absolute_url(self):
        post = Post.objects.get(pk=1)
        self.assertEquals(post.get_absolute_url(),'/post/1/')

class ReplyTest(TestCase):
    def reply_name(self):
        pass

#======================= VIEWS TEST ===================================
# Test the views: Use the Client to mimic the browser
class PostListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_post =8

        for i in range(number_of_post):
            user = User.objects.create_user(
                username=f'testuser{i}', password=f'45rtyfj{i}'
            )
            user.save()

            post = Post.objects.create(
                title= f"Nothing {i}", content=f"{content} {i}", created_on=timezone.now(),
                genre='GV', author=user
            )
            post.save()

    def setUp(self):
        pass

    def test_post_list_view_url(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_post_list_view_template_name(self):
        response = self.client.get(reverse('list-view'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_post_list_view_name(self):
        response = self.client.get(reverse('list-view'))
        self.assertEquals(response.status_code, 200)
        # self.assertEquals(response.view_name, 'list-view')

    def test_post_list_view_order(self):
        response = self.client.get(reverse('list-view'))
        self.assertEquals(response.status_code, 200)
        
        last_date = 0
        for post in response.context['object_list']:
            if last_date == 0:
                last_date = post.created_on
            else:
                self.assertTrue(last_date <= post.created_on)  
                last_date = post.created_on

    def test_post_list_pagination(self):
        response = self.client.get(reverse('list-view'))
        self.assertEquals(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(len(response.context['object_list']) == 2)

    def test_post_list_pagination_next_page(self):
        response = self.client.get(reverse('list-view')+'?page=2')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.context['object_list']),2)

    
class PostDetailViewTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username='testuser', password='45rtyfj'
        )
        user.save()

        post = Post.objects.create(
            title="Nothing", content=content, created_on=timezone.now(),
            genre='GV', author=user
        )
        post.save()

    def test_post_detail_with_pk_exists(self):
        response = self.client.get('/post/1/')
        self.assertEquals(response.status_code, 200)

    def test_invalid_post_detail_pk(self):
        response = self.client.get('/post/2/')
        self.assertEquals(response.status_code, 404)

    def test_post_detail_view_url(self):
        response = self.client.get('/post/1/')
        self.assertEquals(response.status_code, 200)
        # self.assertEquals(response, '/post/1/')

    def test_post_detail_view_template_name(self):
        response = self.client.get('/post/1/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'post_detail.html')

class PostCreateViewTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username='testuser', password='45rtyfj'
        )
        user.save()

        post = Post.objects.create(
            title="Nothing", content=content, created_on=timezone.now(),
            genre='GV', author=user
        )
        post.save()

    def test_csrf(self):
        url = reverse('post-detail', kwargs={'pk':1})
        login = self.client.login(username='testuser', password='45rtyfj')

        response = self.client.get(url,{})
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_user_login_redirect_before_creating_post(self):
        response = self.client.get(reverse('post-create'))
        self.assertRedirects(response,'/user/login/?next=/post/create/')

    def test_new_post_valid_data(self):
        user = User.objects.get(pk=1)
        data = {
            'title': "Nothing", 'content': content, 'created_on': timezone.now(),
            'genre': 'GV', 'author': user
        }

        login = self.client.login(username=user.username, password=user.password)
        response = self.client.post(reverse('post-create'), data)
        self.assertTrue(Post.objects.exists())

    def test_new_post_invalid_data(self):
        """
        Invalid data should not redirect to post-detail
        Expected: Show form again with validation errors
        """
        response = self.client.post(
            reverse('post-create'), {})
        self.assertTrue(response.status_code, 200)

    def test_new_post_invalid_empty_data(self):
        user = User.objects.get(pk=1)
        data = {
            'title': "", 'created_on': timezone.now(),
            'genre': '', 'author': user
        }

        url = reverse('post-create')
        login = self.client.login(username='testuser', password='45rtyfj')
        response = self.client.post(url, data)

        self.assertEquals(response.status_code, 200)
        # self.assertFalse(Post.objects.exists()) #=======================

    def test_new_post_redirect_url(self):
        user = User.objects.get(pk=1)
        data = {
            'title': "Nothing", 'content': content, 'created_on': timezone.now(),
            'genre': 'GV', 'author': user
        }
        url = reverse('post-create')
        login = self.client.login(username='testuser', password='45rtyfj')
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)

    def test_new_post_template(self):
        user = User.objects.get(pk=1)
        data = {
            'title': "Nothing", 'content': content, 'created_on': timezone.now(),
            'genre': 'GV', 'author': user
        }
        url = reverse('post-create')
        login = self.client.login(username='testuser', password='45rtyfj')
        response = self.client.post(url, data)

        self.assertTemplateUsed(response,'post_create.html')
        
class PostUpdateViewTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username='testuser', password='45rtyfj'
        )
        user.save()

        post = Post.objects.create(
            title="Nothing", content=content, created_on=timezone.now(),
            genre='GV', author=user
        )
        post.save()

    def test_post_author_is_logged_in_user(self):
        response = self.client.get(reverse('post-update', kwargs={'pk':1}))
        self.assertRedirects(response, '/user/login/?next=/post/update/1/')

    def test_update_post_valid_data(self):
        pass

    def test_update_post_invalid_data(self):
        pass

    def test_update_redirect_url(self):
        pass

    def test_update_template(self):
        pass

    def test_update_form_url(self):
        # Test success_url
        login = self.client.login(username='testuser', password='45rtyfj')
        response = self.client.get('/post/update/1/')
        self.assertEquals(response.status_code, 200)

class PostDeleteView(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username='testuser', password='45rtyfj'
        )
        user.save()

        post = Post.objects.create(
            title="Nothing", content=content, created_on=timezone.now(),
            genre='GV', author=user
        )
        post.save()

    def test_inexistent_post_delete(self):
        url = reverse('post-delete', kwargs={'pk': 2})
        login = self.client.login(username='testuser', password='45rtyfj')
        response = self.client.delete(url)

        self.assertEquals(response.status_code, 404)

    def test_valid_post_delete(self):
        """
        Expected a successful delete lead to redirection
        """
        url = reverse('post-delete', kwargs={'pk':1})
        response = self.client.delete(url)
        
        self.assertEquals(response.status_code, 302)
    
    def test_post_delete_redirect_url(self):
        url = reverse('post-delete',kwargs={'pk':1})
        response = self.client.delete(url)
        self.assertRedirects(response, '/user/login/?next=/post/delete/1/')

class PostSearchViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_post =8

        user = User.objects.create_user(
            username='testuser', password=f'45rtyfj'
        )
        user.save()

        for i in range(number_of_post):
            post = Post.objects.create(
                title= f"Nothing {i}", content=f"{content} {i}", created_on=timezone.now(),
                genre='GV', author=user
            )
            post.save()
    
    def setUp(self):
        pass

    def test_inexistent_post(self):
        url = reverse('list-view')
        response = self.client.get(url, {'q': 'Running'})
        self.assertEquals(len(response.context['object_list']), 0)

    def test_with_empty_search_query(self):
        """
        Expected: Return Eight post
        """
        url = reverse('list-view')
        response = self.client.get(url, {'q': ''})
        self.assertEquals(len(response.context['object_list']) , 2)

    def test_with_valid_search_query(self):
        url = reverse('list-view')
        response = self.client.get(url, {'q':'Nothing'})
        # print(response.context)
        self.assertEquals(len(response.context['object_list']) , 2)

class PostReplyViewTest(TestCase):
    def setUp(self):
        pass

    def test_reply_get_request(self):
        pass

    def test_reply_post_request(self):
        pass

    def test_reply_with_invalid_data(self):
        pass

# Test the forms
class RepyFormTest(TestCase):
    def test_form_date_is_naive(self):
        pass

    def test_test_form_date_isnot_naive(self):
        pass

    def test_form_errors(self):
        pass

class PostForm(TestCase):
    def test_form_date_is_naive(self):
        pass

    def test_form_date_isnot_naive(self):
        pass

    def test_form_errors(self):
        pass

    def test_form_help_text(self):
        pass



"""
  assertContains() (SimpleTestCase method), 
  351 assertFieldOutput() (SimpleTestCase method),
  350 assertFormError() (SimpleTestCase method),
  350 assertFormsetError() (SimpleTestCase method),
  351 assertHTMLEqual() (SimpleTestCase method), 
  352 assertHTMLNotEqual() (SimpleTestCase method), 
  352 assertInHTML() (SimpleTestCase method), 
  353 assertJSONEqual() (SimpleTestCase method), 
  353 assertJSONNotEqual() (SimpleTestCase method), 
  353 assertNotContains() (SimpleTestCase method), 
  351 assertNumQueries() (TransactionTestCase method), 
  353 assertQuerysetEqual() (TransactionTestCase method), 
  353 assertRaisesMessage() (SimpleTestCase method), 
  350 assertRedirects() (SimpleTestCase method), 
  352 assertTemplateNotUsed() (SimpleTestCase method), 
  351 assertTemplateUsed() (SimpleTestCase method), 
  351 assertURLEqual() (SimpleTestCase method), 
  351 assertWarnsMessage() (SimpleTestCase method), 
  350 assertXMLEqual() (SimpleTestCase method), 
  352 assertXMLNotEqual() (SimpleTestCase method), 
  353 AsSVG (class in django.contrib.gis.db.models.functions), 827



  Commands:
  --verbosity=0,1,2
"""
