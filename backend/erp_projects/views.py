(venv) abcd@pop-os:~/projects/erp-system/backend$ python manage.py runserver
Watching for file changes with StatReloader
Performing system checks...

Exception in thread django-main-thread:
Traceback (most recent call last):
  File "/home/abcd/projects/erp-system/venv/lib/python3.10/site-packages/django/core/checks/urls.py", line 136, in check_custom_error_handlers
    handler = resolver.resolve_error_handler(status_code)
  File "/home/abcd/projects/erp-system/venv/lib/python3.10/site-packages/django/urls/resolvers.py", line 732, in resolve_error_handler
    callback = getattr(self.urlconf_module, "handler%s" % view_type, None)
  File "/home/abcd/projects/erp-system/venv/lib/python3.10/site-packages/django/utils/functional.py", line 47, in __get__
    res = instance.__dict__[self.name] = self.func(instance)
  File "/home/abcd/projects/erp-system/venv/lib/python3.10/site-packages/django/urls/resolvers.py", line 711, in urlconf_module
    return import_module(self.urlconf_name)
  File "/usr/lib/python3.10/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
  File "<frozen importlib._bootstrap>", line 1050, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1027, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1006, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 688, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 883, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/home/abcd/projects/erp-system/backend/backend/urls.py", line 6, in <module>
    from erp_projects.views import (
ImportError: cannot import name 'create_task' from 'erp_projects.views' (/home/abcd/projects/erp-system/backend/erp_projects/views.py)

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/usr/lib/python3.10/threading.py", line 1016, in _bootstrap_inner
    self.run()
  File "/usr/lib/python3.10/threading.py", line 953, in run
    self._target(*self._args, **self._kwargs)
  File "/home/abcd/projects/erp-system/venv/lib/python3.10/site-packages/django/utils/autoreload.py", line 64, in wrapper
    fn(*args, **kwargs)
  File "/home/abcd/projects/erp-system/venv/lib/python3.10/site-packages/django/core/management/commands/runserver.py", line 134, in inner_run
    self.check(**check_kwargs)
  File "/home/abcd/projects/erp-system/venv/lib/python3.10/site-packages/django/core/management/base.py", line 496, in check
    all_issues = checks.run_checks(
  File "/home/abcd/projects/erp-system/venv/lib/python3.10/site-packages/django/core/checks/registry.py", line 89, in run_checks
    new_errors = check(app_configs=app_configs, databases=databases)
  File "/home/abcd/projects/erp-system/venv/lib/python3.10/site-packages/django/core/checks/urls.py", line 138, in check_custom_error_handlers
    path = getattr(resolver.urlconf_module, "handler%s" % status_code)
  File "/home/abcd/projects/erp-system/venv/lib/python3.10/site-packages/django/utils/functional.py", line 47, in __get__
    res = instance.__dict__[self.name] = self.func(instance)
  File "/home/abcd/projects/erp-system/venv/lib/python3.10/site-packages/django/urls/resolvers.py", line 711, in urlconf_module
    return import_module(self.urlconf_name)
  File "/usr/lib/python3.10/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
  File "<frozen importlib._bootstrap>", line 1050, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1027, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1006, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 688, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 883, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/home/abcd/projects/erp-system/backend/backend/urls.py", line 6, in <module>
    from erp_projects.views import (
ImportError: cannot import name 'create_task' from 'erp_projects.views' (/home/abcd/projects/erp-system/backend/erp_projects/views.py)
