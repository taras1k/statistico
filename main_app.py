import web


import helper 
from web.contrib.template import render_mako
from models import Url, Click

urls = (
"/h", "hello",
"/stat/(.*)", "statistic",
'/(.*)', 'redirect',
)
app = web.application(urls, globals())


render = render_mako(
        directories=['templates'],
        input_encoding='utf-8',
        output_encoding='utf-8',
        )


class redirect:
    def GET(self, path):
    	url_models = Url()
    	url_model = url_models.get_url_by_key('code', path)
    	if url_model:
            helper.save_click(web.ctx.env, path)
    	    web.redirect(url_model['url'])
        web.notfound
        
class statistic:
    def GET(self, path):
        return helper.get_click_info(path)

class hello:
    def GET(self):
    	params = web.input()
    	data = {}
    	if 'url' in params:
    		url = params.url
    		data['url'] = helper.short_it(url)
        return render.default(params = data)

if __name__ == "__main__":
    app.run()
