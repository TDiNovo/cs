import datetime
import unittest
import importlib
from django.utils import timezone
from django.test import TestCase
from django.test import RequestFactory
from django.http import HttpRequest
from image_space_app.views import *
from image_space_app.forms import *
from image_space_app.models import *
from django.core.urlresolvers import resolve
from django.test import Client

class ImageSpaceTests(TestCase):

    #Test ability for an existing user to log in (user is created then authenticated)
    def test_login(self):
        self.c = Client()
        self.user = User.objects.create(username = 'user1', password = 'password', is_active = True, is_superuser = False)
        self.user.set_password('hello') 
        self.user.save()
        self.user = authenticate(username = 'user1', password = 'hello')
        login = self.c.login(username = 'user1', password = 'hello')
        self.assertTrue(login)

    #Test that '/' goes to RootView view
    def test_root(self):
        res = resolve('/')
        view_name = res.view_name
        view_func = resolve(reverse(view_name)).func
        module = importlib.import_module(view_func.__module__)
        view = getattr(module, view_func.__name__)
        self.assertEqual(view, RootView)

    #Test that '/login' goes to LoginUserView view
    def test_login_view(self):

        req = RequestFactory().get('/login/')
        view = LoginUserView.as_view()

        response = view(req)
        
        self.assertEqual(response.status_code, 200 )


    #Test that '/register/' renders
    def test_register_view(self):
        res = resolve('/register/')
        view_name = res.view_name
        view_func = resolve(reverse(view_name)).func
        module = importlib.import_module(view_func.__module__)
        view = getattr(module, view_func.__name__)
        self.assertEqual(view, RegisterView)
        

    #Test the User form
    def test_user_form(self):
        form_vars = {'username' : 'testUser4', 'first_name' : 'Bob', 'last_name' : 'Tester', 'email' : 'test@test.com', 'password' : 'password'}
        form = UserForm(data = form_vars)
        self.assertEqual(form.is_valid(), True)
        user = form.save()
        self.assertEqual(user.username, 'testUser4')
        
    #Test that '/profile/' URL renders
    def test_profile_url(self):
        result = self.client.get('/profile/')
        self.assertEqual(result.status_code, 200)

        #Test that '/pictures/' goes to PicturesList view
    def test_pictures_view(self):
        res = resolve('/pictures/')
        view_name = res.view_name
        view_func = resolve(reverse(view_name)).func
        module = importlib.import_module(view_func.__module__)
        view = getattr(module, view_func.__name__)
        self.assertEqual(view, PicturesList)

    #Test that '/pictures/upload/' goes to PictureUpload view
    def test_PictureUpload_view(self):
        res = resolve('/pictures/upload')
        view_name = res.view_name
        view_func = resolve(reverse(view_name)).func
        module = importlib.import_module(view_func.__module__)
        view = getattr(module, view_func.__name__)
        self.assertEqual(view, PictureUpload)
            

    #Test that '/edit/' URL renders
    def test_edit_url(self):
        result = self.client.get('/edit/')
        self.assertEqual(result.status_code, 200)

    #Test that ProfileDetails view 'user_img' context is blank when no user image
    def test_profile_url_image_context_blank(self):
        result = self.client.get('/profile/')
        self.assertEqual(result.context['user_img'], "")


    #Test logout (first with an active user logged in)
    def test_logout_currently_logged_in(self):
        self.c = Client()
        self.user = User.objects.create(username = 'user1', password = 'password', is_active = True, is_superuser = False)
        self.user.set_password('hello') 
        self.user.save()
        self.user = authenticate(username = 'user1', password = 'hello')
        login = self.c.login(username = 'user1', password = 'hello')
        login = self.c.logout()
        self.assertIsNone(login)

    #Test logout view
    def test_logout_no_active_user(self):
        res = resolve('/logout/')
        self.assertEqual(res.func, log_out)

    #Test model
    def create_user(self):
        return User.objects.create(username = 'user2', password = 'password', is_active = True, is_superuser = False)


    def create_userprofile(self):
        t2 = self.create_user()
        return UserProfile.objects.create(user = t2)

    def test_user_profile_model(self):
        t1 = self.create_userprofile()
        self.assertTrue(instance(t1, UserProfile))
        self.assertEqual(t1.__unicode__(), t1.user)
