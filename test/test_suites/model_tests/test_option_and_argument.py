from enum import Flag
import unittest

from amirotest.model import \
    AosArgument, \
    AosOption, \
    GlobalOption, \
    UserOption, \
    AosVariable


class TestArgumentModel(unittest.TestCase):
    def test_create_arguments(self):
        arg = AosArgument("-WALL")
        self.assertEqual(arg.name, "-WALL")

    def test_create_option(self):
        name = "option"
        wall = "-WALL"
        dtest = "-Dtest"
        arg_string = " ".join([wall, dtest])
        args = [AosArgument(wall), AosArgument(dtest)]
        option = AosOption(name, arg_string)
        self.assertEqual(option.name, name)
        self.assertEqual(option.argument_str, arg_string)
        self.assertEqual(set(option.args),set(args))

    def test_option_has_unresolved_arguments(self):
        # example: -mfloat-abi=$(USE_FPU)
        unresolved_option = AosOption(
            'USE_FPU_OPT',
            '-mfloat-abi=$(USE_FPU) -mfpu=fpv4-sp-d16')
        self.assertFalse(unresolved_option.is_resolved())


    def test_no_substitution_option_in_resolved_argument(self):
        resolved_option = AosOption(
            'USE_FPU_OPT',
            '-mfloat-abi=no -mfpu=fpv4-sp-d16')
        self.assertTrue(resolved_option.is_resolved())
        sub_option_names = resolved_option.get_substitution_opt_names()
        self.assertEqual(sub_option_names, list())

    def test_get_substitution_option_from_argument_multiple_sub_option(self):
        unresolved_flag = AosOption(
            'USE_FPU_OPT',
            '-mfloat-abi=$(USE_FPU) -mfpu=$(USE_MPU_TYPE)')
        sub_flag_names = unresolved_flag.get_substitution_opt_names()
        self.assertEqual(sub_flag_names, ['USE_FPU', 'USE_MPU_TYPE'])

    def test_option_resolve_unresolved_option(self):
        unresolved_opt = AosOption(
            'USE_FPU_OPT',
            '-mfloat-abi=$(USE_FPU)')
        self.assertFalse(unresolved_opt.is_resolved())
        self.assertTrue(unresolved_opt.resolve(
            AosOption("USE_FPU", "fpu_value")))
        self.assertTrue(unresolved_opt.is_resolved())
        self.assertEqual(
            unresolved_opt.args[0].name,
            '-mfloat-abi=fpu_value'
        )

    def test_create_global_option(self):
        u_opt = GlobalOption("UDEFS", "-DBOARD_TOF_CONNECTED")
        self.assertEqual(len(u_opt.args), 1)
        self.assertEqual(
            u_opt.args[0].name,
            "-DBOARD_TOF_CONNECTED")

    def test_create_user_option_sub_argument(self):

        u_opt = UserOption("UDEFS", "-DBOARD_TOF_CONNECTED")
        self.assertEqual(len(u_opt.args), 1)
        self.assertEqual(
            u_opt.args[0].name,
            "-DBOARD_TOF_CONNECTED=$(BOARD_TOF_CONNECTED)")

    def test_create_user_option_sub_argument_already_exists(self):
        u_opt = UserOption("UDEFS", "-DBOARD_SENSORRING=$(BOARD_SENSORRING)")
        self.assertEqual(len(u_opt.args), 1)
        self.assertEqual(
            u_opt.args[0].name,
            "-DBOARD_SENSORRING=$(BOARD_SENSORRING)")

    def test_extract_variable_in_option_args(self):
        option = AosOption("USE_COPT", "-std=c99 -fshort-enums")
        aos_vars: list[AosVariable] = option.extract_variables()
        self.assertEqual(len(aos_vars), 2)
        self.assertEqual(aos_vars[0].name, "USE_COPT_STD")
        self.assertEqual(aos_vars[0].args[0].name, "c99")
        self.assertEqual(aos_vars[1].name, "USE_COPT_FSHORT_ENUMS")
        self.assertEqual(aos_vars[1].args[0].name, "fshort-enums")

        self.assertEqual(option.args[0].name, "-std=$(USE_COPT_STD)")
        self.assertEqual(option.args[1].name, "-$(USE_COPT_FSHORT_ENUMS)")

    def test_extract_variable_preprocessor_option(self):
        option = AosOption("USE_COPT", '-Wl,--print-memory-usage')
        aos_vars: list[AosVariable] = option.extract_variables()
        self.assertEqual(len(aos_vars), 1)
        self.assertEqual(aos_vars[0].name, "USE_COPT_WL_PRINT_MEMORY_USAGE")
        self.assertEqual(aos_vars[0].args[0].name, "Wl,--print-memory-usage")

    def test_extract_no_option(self):
        option = AosOption("USE_FPU", 'softfp')
        aos_vars: list[AosVariable] = option.extract_variables()
        self.assertEqual(len(aos_vars), 0)
