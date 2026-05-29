from datetime import datetime, timezone

from django.core.paginator import Page
from django.test import TestCase
from django.urls import reverse

from .models import Post


class PostModelTest(TestCase):
    def test_create_post_with_all_fields(self):
        post = Post.objects.create(
            title='Sismo en prueba',
            location='Prueba',
            magnitude=4.5,
            depth_km=120.0,
            latitude=-33.45,
            longitude=-70.67,
            utc_time=datetime(2024, 7, 4, 10, 30, 0, tzinfo=timezone.utc),
        )
        self.assertEqual(str(post), 'Sismo en prueba')
        self.assertEqual(post.magnitude, 4.5)
        self.assertEqual(post.depth_km, 120.0)

    def test_default_ordering(self):
        Post.objects.create(title='Segundo', magnitude=3.0)
        Post.objects.create(title='Primero', magnitude=5.0)
        posts = Post.objects.all()
        self.assertEqual(posts[0].title, 'Primero')

    def test_nullable_fields(self):
        post = Post.objects.create(title='Solo titulo')
        self.assertIsNone(post.magnitude)
        self.assertIsNone(post.depth_km)
        self.assertIsNone(post.latitude)
        self.assertIsNone(post.longitude)
        self.assertIsNone(post.utc_time)


class PostViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(15):
            Post.objects.create(
                title=f'Sismo {i}',
                location=f'Lugar {i}',
                magnitude=3.0 + i * 0.1,
                depth_km=100.0 + i,
            )

    def test_view_status_code(self):
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('post_list'))
        self.assertTemplateUsed(response, 'blog/index.html')

    def test_pagination_first_page(self):
        response = self.client.get(reverse('post_list'))
        self.assertTrue('posts' in response.context)
        self.assertEqual(len(response.context['posts']), 10)

    def test_pagination_second_page(self):
        response = self.client.get(reverse('post_list'), {'page': 2})
        self.assertEqual(len(response.context['posts']), 5)

    def test_context_contains_last_event(self):
        response = self.client.get(reverse('post_list'))
        self.assertIn('last_event', response.context)
        self.assertIsNotNone(response.context['last_event'])
        self.assertEqual(response.context['last_event']['place'], 'Lugar 14')

    def test_context_contains_depth_series_json(self):
        response = self.client.get(reverse('post_list'))
        self.assertIn('depth_series_json', response.context)
        self.assertTrue(response.context['depth_series_json'].startswith('['))
