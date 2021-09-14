import unittest

from amirotest.tools.gcc_version_checker import GccVersionChecker, WrongGccVersion

class TestGccVersionChecker(unittest.TestCase):
    def setUp(self) -> None:
        self.version_str = """
Using built-in specs.
COLLECT_GCC=arm-none-eabi-gcc
COLLECT_LTO_WRAPPER=/usr/lib/gcc/arm-none-eabi/9.2.1/lto-wrapper
Target: arm-none-eabi
Configured with: ../configure --build=x86_64-linux-gnu --prefix=/usr --includedir='/usr/lib/include' --mandir='/usr/lib/share/man' --infodir='/usr/lib/share/info' --sysconfdir=/etc --localstatedir=/var --disable-silent-rules --libdir='/usr/lib/lib/x86_64-linux-gnu' --libexecdir='/usr/lib/lib/x86_64-linux-gnu' --disable-maintainer-mode --disable-dependency-tracking --mandir=/usr/share/man --enable-languages=c,c++,lto --enable-multilib --disable-decimal-float --disable-libffi --disable-libgomp --disable-libmudflap --disable-libquadmath --disable-libssp --disable-libstdcxx-pch --disable-nls --disable-shared --disable-threads --enable-tls --build=x86_64-linux-gnu --target=arm-none-eabi --with-system-zlib --with-gnu-as --with-gnu-ld --with-pkgversion=15:9-2019-q4-0ubuntu1 --without-included-gettext --prefix=/usr/lib --infodir=/usr/share/doc/gcc-arm-none-eabi/info --htmldir=/usr/share/doc/gcc-arm-none-eabi/html --pdfdir=/usr/share/doc/gcc-arm-none-eabi/pdf --bindir=/usr/bin --libexecdir=/usr/lib --libdir=/usr/lib --disable-libstdc++-v3 --host=x86_64-linux-gnu --with-headers=no --without-newlib --with-multilib-list=rmprofile CFLAGS='-g -O2 -fdebug-prefix-map=/build/gcc-arm-none-eabi-Gl9kT9/gcc-arm-none-eabi-9-2019-q4=. -fstack-protector-strong' CPPFLAGS='-Wdate-time -D_FORTIFY_SOURCE=2' CXXFLAGS='-g -O2 -fdebug-prefix-map=/build/gcc-arm-none-eabi-Gl9kT9/gcc-arm-none-eabi-9-2019-q4=. -fstack-protector-strong' FCFLAGS='-g -O2 -fdebug-prefix-map=/build/gcc-arm-none-eabi-Gl9kT9/gcc-arm-none-eabi-9-2019-q4=. -fstack-protector-strong' FFLAGS='-g -O2 -fdebug-prefix-map=/build/gcc-arm-none-eabi-Gl9kT9/gcc-arm-none-eabi-9-2019-q4=. -fstack-protector-strong' GCJFLAGS='-g -O2 -fdebug-prefix-map=/build/gcc-arm-none-eabi-Gl9kT9/gcc-arm-none-eabi-9-2019-q4=. -fstack-protector-strong' LDFLAGS='-Wl,-Bsymbolic-functions -Wl,-z,relro' OBJCFLAGS='-g -O2 -fdebug-prefix-map=/build/gcc-arm-none-eabi-Gl9kT9/gcc-arm-none-eabi-9-2019-q4=. -fstack-protector-strong' OBJCXXFLAGS='-g -O2 -fdebug-prefix-map=/build/gcc-arm-none-eabi-Gl9kT9/gcc-arm-none-eabi-9-2019-q4=. -fstack-protector-strong' INHIBIT_LIBC_CFLAGS=-DUSE_TM_CLONE_REGISTRY=0 AR_FOR_TARGET=arm-none-eabi-ar AS_FOR_TARGET=arm-none-eabi-as LD_FOR_TARGET=arm-none-eabi-ld NM_FOR_TARGET=arm-none-eabi-nm OBJDUMP_FOR_TARGET=arm-none-eabi-objdump RANLIB_FOR_TARGET=arm-none-eabi-ranlib READELF_FOR_TARGET=arm-none-eabi-readelf STRIP_FOR_TARGET=arm-none-eabi-strip
Thread model: single
gcc version {}.{}.{} 20191025 (release) [ARM/arm-9-branch revision 277599] (15:9-2019-q4-0ubuntu1)
        """
        self.checker = GccVersionChecker()

    def test_extract_version(self):
        major, minor, bug = self.checker.get_version(self.version_str.format(9, 2, 1))
        self.assertEqual(9, major)
        self.assertEqual(2, minor)
        self.assertEqual(1, bug)

    def test_raise_WronGccVersionDetected(self):
        self.assertRaises(WrongGccVersion, self.checker.check_version, (8, 0, 0))

    def test_load_current_version(self):
        v_str = self.checker.get_version_string()
        version = self.checker.get_version(v_str)
        self.assertGreaterEqual(version[0], 0)
        self.assertGreaterEqual(version[1], 0)
        self.assertGreaterEqual(version[2], 0)

    def test_validate(self):
        self.assertTrue(self.checker.validate())
