from attest import Tests
import helper
import requests

generate = Tests()
code = Tests()
load = Tests()


@generate.test
def gen():
    for i in range(5,10):
        str = helper._id_generator(i)
        assert i == len(str)


@code.test
def chek():
    server_url = 'http://0.0.0.0:8080/'
    url = helper.short_it('nic.to')
    print url
    r = requests.get(server_url+url, allow_redirects=False)
    assert r.status_code == 301     


@load.test
def chek():
    server_url = 'http://0.0.0.0:8080/'
    url = helper.short_it('http://www.google.com.ua/')
    for i in range(1000):
        r = requests.get(server_url+url, allow_redirects=False)
        assert r.status_code == 301         

if __name__ == '__main__':
    #generate.run()
    code.run()
    load.run()