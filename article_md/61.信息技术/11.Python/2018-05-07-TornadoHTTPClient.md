# Tornado HTTPClient

## 1、阻塞型客户端
	from tornado.httpclient import HTTPClient
	client = HTTPClient()
	response = client.fetch("http://127.0.0.1:80/login",method="GET")
	response = client.fetch("http://127.0.0.1:80/login?t=t",method="POST", body="user=a&pswd=w")
	print(response.body)

## 2、非阻塞型客户端
	from tornado.httpclient import AsyncHTTPClient()
    client = AsyncHTTPClient()
    data_send = urllib.urlencode({"data_test":"1"})
    response = client.fetch("http://127.0.0.1:80", method='POST', body=data_send, callback = data_resp)
        
    def data_resp(resp):
        print(resp.body)