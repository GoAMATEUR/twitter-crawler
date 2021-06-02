'''
    request x_gust_token
'''
from ..http_requests.web_client import WebClient, init_headers
from ..http_requests.request_list import RequestList
from ..http_requests.http_method import HttpMethod
import json
from typing import Optional
from retrying import retry

retries = 5
timeout = 10
url = 'https://api.twitter.com/1.1/guest/activate.json'
auth_token = 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81' \
              'IUq16cHjhLTvJu4FA33AGWWjCpTnA'
headers = {'Authorization': auth_token}

class AuthTokenProvider:
    def __init__(self, web_client:Optional[WebClient] = None):
        if web_client:
            self.web_client = web_client
        else:
            self.web_client = WebClient()

    @staticmethod
    def request_list_builder():
        return RequestList(url, HttpMethod.POST, timeout, headers=headers, params=dict())
    
    def get_response_body(self):
        token_response = self.web_client.run_request(self.request_list_builder())
        if token_response.is_success():
            return token_response.text
        else:
            raise Exception('Error during request for token')
    
    @retry(stop_max_attempt_number=8)
    def get_new_token(self):
        try:
            token_html = self.get_response_body()
            response_json = json.loads(token_html)
            return response_json['guest_token']
        except json.JSONDecodeError:
            raise Exception('Error during request for token')

class AuthTokenProviderCreator:
    def create(self, web_client:WebClient):
        return AuthTokenProvider(web_client)
