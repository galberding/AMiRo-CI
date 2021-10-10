from typing import Any
import pandas as pd


class ConfMatrixBuilder:
    def build_dataframe_config(
        self, config: dict[str, list[Any]]
    ) -> pd.DataFrame:
        """Creates matrix where all parameters passed by the config are combined with each other.
        config: dict in form of: {"ParamerterName": ["list", "of", "Values"], ...}
        return  configuration matrix in form of a DataFrame where the columns hold the parameter names.
        """
        col_names = config.keys()

        aug_conf = self.augment_config(config)
        # return pd.DataFrame(aug_conf)
        return pd.DataFrame(aug_conf, columns=col_names, dtype="string")

    def augment_config(self, config: dict[str, list[Any]]) -> list[list]:
        """Combine all config values with each other
        """
        mat: list[list] = []
        for opt, args in config.items():
            mat = self._insert_in_config_mat(args, mat)
        return mat

    def _insert_in_config_mat(self, col: list[Any], mat: list[list[Any]]):
        """Combine all values in mat with all values in col.
        """
        if not mat:
            return self._populate_matrix(col)

        new_mat: list[list] = []
        for i in col:
            for row in mat:
                new_mat.append([*row, i])
        return new_mat

    def _populate_matrix(self, col: list[Any]):
        """Create matrix construct and fill with col values.
        """
        new_mat = []
        for i in col:
            new_mat.append([i])
        return new_mat

    def _get_conf_mat_size(self, config: dict[str,
                                              list[Any]]) -> tuple[int, int]:
        """Return row and column count.
        """
        col_count = len(config.items())
        row_count = 1
        for _, args in config.items():
            row_count *= len(args)
        return row_count, col_count
