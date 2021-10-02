from enum import Enum, auto
from amiroci.model.aos_module import AosModule
from amiroci.tools.config.config_tags import ConfTag


class DependencyChecker:
    """!Accepts a dependency configuration which is used to check
    if modules fulfill the dependencies.
    @note Dependencies are usually provided by the replacement config.
    """
    def __init__(self, dependencies):
        self.dep = self.resolve_requires_all_tag(dependencies)

    def resolve_requires_all_tag(self, conf):
        """!Convert the `requires_all` tag to `requires`.
        This simply removes the syntactic sugar.
        For example both expressions below are equivalent but only
        the latte one can be processed.
        ~~~
        0 Dependency:
        1    Dep1:
        2        with_value: True
        3        requires_all: [Dep2, Dep3]
        4        to_be: True

        # is equivalent to:

        0 Dependency:
        1    Dep1:
        2        with_value: True
        3        requires:
        4            Dep2: True
        5            Dep3: True
        ~~~
        """
        resolved_conf = {}
        for lead_opt, dep, in conf.items():
            if ConfTag.requires_all.name in dep:
             resolved_conf[lead_opt] = {
                 ConfTag.with_value.name: dep[ConfTag.with_value.name],
                 ConfTag.requires.name: {}
             }
             for opt in dep[ConfTag.requires_all.name]:
                 resolved_conf[lead_opt][ConfTag.requires.name][opt] = dep[ConfTag.to_be.name]
            else:
                resolved_conf[lead_opt] = dep
        return resolved_conf

    def is_valid(self, module: AosModule) -> bool:
        """!A module that fulfills all or is not affected by dependencies
        is considered valid.
        @param module
        @return whether a module is valid or not
        """
        if not self.has_dependencies():
            return True
        return self.check_all_deps(module)

    def has_dependencies(self) -> bool:
        """!Check if dependencies are available.
        """
        return bool(self.dep)

    def check_all_deps(self, module) -> bool:
        """!Check if all dependencies are fulfilled.
        The module is queried for all dependencies.
        If the lead condition of the dependency fits all
        other required dependencies are checked.
        @param module
        @return bool
        """
        for lead_opt, dep in self.dep.items():
            if self.opt_in(lead_opt, dep[ConfTag.with_value.name], module):
                for dep_opt, value, in dep[ConfTag.requires.name].items():
                    if not self.opt_in(dep_opt, value, module):
                       return False
        return True

    def opt_in(self,opt_name, value, module: AosModule):
        """!Helper to quickly check if module has an option with
        the given value.
        @warning `find_option_by_name()` can raise an exception if
        the option is not found!
        """
        return module.find_option_by_name(opt_name).value == value
