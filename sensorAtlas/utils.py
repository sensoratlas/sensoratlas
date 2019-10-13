from collections import defaultdict


def dict_from_qs(qs):
    """
    Slightly introverted parser for lists of comma seperated nested fields
    i.e. "period.di,period/fhr" => {"period": {"di": {}, "fhr": {}}}
    """
    entries = qs.split(',') if qs.strip() else []
    entries = [entry.strip() for entry in entries]

    def _dict_from_qs(line, d):
        if '/' in line:
            key, value = line.split('/', 1)
            d.setdefault(key, {})
            return _dict_from_qs(value, d[key])
        else:
            d[line] = {}

    def _default():
        return defaultdict(_default)

    d = defaultdict(_default)
    for line in entries:
        _dict_from_qs(line, d)
    return d


def qs_from_dict(qsdict, prefix=""):
    """
    Same as dict_from_qs, but in reverse
    i.e. {"period": {"di": {}, "fhr": {}}} => "period/di,period/fhr"
    """
    prefix = prefix + '/' if prefix else ""

    def descend(qsd):
        for key, val in sorted(qsd.items()):
            if val:
                yield qs_from_dict(val, prefix + key)
            else:
                yield prefix + key
    return ",".join(descend(qsdict))


