#pragma once

#include <libhal/can.hpp>

#include "pin.hpp"

namespace hal::stm32f1 {
class can final : public hal::can
{
public:
  can(const can::settings& p_settings = {},
      can_pins p_pins = can_pins::pa11_pa12);
  void enable_self_test(bool p_enable);
  ~can() override;

private:
  void driver_configure(const settings& p_settings) override;
  void driver_bus_on() override;
  void driver_send(const message_t& p_message) override;
  void driver_on_receive(hal::callback<handler> p_handler) override;
};
}  // namespace hal::stm32f1
