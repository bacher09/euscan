"""
djeuscan.helpers
"""

from distutils.version import StrictVersion, LooseVersion


def xint(i):
    """
    Tries to cast to int, fallbacks to 0
    """
    try:
        return int(i)
    except Exception:
        return 0


def select_related_last_versions(queryset):
    queryset = queryset.select_related(
        'last_version_gentoo',
        'last_version_overlay',
        'last_version_upstream'
    )


def version_key(version):
    version = version.version
    try:
        return StrictVersion(version)
    # in case of abnormal version number, fall back to LooseVersion
    except ValueError:
        return LooseVersion(version)


def packages_from_names(data):
    """
    Returns a list of Package objects from a string of names
    """

    from djeuscan.models import Package

    packages = []
    data = data.replace("\r", "")

    for pkg in data.split('\n'):
        if '/' in pkg:
            cat, pkg = pkg.split('/')
            packages.extend(Package.objects.filter(category=cat, name=pkg))
        else:
            packages.extend(Package.objects.filter(name=pkg))
    return packages


def rename_fields(vqs, fields):
    ret = []
    for n in vqs:
        for tr in fields:
            if tr[0] in n:
                n[tr[1]] = n[tr[0]]
                del n[tr[0]]
        ret.append(n)
    return ret


class catch_and_return(object):
    def __init__(self, err, response):
        self.err = err
        self.response = response

    def __call__(self, fn):
        def wrapper(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except self.err:
                return self.response
        return wrapper
