"""
    create_python_project.project
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Main class for manipulating a project

    :copyright: Copyright 2017 by Nicolas Maurice, see AUTHORS.rst for more details.
    :license: BSD, see :ref:`license` for more details.
"""

from .git import RepositoryManager
from .utils import get_info, publish, \
    format_package_name, format_project_name, format_py_script_title


def get_config():
    return


class ProjectManager(RepositoryManager):

    def get_info(self, is_filtered):
        info = []
        self.apply_func(lambda blob: info.append(get_info(blob)), is_filtered=is_filtered)

    def publish(self, *args, **kwargs):
        self.apply_func(publish, *args, **kwargs)

    @property
    def setup_info(self):
        info = self.get_info('setup.py')
        return info[0].code.setup

    def set_project_name(self, name):
        assert not self.is_dirty(), \
            'You have uncommmitted modifications. ' \
            'Please commit or stash all modifications before setting new project\'s name'

        new_project_name, new_package_name = format_project_name(name), format_package_name(name)

        old_info = self.setup_info
        self.mv(old_info.package[0].text, new_package_name)

        # Update python scripts headers title
        self.publish(is_filtered='{folder}*.py'.format(folder=new_package_name),
                     new_title=format_py_script_title)

        # Update scripts
        self.publish(old_project_name=old_info.name.text, new_project_name=new_project_name,
                     old_package_name=old_info.package[0].text, new_package_name=new_package_name)

        self.git.commit('-am', 'rename project to {name}'.format(name=new_project_name))
