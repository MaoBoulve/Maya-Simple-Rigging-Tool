"""
Freeform Rigging and Animation Tools
Copyright (C) 2020  Micah Zahm

Freeform Rigging and Animation Tools is free software: you can redistribute it
and/or modify it under the terms of the GNU General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Freeform Rigging and Animation Tools is distributed in the hope that it will
be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Freeform Rigging and Animation Tools.
If not, see <https://www.gnu.org/licenses/>.
"""


import inspect


class Singleton(type):
    """
    Singleton metaclass.  Enforces singleton behavior on any class that inherits it
    """
    _instances = {}

    def __call__(self, *args, **kwargs):
        if self.__name__ not in self._instances:
            self._instances[self.__name__] = super(Singleton, self).__call__(*args, **kwargs)
        return self._instances[self.__name__]


class Freeform_Registry(object, metaclass=Singleton):
    """
    Base Registry class for gathering components of the Freeform Tools.  On class import
    classes register their type into these registries for easy and consistent lookup no matter
    how the import was handled.
    """
    @property
    def type_list(self):
        return list(self.registry.values())

    @property
    def name_list(self):
        return list(self.registry.keys())

    def __init__(self):
        self.registry = {}
        self.hidden_registry = {}

    def _add_internal(self, a_name, a_type, internal_registry):
        if a_name not in internal_registry:
            internal_registry[a_name] = a_type

    def add(self, a_name, a_type):
        self._add_internal(a_name, a_type, self.registry)

    def add_hidden(self, a_name, a_type):
        self._add_internal(a_name, a_type, self.hidden_registry)

    def clear(self):
        self.registry.clear()

    def _get_internal(self, get_name, internal_registry, all_registries=False):
        return_item = None
        if not all_registries:
            return_item = internal_registry.get(get_name)
        else:
            registry_list = [x for x in Freeform_Registry._instances.values() if isinstance(x,Freeform_Registry)]
            for registry in registry_list:
                return_item = registry.get(get_name)
                if return_item:
                    break

        return return_item

    def get(self, get_obj, all_registries=False):
        if(inspect.isclass(get_obj)):
            get_obj = get_obj.__name__
        
        return self._get_internal(get_obj, self.registry, all_registries)

    def get_hidden(self, get_obj, all_registries=False):
        if(inspect.isclass(get_obj)):
            get_obj = get_obj.__name__

        return self._get_internal(get_obj, self.hidden_registry, all_registries)


class Network_Registry(Freeform_Registry):
    """
    Central registry for gathering all available network objects
    """
    def __init__(self):
        super(Network_Registry, self).__init__()


class Network_Meta(type):
    def __new__(cls, cls_name, bases, attr_dct):
        new_class = type.__new__(cls, cls_name, bases, attr_dct)
        if new_class._do_register:
            Network_Registry().add(cls_name, new_class)
        else:
            Network_Registry().add_hidden(cls_name, new_class)

        return new_class


class Property_Registry(Freeform_Registry):
    """
    Central registry for gathering all available property objects
    """
    def __init__(self):
        super(Property_Registry, self).__init__()


class Property_Meta(Network_Meta):
    def __new__(cls, cls_name, bases, attr_dct):
        new_class = type.__new__(cls, cls_name, bases, attr_dct)
        if new_class._do_register:
            Property_Registry().add(cls_name, new_class)
        else:
            Property_Registry().add_hidden(cls_name, new_class)

        return new_class
