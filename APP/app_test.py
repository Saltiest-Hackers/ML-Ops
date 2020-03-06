import unittest
import requests
import json


class AppTests(unittest.TestCase):
    """Making sure end-points work as expected"""

    def topusers(self):
        """Making sure end-point returns 100 items"""
        result=requests.get('https://hn-saltiness.herokuapp.com/topusers')
        #Conver resulting string into a list of dictionaries
        final=json.loads(result.text) 
        self.asserEqual(len(final), 100)

    def topusers_json_type():
        """Making sure the format of the output is correct: list of dictionaries"""
        result=requests.get('https://hn-saltiness.herokuapp.com/topusers')
        #Conver resulting string into a list of dictionaries
        final=json.loads(result.text) 
        self.assertEqual(type(final), list)
        self.assertEqual(type(final[0]), dict) 

    def topcomments(self):
        """Making sure end-point returns 100 items"""
        result=requests.get('https://hn-saltiness.herokuapp.com/topcomments')
        #Conver resulting string into a list of dictionaries
        final=json.loads(result.text) 
        self.asserEqual(len(final), 100)

    def topcomments_type():
        """Making sure the format of the output is correct: list of dictionaries"""
        result=requests.get('https://hn-saltiness.herokuapp.com/topcomments')
        #Conver resulting string into a list of dictionaries
        final=json.loads(result.text) 
        self.assertEqual(type(final), list)
        self.assertEqual(type(final[0]), dict) 

if __name__ == '__main__':
    unittest.main()