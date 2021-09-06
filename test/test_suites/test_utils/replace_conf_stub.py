from pathlib import Path
from typing import Optional
from overrides.overrides import overrides
from amirotest.tools.config.dependency_checker import DepTag
from amirotest.tools.replace_config_builder import ReplaceConfig


class ReplaceConfigStub(ReplaceConfig):

    @overrides
    def load(self, path: Path):
        pass

    @overrides
    def is_valid(self) -> bool:
        return True

    def get_module_names(self) -> list[str]:
        return ['Test Module']

    @overrides
    def get_flatten_config(self) -> dict[str, list]:
        return {
            'dep1': ['True', 'False'],
            'dep2': ['True', 'False'],
            'dep3': ['True', 'False'],
            'dep4': ['True', 'False'],
            'dep5': ['True', 'False'],
            'dep6': ['True', 'False'],
            'dep7': ['True', 'False'],
            'dep8': ['True', 'False'],
        }

    @overrides
    def get_dependencies(self) -> dict:
        return {
            'dep1':{
                DepTag.with_value.name: 'True',
                DepTag.requires.name: {
                    'dep2': 'True',
                }
            },
            'dep3': {
                DepTag.with_value.name: 'False',
                DepTag.requires.name: {
                    'dep4': 'False'
                }
            },
            'dep5': {
                DepTag.with_value.name: 'False',
                DepTag.requires_all.name: ['dep6', 'dep7', 'dep8'],
                DepTag.to_be.name: 'False'
            }

        }