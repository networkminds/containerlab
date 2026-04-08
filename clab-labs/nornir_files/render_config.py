from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_jinja2.plugins.tasks import template_file
from nornir_scrapli.tasks import send_command, send_configs, send_config
from rich import inspect

def render_config(task):
    template = 'bgp_config.j2'
    result = task.run(task=template_file, template=template, path='config_templates/', **task.host)
    rendered_config = result[0].result
    task.host['rendered_config'] = rendered_config

def scrapli_send_config(task):
    host = task.host
    config = host['rendered_config']

    task.run(task=send_config, config=config)


if __name__ == "__main__":
    nr = InitNornir(config_file='config.yaml')

    result = nr.run(task=render_config)
    result1 = nr.run(task=scrapli_send_config)


    print_result(result1)
