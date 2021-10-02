import unittest
from amiroci.model.option import AosOption, MakeOption
from amiroci.model.argument import AosArgument
from amiroci.model.option.aos_opt import AosVariable, CfgOption


class TestOptions(unittest.TestCase):
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
        u_opt = CfgOption("UDEFS", "-DBOARD_TOF_CONNECTED")
        self.assertEqual(len(u_opt.args), 1)
        self.assertEqual(
            u_opt.args[0].name,
            "-DBOARD_TOF_CONNECTED")

    # def test_create_user_option_sub_argument(self):

    #     u_opt = MakeUserOption("UDEFS", "-DBOARD_TOF_CONNECTED")
    #     self.assertEqual(len(u_opt.args), 1)
    #     self.assertEqual(
    #         u_opt.args[0].name,
    #         "-DBOARD_TOF_CONNECTED=$(BOARD_TOF_CONNECTED)")

    # def test_create_user_option_sub_argument_already_exists(self):
    #     u_opt = MakeUserOption("UDEFS", "-DBOARD_SENSORRING=$(BOARD_SENSORRING)")
    #     self.assertEqual(len(u_opt.args), 1)
    #     self.assertEqual(
    #         u_opt.args[0].name,
    #         "-DBOARD_SENSORRING=$(BOARD_SENSORRING)")

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

    def test_variable_resolution(self):
        option = AosOption("USE_COPT", '-Wl,--print-memory-usage')
        aos_vars = option.extract_variables()
        self.assertFalse(option.is_resolved())
        self.assertTrue(option.resolve(aos_vars[0]))
        self.assertEqual(option.args[0].name, "-Wl,--print-memory-usage")

    def test_check_for_substitution_option(self):
        option = AosOption("USE_COPT", '-Wl,--print-memory-usage')
        option.extract_variables()
        opt_names = option.get_substitution_opt_names()
        self.assertEqual(len(opt_names), 1)
        self.assertEqual(opt_names[0], "USE_COPT_WL_PRINT_MEMORY_USAGE")

    def test_use_variable_extraction_for_reset(self):
        """Special by the reset is that argument string is utilized to generate the default values."""
        sub_option = AosOption("USE_FPU", 'softfp')
        self.check_resolution_reset(
            option=AosOption("USE_FPU_COPT", '-mfloat-abi=$(USE_FPU)'),
            before="-mfloat-abi=softfp",
            after="-mfloat-abi=$(USE_FPU)",
            res_option=sub_option
        )

    def test_option_reset_with_resolved_opt(self):
        self.check_resolution_reset(
            option=AosOption("USE_COPT", '-Wl,--print-memory-usage'),
            before="-Wl,--print-memory-usage",
            after="-$(USE_COPT_WL_PRINT_MEMORY_USAGE)"
        )

    # def test_resolution_of_aosconf_option(self):
    #     opt = AosconfOption("NAME", "SUB", "42")
    #     opt.resolve(AosVariable("SUB", "var"))
    #     self.assertTrue(opt.is_resolved())
    #     self.assertTrue(opt.args[0], "var")

    def test_aos_variable_returns_no_build_option(self):
        var = AosVariable("OPT", "Value")
        self.assertEqual("", var.get_build_option())

    def test_make_option_fomrat(self):
        name = 'OPT_NAME'
        args = ['-opt1', '-opt2']
        make_opt = MakeOption(name, args)
        self.assertEqual(f'{name}={args[0]} {args[1]}', make_opt.get_build_option())

    def check_resolution_reset(self,option: AosOption,
                               before: str,
                               after: str,
                               res_option: AosOption=None):
        aos_vars = option.extract_variables()
        if res_option:
            option.resolve(res_option)
        else:
            option.resolve(aos_vars[0])
        # Before reset (after resolution)
        self.assertEqual(option.args[0], AosArgument(before))
        option.reset_resolution()
        # After reset
        self.assertEqual(option.args[0], AosArgument(after))
