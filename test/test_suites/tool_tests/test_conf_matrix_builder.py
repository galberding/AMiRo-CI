import unittest
import pandas as pd

from amirotest.tools.config import ConfMatrixBuilder

class TestConfMatrixBuilder(unittest.TestCase):
    def setUp(self) -> None:
        self.conf = {"opt1": ["1","2"], "opt2": ["A", "B"], "opt3": ["true", "false", "None"], "opt4": ["42", "44", "45"]}
        self.c_build = ConfMatrixBuilder()

    def test_get_row_col_counts(self):
        conf = {"opt1": [1,2], "opt2": ["A", "B"], "opt3": ["true", "false", "None"]}
        cols = 3
        rows = 12
        rows_cols = self.c_build._get_conf_mat_size(conf)
        self.assertEqual(rows_cols[0], rows)
        self.assertEqual(rows_cols[1], cols)
    # create empty matrix
    def test_augment_config(self):
        _, cols = self.c_build._get_conf_mat_size(self.conf)
        aug_conf = self.c_build.augment_config(self.conf)
        # print(aug_conf)
        for row in aug_conf:
            self.assertEqual(cols, len(row))

    def test_ensure_correct_parameter_names_in_combined_config(self):
        """Checks two conditions:
        1. The Parameter names are assigned to the right column
        2. The columns are created correctly
        """
        df: pd.DataFrame = self.c_build.build_dataframe_config(self.conf)
        rows, _ = self.c_build._get_conf_mat_size(self.conf)
        for parameter_name, parameters in self.conf.items():
            val_count = df[parameter_name].value_counts()
            item_count = val_count.shape[0]
            for param in parameters:
                # print("REs:",)
                res = df[parameter_name].str.contains(param)
                self.assertEqual(res[res == True].shape[0], rows // item_count)
