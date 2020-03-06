from psycopg2 import connect
from requests import get
import json
import unittest


def request_saltiness(route, route_id=False):
    BASE_URL = 'https://hn-saltiness.herokuapp.com/'+route
    FINAL_URL = BASE_URL if not route_id else BASE_URL+'/'+route_id
    print(FINAL_URL)
    request = get(FINAL_URL)
    return json.loads(request.text)

class AppTests(unittest.TestCase):

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

if __name__ == "__main__":
    unittest.main()
    # request_saltiness(route='user', username='Data_Junkie')