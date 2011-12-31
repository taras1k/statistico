from attest import Tests
import helper
generate = Tests()

@generate.test
def gen():
	for i in range(5,10):
		str = helper._id_generator(i)
		assert i == len(str)

if __name__ == '__main__':
	generate.run()


