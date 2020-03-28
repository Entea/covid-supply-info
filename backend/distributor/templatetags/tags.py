import subprocess

from django.template import Library

register = Library()

cache = {'version': None}


@register.simple_tag(name='current_application_version')
def get_current_application_version():
    if not cache['version']:
        cache['version'] = get_git_revision_short_hash()
    return cache['version']


def get_git_revision_short_hash():
    last_hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'])
    return last_hash.strip().decode() if last_hash else None
