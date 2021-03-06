import inspect
import sys

import config
import uri
from linkr import app


@app.context_processor
def get_config():
    """
    Expose the server-side configuration options as a templating method.
    """
    return dict(config=lambda: config.options.server(''))


@app.context_processor
def get_uri_path():
    """
    Templating utility to easily retrieve the URI path given the URI module and class name of the
    desired URI. This saves the effort of explicitly retrieving the URI path when building
    the template environment, instead allowing for on-the-fly template-side URI retrievals like:

        {{ uri('user', 'UserCreateURI') }}
        {{ uri('user', 'UserCreateURI', param='value') }}
        {{ full_uri('user', 'UserCreateURI', param='value') }}

    :raises ImportError: If one or both of the URI module or class name is invalid
    """
    def uri_func(uri_module, uri_name, *args, **kwargs):
        uri_module = __import__('uri.' + uri_module, globals(), locals(), [uri_name], -1)
        uri_class = getattr(uri_module, uri_name)
        return uri_class.uri(*args, **kwargs)

    def full_uri_func(uri_module, uri_name, *args, **kwargs):
        uri_module = __import__('uri.' + uri_module, globals(), locals(), [uri_name], -1)
        uri_class = getattr(uri_module, uri_name)
        return uri_class.full_uri(*args, **kwargs)

    return dict(uri=uri_func, full_uri=full_uri_func)


@app.context_processor
def get_all_uris():
    """
    Templating utility to retrieve all available URIs, mapping modules to URI classes.
    Used ultimately to store all URI paths in the template for easy retrieval by frontend logic.

        {{ all_uris() }}
    """
    return dict(all_uris=lambda: {
        uri_module: filter(
            lambda module_name: module_name.endswith('URI') and len(module_name) > 3,
            map(
                lambda module_pair: module_pair[0],
                inspect.getmembers(sys.modules['uri.' + uri_module]),
            ),
        )
        for uri_module in filter(
            lambda mod: not mod.startswith('__'),
            dir(uri),
        )
    })
