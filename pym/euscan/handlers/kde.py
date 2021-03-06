from euscan.handlers import generic


def can_handle(cpv, url):
    if url.startswith('mirror://kde/'):
        return True
    return False


def clean_results(results):
    ret = []

    for path, version in results:
        if version == '5SUMS':
            continue
        ret.append((path, version))

    return ret


def scan(cpv, url):
    results = generic.scan(cpv, url)

    if url.startswith('mirror://kde/unstable/'):
        url = url.replace('mirror://kde/unstable/', 'mirror://kde/stable/')
        results += generic.scan(cpv, url)

    return clean_results(results)


def brute_force(cpv, url):
    results = generic.brute_force(cpv, url)

    if url.startswith('mirror://kde/unstable/'):
        url = url.replace('mirror://kde/unstable/', 'mirror://kde/stable/')
        results += generic.brute_force(cpv, url)

    return clean_results(results)
