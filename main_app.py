import web
import helper 
from web.contrib.template import render_mako
from controlers import Shortener, ClickInfo, Links

import qrcode
import cStringIO


urls = (
"/", "hello",
"/about", "about",
"/stat/(.*)", "statistic",
"/qrcode/(.*)", "generate_qrcode",
'/(.*)', 'redirect',
)

pages = ['about']

app = web.application(urls, globals())

server_name = 'http://0.0.0.0:8080/'

render = render_mako(
        directories=['templates'],
        input_encoding='utf-8',
        output_encoding='utf-8',
        )


class redirect:
    def GET(self, path):
        shortener = Shortener()
        click_info = ClickInfo()
        url = shortener.get_url(path)
        if url:
            click_info.save_click(web.ctx.env, path)
            web.redirect(shortener.format_url(url['url']))
        web.notfound 

class generate_qrcode:
    def GET(self, code):
        shortener = Shortener()
        url = shortener.get_url(code)
        if url:
            img = qrcode.make(shortener.format_url(server_name+url['code']))
            file = cStringIO.StringIO() 
            img.save(file, 'png')
            image_code = file.getvalue()
            file.close()
            return image_code
        return ''

class about:
    def GET(self):
        data = {}
        data['menu'] = helper.main_menu()        
        return render.about(params = data)


class statistic:
    def GET(self, path):
        click_info = ClickInfo()
        data = {}
        params = web.input()
        from_date = params.get('from_date', None)
        to_date = params.get('to_date', None)
        if from_date:
            from_date = helper.prepare_date(from_date)
        if to_date:
            to_date = helper.prepare_date(to_date)
        data['browsers'] = []
        data['os'] = []
        data['clicks'] = []
        clicks = click_info.get_click_info(path, f_date = from_date, t_date = to_date)
        data['count'] = clicks['count']
        if 'click_statistic' in clicks:
            if 'browser' in clicks['click_statistic']:
                helper.prpare_list(clicks['click_statistic']['browser'], data['browsers'])
            if 'os' in clicks['click_statistic']:
                helper.prpare_list(clicks['click_statistic']['os'], data['os'])
            if 'time' in clicks['click_statistic']:
                helper.prpare_list(clicks['click_statistic']['time'], data['clicks'])    
        return render.statistic(params = data)

class hello:
    def GET(self):
        shortener = Shortener()
        input_params = web.input()
        data = {}
        if 'url' in input_params:
            url = input_params.url
            links = Links(server_name)

            shorted_url = shortener.short_it(url)
            links.add_link('url', param =shorted_url)
            links.add_link('statistic', param =shorted_url)
            links.add_link('qrcode', param = shorted_url)
            for element in links.get_links():
                data[element['link']] = element['url']
        data['menu'] = helper.main_menu()
        return render.main(params = data)

if __name__ == "__main__":
    app.run()
