import json
import unittest
from psycopg2 import connect
from requests import get


def request_saltiness(route, route_id=False):
    '''
    Requests 'hn-saltiness' endpoints given 'route' and 'route_id' parameters
    Returns resulting data in json format
    '''
    BASE_URL = 'https://hn-saltiness.herokuapp.com/'+route
    FINAL_URL = BASE_URL if not route_id else BASE_URL+'/'+route_id
    request = get(FINAL_URL)
    return json.loads(request.text)

class AppTests(unittest.TestCase):

    def test_users(self):
        '''
        Testing /topusers route
        '''
        results = request_saltiness('topusers')
        
        self.assertEqual(len(results), 100)
        self.assertEqual(type(results), list)
        self.assertEqual(type(results[0]), dict) 
        return

    def test_comments(self):
        '''
        Testing /topcomments route
        '''
        results = request_saltiness('topcomments')

        self.assertEqual(len(results), 100)
        self.assertEqual(type(results), list)
        self.assertEqual(type(results[0]), dict) 
        return

    def test_username(self):
        '''
        Testing /user/<username> route
        '''
        username = 'Data_Junkie'
        results = request_saltiness('user', username)

        self.assertEqual(len(results), 51)
        self.assertEqual(type(results[0]), dict)
        self.assertEqual(results[0]['author'], username)
        return

    def test_comment(self):
        '''
        Testing /comment/<comment_id> route
        '''
        comment_id = '21731901'
        results = request_saltiness('comment', comment_id)

        self.assertEqual(len(results), 6)
        self.assertEqual(type(results), dict)
        self.assertEqual(results['id'], int(comment_id))
        self.assertEqual(type(results['id']), int)


if __name__ == '__main__':
    unittest.main()