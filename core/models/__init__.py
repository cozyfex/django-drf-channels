import importlib
import inspect
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

for filename in os.listdir(current_dir):
    if filename.endswith('.py') and filename != '__init__.py':
        module_name = filename[:-3]
        module = importlib.import_module(f'.{module_name}', package=__name__)

        for name, obj in inspect.getmembers(module, inspect.isclass):
            if obj.__module__ == module.__name__:
                globals()[name] = obj
