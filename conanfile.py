from conan import ConanFile
from conan.tools.files import copy
from conan.tools.layout import basic_layout
from conan.tools.build import check_min_cppstd
from conan.errors import ConanInvalidConfiguration
import os

required_conan_version = ">=1.50.0"

class libhalSTM32F10x_conan(ConanFile):
    name = "libhal-stm32f10x"
    version = "0.0.1"
    license = "Apache-2.0"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://libhal.github.io/libhal-stm32f10x"
    description = ("Drivers for the stm32f10x series of microcontrollers using "
                    "libhal's abstractions.")
    topics = ("ARM", "microcontroller", "peripherals", "hardware", "stm32f10x")
    settings = "compiler"
    exports_sources = ("include/*", "linkers/*", "LICENSE")
    no_copy_source = True

    def package_id(self):
        self.info.clear()
    
    @property
    def _min_cppstd(self):
        return "20"

    @property
    def _compilers_minimum_version(self):
        return {
            "gcc": "11",
            "clang": "14",
            "apple-clang": "14.0.0"
        }

    def requirements(self):
        self.requires("libhal/0.3.3@")
        self.requires("libhal-util/0.3.7@")
        self.requires("libhal-armcortex/0.3.8@")
        self.requires("ring-span-lite/0.6.0")

    def validate(self):
        if self.settings.get_safe("compiler.cppstd"):
            check_min_cppstd(self, self._min_cppstd)

        def lazy_lt_semver(v1, v2):
                lv1 = [int(v) for v in v1.split(".")]
                lv2 = [int(v) for v in v2.split(".")]
                min_length = min(len(lv1), len(lv2))
                return lv1[:min_length] < lv2[:min_length]

        compiler = str(self.settings.compiler)
        version = str(self.settings.compiler.version)
        minimum_version = self._compilers_minimum_version.get(compiler, False)

        if minimum_version and lazy_lt_semver(version, minimum_version):
            raise ConanInvalidConfiguration(
                f"{self.name} {self.version} requires C++{self._min_cppstd}, which your compiler ({compiler}-{version}) does not support")

    def layout(self):
        basic_layout(self)

    def package(self):
        copy(self, "LICENSE", dst=os.path.join(
            self.package_folder, "licenses"),  src=self.source_folder)
        copy(self, "*.h", dst=os.path.join(self.package_folder, "include"),
             src=os.path.join(self.source_folder, "include"))
        copy(self, "*.hpp", dst=os.path.join(self.package_folder,
             "include"), src=os.path.join(self.source_folder, "include"))
        copy(self, "*.ld", dst=os.path.join(self.package_folder,
             "linkers"), src=os.path.join(self.source_folder, "linkers"))

    def package_info(self):
        requirements_list = ["libhal::libhal",
                             "libhal-util::libhal-util",
                             "libhal-armcortex::libhal-armcortex",
                             "ring-span-lite::ring-span-lite"]

        m4_architecture_flags = [
            "-mcpu=cortex-m4",
            "-mthumb",
            "-mfloat-abi=soft"
        ]

        linker_path = os.path.join(self.package_folder, "linkers")

        self.cpp_info.set_property("cmake_file_name", "libhal-stm32f10x")
        self.cpp_info.set_property("cmake_find_mode", "both")

        self.cpp_info.components["stm32f10x"].set_property(
            "cmake_target_name",  "libhal::stm32f10x")
        self.cpp_info.components["stm32f10x"].exelinkflags.append(
            "-L" + linker_path)
        self.cpp_info.components["stm32f10x"].requires = requirements_list

        def create_component(self, component, flags):
            link_script = "-Tlibhal-stm32f10x/" + component + ".ld"
            component_name = "libhal::" + component
            self.cpp_info.components[component].set_property(
                "cmake_target_name", component_name)
            self.cpp_info.components[component].requires = ["stm32f10x"]
            self.cpp_info.components[component].exelinkflags.append(link_script)
            self.cpp_info.components[component].exelinkflags.extend(flags)
            self.cpp_info.components[component].cflags = flags
            self.cpp_info.components[component].cxxflags = flags

        create_component(self, "stm32f103", m4_architecture_flags)