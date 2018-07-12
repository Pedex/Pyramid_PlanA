from pyramid.config import Configurator
import deform
import cherrypy
from pkg_resources import resource_filename
from pyramid.i18n import get_localizer
from pyramid.threadlocal import get_current_request


def pregen(request, elements, kw):
    kw.setdefault('amountWeeks', '2')
    return elements, kw

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('multiweek', '/multiweek/{amountWeeks}', pregenerator=pregen)
    config.add_route('multiweekPost', '/multiweekPost')
    config.add_route('multiweekForm', '/multiweekForm')
    config.add_route('multiweekDelete', '/multiweekDelete')
    config.add_static_view('static2', 'deform:static')
    config.scan('.views')
    config.add_translation_dirs(
        'colander:locale',
        'deform:locale',
    )
    def translator(term):
        return get_localizer(get_current_request()).translate(term)

    deform_template_dir = resource_filename('deform', 'templates/')
    zpt_renderer = deform.ZPTRendererFactory(
        [deform_template_dir],
        translator=translator,
    )
    deform.Form.set_default_renderer(zpt_renderer)
    return config.make_wsgi_app()

