import subprocess

from django.template import Library

register = Library()

DEFAULT_VERSION = 'Unknown'
cache = {'version': DEFAULT_VERSION}


@register.simple_tag(name='current_application_version')
def get_current_application_version():
    if cache['version'] == DEFAULT_VERSION:
        cache['version'] = get_git_revision_short_hash()
    return cache['version']


def get_git_revision_short_hash():
    try:
        last_hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'])
        return last_hash.strip().decode()
    except:
        return DEFAULT_VERSION
