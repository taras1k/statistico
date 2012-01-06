import web
import helper 
from web.contrib.template import render_mako
from controlers import shortener, click_info

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
        url = shortener.get_url(path)
        if url:
            click_info.save_click(web.ctx.env, path)
            web.redirect(shortener.format_url(url['url']))
        web.notfound 

class statistic:
    def GET(self, path):
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
        params = web.input()
        data = {}
        if 'url' in params:
            url = params.url
            data['url'] = shortener.short_it(url)
        return render.main(params = data)

if __name__ == "__main__":
    app.run()
