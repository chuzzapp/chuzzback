from jinja2 import Environment, FileSystemLoader
import os


def render_template(path, context={}):
    path, filename = os.path.split('plugin/templates/' + path)
    env = Environment(loader=FileSystemLoader(path))
    template = env.get_template(filename)
    return template.render(context)
