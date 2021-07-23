import json
import unittest

import requests

count_blogs = 0


def setUpModule():
    r = requests.get(f"http://127.0.0.1:8000/blog")
    global count_blogs
    count_blogs = len(r.json())


def tearDownModule():
    r = requests.get(f"http://127.0.0.1:8000/blog")
    global count_blogs
    assert count_blogs == len(r.json()), f" count blogs changed '"


class TestBlogs(unittest.TestCase):
    blog = {}

    @classmethod
    def setUpClass(cls):
        r = requests.post(
            'http://127.0.0.1:8000/blog/?user_id=1',
            data=json.dumps({"title": "yh5", "body": "fgh5"})
        )
        cls.blog = r.json()

    def test_case01_get(self):
        r = requests.get(f"http://127.0.0.1:8000/blog/{self.blog['id']}")
        self.assertEqual(r.status_code, 200)
        blog = r.json()
        self.assertEqual(blog['title'], 'yh5')
        self.assertEqual(blog['body'], 'fgh5')

    def test_case02_update(self):
        r = requests.put(
            f"http://127.0.0.1:8000/blog/{self.blog['id']}",
            data=json.dumps({"title": "yh6", "body": "fgh6"})
        )
        self.assertEqual(r.status_code, 202)

    def test_case03_get(self):
        r = requests.get(f"http://127.0.0.1:8000/blog/{self.blog['id']}")
        self.assertEqual(r.status_code, 200)
        blog = r.json()
        self.assertEqual(blog['title'], 'yh6')
        self.assertEqual(blog['body'], 'fgh6')

    @classmethod
    def tearDownClass(cls):
        requests.delete(f"http://127.0.0.1:8000/blog/{cls.blog['id']}")
