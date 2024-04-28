// Copyright 2024 Khalil Estell
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include <libhal-armcortex/dwt_counter.hpp>
#include <libhal-stm32f1/clock.hpp>
#include <libhal-stm32f1/constants.hpp>
#include <libhal-stm32f1/input_pin.hpp>
#include <libhal-stm32f1/output_pin.hpp>
#include <libhal-stm32f1/pin.hpp>
#include <libhal-util/steady_clock.hpp>

void application()
{
  auto cpu_frequency = hal::stm32f1::frequency(hal::stm32f1::peripheral::cpu);
  hal::cortex_m::dwt_counter steady_clock(cpu_frequency);
  hal::stm32f1::release_jtag_pins();
  hal::stm32f1::output_pin led('C', 13);
  // pin G0 on the STM micromod is port B, pin 4
  hal::stm32f1::input_pin button('B', 4);
  // internal pull up/down resistors don't work for STM, behaves like floating

  while (true) {
    using namespace std::chrono_literals;
    if (button.level()) {
      led.level(false);
    } else {
      led.level(true);
    }
    hal::delay(steady_clock, 200ms);
  }
}
