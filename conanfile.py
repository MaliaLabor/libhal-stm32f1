#!/usr/bin/python
#
# Copyright 2024 Khalil Estell
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from conan import ConanFile
import os


required_conan_version = ">=2.0.14"


class libhal_stm32f1_conan(ConanFile):
    name = "libhal-stm32f1"
    license = "Apache-2.0"
    homepage = "https://libhal.github.io/libhal-stm32f1"
    description = ("A collection of drivers and libraries for the stm32f1 "
                   "series microcontrollers from NXP")
    topics = ("arm", "microcontroller", "lpc", "stm32f1",
              "stm32f1xx", "stm32f172", "stm32f174", "stm32f178", "stm32f188")
    settings = "compiler", "build_type", "os", "arch"

    python_requires = "libhal-bootstrap/[^1.0.3]"
    python_requires_extend = "libhal-bootstrap.library"

    options = {
        "platform": ["ANY"],
    }
    default_options = {
        "platform": "ANY",
    }

    def requirements(self):
        self.requires("libhal-armcortex/[^3.0.2]", transitive_headers=True)

    def add_linker_scripts_to_link_flags(self):
        linker_script_name = list(str(self.options.platform))
        # Replace the MCU number and pin count number with 'x' (don't care)
        # to map to the linker script
        linker_script_name[8] = 'x'
        linker_script_name[9] = 'x'
        linker_script_name = "".join(linker_script_name)

        self.cpp_info.exelinkflags = [
            "-L" + os.path.join(self.package_folder, "linker_scripts"),
            "-T" + os.path.join("libhal-stm32f1", linker_script_name + ".ld"),
        ]

    @property
    def _is_me(self):
        return (
            str(self.options.platform).startswith("stm32f1") and
            len(str(self.options.platform)) == 11
        )

    def package_info(self):
        self.cpp_info.libs = ["libhal-stm32f1"]
        self.cpp_info.set_property("cmake_target_name", "libhal::stm32f1")

        if self.settings.os == "baremetal" and self._is_me:
            self.add_linker_scripts_to_link_flags()
            self.buildenv_info.define("LIBHAL_PLATFORM",
                                      str(self.options.platform))
            self.buildenv_info.define("LIBHAL_PLATFORM_LIBRARY",
                                      "stm32f1")

    def package_id(self):
        if self.info.options.get_safe("platform"):
            del self.info.options.platform
