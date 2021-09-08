from pathlib import Path
from typing import Optional
from overrides.overrides import overrides
from amirotest.tools.config.dependency_checker import ConfTag
from amirotest.tools.replace_config_builder import YamlReplConf


class ReplacementConfWithAppsStub(YamlReplConf):
    def __init__(self, list_apps=True) -> None:
        self.list_apps = list_apps
        super().__init__(Path())

    @overrides
    def get_config(self, conf_path: Path) -> Optional[dict]:
        return {
            ConfTag.Modules.name: ['TestModule'],
            ConfTag.Apps.name: ['TestApp1', 'TestApp2'] if self.list_apps else [],
            ConfTag.Options.name: {
                'OptionGroup1': {
                    'opt1': ['true', 'false'],
                    'opt2': ['true', 'false']
                },
                'OptionGroup2': {
                    'opt3': ['true', 'false'],
                    'opt4': ['true', 'false']
                }
            }
        }


class ReplaceConfigWithDependenciesStub(YamlReplConf):

    @overrides
    def get_config(self, conf_path: Path) -> Optional[dict]:
        return {
            ConfTag.Modules.name: ['TestModule'],
            ConfTag.Apps.name: ['TestApp'],
            ConfTag.Options.name: {
                'OptionGroup': {
                    'dep1': ['True', 'False'],
                    'dep2': ['True', 'False'],
                    'dep3': ['True', 'False'],
                    'dep4': ['True', 'False'],
                    'dep5': ['True', 'False'],
                    'dep6': ['True', 'False'],
                    'dep7': ['True', 'False'],
                    'dep8': ['True', 'False'],
                },
            },
            ConfTag.Dependencies.name: {
                'dep1':{
                    ConfTag.with_value.name: 'True',
                    ConfTag.requires.name: {
                        'dep2': 'True',
                    }
                },
                'dep3': {
                    ConfTag.with_value.name: 'False',
                    ConfTag.requires.name: {
                        'dep4': 'False'
                    }
                },
                'dep5': {
                    ConfTag.with_value.name: 'False',
                    ConfTag.requires_all.name: ['dep6', 'dep7', 'dep8'],
                    ConfTag.to_be.name: 'False'
                }

            }
        }
