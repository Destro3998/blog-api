import unittest
import json
import tempfile
import os
import sys

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from app import app

class BlogAPITestCase(unittest.TestCase):
    def setUp(self):
        """Set up test client and create a temporary database"""
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.app = app.test_client()
        
        # Initialize database
        with app.app_context():
            from app import init_db
            init_db()

    def tearDown(self):
        """Clean up after tests"""
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def test_home_endpoint(self):
        """Test the home endpoint"""
        response = self.app.get('/')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', data)
        self.assertIn('status', data)
        self.assertEqual(data['status'], 'healthy')

    def test_health_endpoint(self):
        """Test the health endpoint"""
        response = self.app.get('/health')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('status', data)
        self.assertIn('database', data)
        self.assertEqual(data['status'], 'healthy')

    def test_create_post(self):
        """Test creating a new post"""
        post_data = {
            'title': 'Test Post',
            'content': 'This is a test post content',
            'author': 'Test Author'
        }
        
        response = self.app.post('/api/posts',
                               data=json.dumps(post_data),
                               content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 201)
        self.assertIn('message', data)
        self.assertIn('id', data)

    def test_get_posts(self):
        """Test getting all posts"""
        # First create a post
        post_data = {
            'title': 'Test Post',
            'content': 'This is a test post content',
            'author': 'Test Author'
        }
        self.app.post('/api/posts',
                     data=json.dumps(post_data),
                     content_type='application/json')
        
        # Then get all posts
        response = self.app.get('/api/posts')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('posts', data)
        self.assertIn('count', data)
        self.assertGreater(data['count'], 0)

    def test_get_single_post(self):
        """Test getting a single post"""
        # First create a post
        post_data = {
            'title': 'Test Post',
            'content': 'This is a test post content',
            'author': 'Test Author'
        }
        create_response = self.app.post('/api/posts',
                                      data=json.dumps(post_data),
                                      content_type='application/json')
        create_data = json.loads(create_response.data)
        post_id = create_data['id']
        
        # Then get the specific post
        response = self.app.get(f'/api/posts/{post_id}')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['title'], 'Test Post')
        self.assertEqual(data['content'], 'This is a test post content')
        self.assertEqual(data['author'], 'Test Author')

    def test_create_user(self):
        """Test creating a new user"""
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com'
        }
        
        response = self.app.post('/api/users',
                               data=json.dumps(user_data),
                               content_type='application/json')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 201)
        self.assertIn('message', data)
        self.assertIn('id', data)

    def test_get_users(self):
        """Test getting all users"""
        # First create a user
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com'
        }
        self.app.post('/api/users',
                     data=json.dumps(user_data),
                     content_type='application/json')
        
        # Then get all users
        response = self.app.get('/api/users')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('users', data)
        self.assertIn('count', data)
        self.assertGreater(data['count'], 0)

    def test_invalid_post_data(self):
        """Test creating a post with invalid data"""
        post_data = {
            'title': 'Test Post'
            # Missing content and author
        }
        
        response = self.app.post('/api/posts',
                               data=json.dumps(post_data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 400)

    def test_invalid_user_data(self):
        """Test creating a user with invalid data"""
        user_data = {
            'username': 'testuser'
            # Missing email
        }
        
        response = self.app.post('/api/users',
                               data=json.dumps(user_data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 400)

    def test_nonexistent_post(self):
        """Test getting a post that doesn't exist"""
        response = self.app.get('/api/posts/999')
        
        self.assertEqual(response.status_code, 404)

    def test_404_error(self):
        """Test 404 error handling"""
        response = self.app.get('/nonexistent-endpoint')
        
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main() 