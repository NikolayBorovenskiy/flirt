from __future__ import absolute_import

import json as _json
from rest_framework.utils.encoders import JSONEncoder


def dumps(obj, **kwargs):
    kwargs.setdefault('cls', JSONEncoder)
    return _json.dumps(obj, **kwargs)


loads = _json.loads
