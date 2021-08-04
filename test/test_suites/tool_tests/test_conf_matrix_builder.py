import unittest
import pandas as pd

from amirotest.tools.config import ConfMatrixBuilder

class TestConfMatrixBuilder(unittest.TestCase):
    def setUp(self) -> None:
        self.conf = {"opt1": [1,2], "opt2": ["A", "B"], "opt3": ["true", "false", "None"]}
        self.c_build = ConfMatrixBuilder()

    def test_get_row_col_counts(self):
        cols = 3
        rows = 12
        rows_cols = self.c_build._get_conf_mat_size(self.conf)
        self.assertEqual(rows_cols[0], rows)
        self.assertEqual(rows_cols[1], cols)
    # create empty matrix
    def test_augment_config(self):
        rows, cols = self.c_build._get_conf_mat_size(self.conf)
        aug_conf = self.c_build.augment_config(self.conf)
        print(aug_conf)
        for row in aug_conf:
            self.assertEqual(cols, len(row))

    def test_build_dataframe(self):
        df: pd.DataFrame = self.c_build.build_dataframe_config(self.conf)
        print(df)
        shape = df.shape
        self.assertEqual((12,3), shape)
