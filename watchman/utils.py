# -*- coding: utf-8 -*-
try: # try for Django 1.7+ first.
    from django.utils.module_loading import import_string
except ImportError: # < Django 1.7
    try:
        from django.utils.module_loading import import_by_path as import_string
    except ImportError: # < Django 1.5.3 (including 1.4 LTS)
        import sys
        from django.utils import six
        from django.utils.importlib import import_module
        from django.core.exceptions import ImproperlyConfigured
        def import_string(dotted_path, error_prefix=''):
            try:
                module_path, class_name = dotted_path.rsplit('.', 1)
            except ValueError:
                raise ImproperlyConfigured("%s%s doesn't look like a module path" % (
                    error_prefix, dotted_path))
            try:
                module = import_module(module_path)
            except ImportError as e:
                msg = '%sError importing module %s: "%s"' % (
                    error_prefix, module_path, e)
                six.reraise(ImproperlyConfigured, ImproperlyConfigured(msg),
                            sys.exc_info()[2])
            try:
                attr = getattr(module, class_name)
            except AttributeError:
                raise ImproperlyConfigured('%sModule "%s" does not define a "%s" attribute/class' % (
                    error_prefix, module_path, class_name))
            return attr


def get_checkers(paths_to_checkers):
    for python_path in paths_to_checkers:
        yield import_string(python_path)
