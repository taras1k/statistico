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
            web.redirect(helper.format_url(url_model['url']))
        web.notfound 

class statistic:
    def GET(self, path):
        data = {}
        data['browsers'] = []
        data['os'] = []
        click_info = helper.get_click_info(path)
        if 'env' in click_info:
            if 'browser' in click_info['env']:
                for key,value in click_info['env']['browser'].items():
                    new_browser = [str(key), value]
                    data['browsers'].append(new_browser)
            if 'os' in click_info['env']:
                for key,value in click_info['env']['os'].items():
                    new_os = [str(key), value]
                    data['os'].append(new_os)
        return render.statistic(params = data)

class hello:
    def GET(self):
        params = web.input()
        data = {}
        if 'url' in params:
            url = params.url
            data['url'] = helper.short_it(url)
        return render.main(params = data)

if __name__ == "__main__":
    app.run()
