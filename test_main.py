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
	url = helper.short_it('ya.ru')
	r = requests.get(server_url+url)
	assert r.status_code == 200		


@load.test
def chek():
	server_url = 'http://0.0.0.0:8080/'
	url = helper.short_it('ya.ru')
	for i in range(1000):
		r = requests.get(server_url+url)
		assert r.status_code == 200			

if __name__ == '__main__':
	generate.run()
	code.run()
	load.run()


