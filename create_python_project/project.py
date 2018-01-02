"""
    create_python_project.project
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Main class for manipulating a project

    :copyright: Copyright 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""

from .git import RepositoryManager
from .utils import get_script, get_info, publish, \
    format_package_name, format_project_name, format_py_script_title


class ProjectManager(RepositoryManager):

    def get_scripts(self, *args, **kwargs):
        scripts = []
        self.apply_func(lambda blob: scripts.append(get_script(blob)), *args, **kwargs)
        return scripts

    def get_info(self, *args, **kwargs):
        info = []
        self.apply_func(lambda blob: info.append(get_info(blob)), *args, **kwargs)
        return info

    def publish(self, *args, **kwargs):
        self.apply_func(publish, *args, **kwargs)

    @property
    def setup_info(self):
        info = self.get_info(is_filtered='setup.py')
        return info[0].code.setup

    def set_project_name(self, name):
        assert not self.is_dirty(), \
            'You have uncommmitted modifications. ' \
            'Please commit or stash all modifications before setting new project\'s name'

        new_project_name, new_package_name = format_project_name(name), format_package_name(name)

        old_info = self.setup_info
        self.mv(old_info.packages[0].value, new_package_name)

        # Update python scripts headers title
        self.publish(is_filtered='{folder}*.py'.format(folder=new_package_name),
                     title=lambda blob: format_py_script_title(blob.path))

        # Rename imports in .py files
        self.publish(is_filtered='*.py', old_import=old_info.packages[0].value, new_import=new_package_name)

        # Replace textual
        self.publish(old_value=old_info.name.value, new_value=new_project_name)
        self.publish(old_value=old_info.packages[0].value, new_value=new_package_name)
        self.publish(old_value=old_info.packages[0].value.replace('_', '-'),
                     new_value=new_package_name.replace('_', '-'))

        # Commit modifications
        self.git.commit('-am', 'rename project to {name}'.format(name=new_project_name))
