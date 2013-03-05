# -*- coding:utf-8 -*-
import json
from base64 import b64encode
from urllib2 import urlopen, Request
import requests
from contextlib import closing

from django.http import HttpResponse, HttpResponseRedirect


APP_ID = r"dj0zaiZpPTd4bGlNdFN0UGFPTyZkPVlXazlaV3QzWjFsdE56QW1jR285TUEtLSZzPWNvbnN1bWVyc2VjcmV0Jng9YTc-"
SECRET = r"754acc20690c6f6dc45d03261af20704521f825c"
REDIRECT_URI = r"http://localhost:7001/authorization"


def welcome(request, *args, **kwargs):
    """Authorization Endpoint."""
    url = ("https://auth.login.yahoo.co.jp/yconnect/v1/authorization?"
           "response_type=code&"
           "client_id=%s&"
           "state=foo&"
           "display=page&"
           "prompt=login&"
           "scope=openid+email&"
           "nonce=foo&"
           "redirect_uri=%s") % (APP_ID, REDIRECT_URI)
    return HttpResponseRedirect(url)


def authorization(request, *args, **kwargs):
    """When passed Token Endpoint, request UserInfo API."""
    ###########################
    # step1: Token Endpoint
    ###########################
    url = r"https://auth.login.yahoo.co.jp/yconnect/v1/token?"
    data = {
        "grant_type": "authorization_code",        
        "code": request.GET["code"],
        "redirect_uri": REDIRECT_URI,
    }
    basic_token = b64encode("%s:%s" % (APP_ID, SECRET))
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "Authorization": "Basic " + basic_token,
    }
    response = requests.post(url, data=data, headers=headers)
    if response.status_code != 200:
        return HttpResponse(response.text)

    ###########################
    # step2: UserInfo API
    ###########################
    dct = json.loads(response.text)
    url = "https://userinfo.yahooapis.jp/yconnect/v1/attribute?schema=openid"
    response = requests.get(userinfo, headers={
        "Authorization": "Bearer %s" % dct["access_token"]
    })
    return HttpResponse(response.text)
