import unittest

from amirotest.model import AosArgument, AosFlag
from amirotest.model.aos_flag import GlobalFlag, UserFlag

class TestArgumentModel(unittest.TestCase):
    def test_create_arguments(self):
        arg = AosArgument("-WALL")
        self.assertEqual(arg.name, "-WALL")

    def test_create_flag(self):
        name = "flag"
        wall = "-WALL"
        dtest = "-Dtest"
        arg_string = " ".join([wall, dtest])
        args = [AosArgument(wall), AosArgument(dtest)]
        flag = AosFlag(name, arg_string)
        self.assertEqual(flag.name, name)
        self.assertEqual(flag.argument_str, arg_string)
        self.assertEqual(set(flag.args),set(args))

    def test_flag_has_unresolved_arguments(self):
        # example: -mfloat-abi=$(USE_FPU)
        unresolved_flag = AosFlag(
            'USE_FPU_OPT',
            '-mfloat-abi=$(USE_FPU) -mfpu=fpv4-sp-d16')
        self.assertFalse(unresolved_flag.is_resolved())


    def test_no_substitution_flag_in_resolved_argument(self):
        resolved_flag = AosFlag(
            'USE_FPU_OPT',
            '-mfloat-abi=no -mfpu=fpv4-sp-d16')
        self.assertTrue(resolved_flag.is_resolved())
        sub_flag_names = resolved_flag.get_substitution_flag_names()
        self.assertEqual(sub_flag_names, list())

    def test_get_substitution_flag_from_argument_multiple_sub_flag(self):
        unresolved_flag = AosFlag(
            'USE_FPU_OPT',
            '-mfloat-abi=$(USE_FPU) -mfpu=$(USE_MPU_TYPE)')
        sub_flag_names = unresolved_flag.get_substitution_flag_names()
        self.assertEqual(sub_flag_names, ['USE_FPU', 'USE_MPU_TYPE'])

    def test_flag_resolve_unresolved_flag(self):
        unresolved_flag = AosFlag(
            'USE_FPU_OPT',
            '-mfloat-abi=$(USE_FPU)')
        self.assertFalse(unresolved_flag.is_resolved())
        self.assertTrue(unresolved_flag.resolve(
            AosFlag("USE_FPU", "fpu_value")))
        self.assertTrue(unresolved_flag.is_resolved())
        self.assertEqual(
            unresolved_flag.args[0].name,
            '-mfloat-abi=fpu_value'
        )

    def test_create_global_flag(self):
        u_flag = GlobalFlag("UDEFS", "-DBOARD_TOF_CONNECTED")
        self.assertEqual(len(u_flag.args), 1)
        self.assertEqual(
            u_flag.args[0].name,
            "-DBOARD_TOF_CONNECTED")

    def test_create_user_flag_sub_argument(self):

        u_flag = UserFlag("UDEFS", "-DBOARD_TOF_CONNECTED")
        self.assertEqual(len(u_flag.args), 1)
        self.assertEqual(
            u_flag.args[0].name,
            "-DBOARD_TOF_CONNECTED=$(BOARD_TOF_CONNECTED)")

    def test_create_user_flag_sub_argument_already_exists(self):
        u_flag = UserFlag("UDEFS", "-DBOARD_SENSORRING=$(BOARD_SENSORRING)")
        self.assertEqual(len(u_flag.args), 1)
        self.assertEqual(
            u_flag.args[0].name,
            "-DBOARD_SENSORRING=$(BOARD_SENSORRING)")
