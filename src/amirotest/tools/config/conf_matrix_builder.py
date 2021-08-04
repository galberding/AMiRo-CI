from typing import Any
import pandas as pd

class ConfMatrixBuilder:
    def build_dataframe_config(self, config: dict[str, list[Any]]) -> pd.DataFrame:
        col_names = config.keys()

        aug_conf = self.augment_config(config)
        # return pd.DataFrame(aug_conf)
        return pd.DataFrame(aug_conf, columns=col_names)

    def augment_config(self, config: dict[str, list[Any]]) -> list[list]:
        row, _ = self._get_conf_mat_size(config)
        tmp_conf = {}
        mat: list[tuple] = []
        for opt, args in config.items():
            # print(args)
            mat = self._append_col(args, mat)
        return mat

    def _append_col(self, col: list[Any], mat: list[tuple[Any]]):
        new_mat: list[list] = []
        if not mat:
            for i in col:
                print(i)
                new_mat.append([i])
            # print("New mat:", new_mat)
            return new_mat
        for i in col:
            for row in mat:
                # print(type(row))
                new_mat.append([i, *row])
        return new_mat

    def _get_conf_mat_size(self, config: dict[str, list[Any]]) -> tuple[int, int]:
        col_count = len(config.items())
        row_count = 1
        for _, args in config.items():
            row_count *= len(args)
        return row_count, col_count
