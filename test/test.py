# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: MIT

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

@cocotb.test()
async def test_project(dut):
  dut._log.info("Start")
  
  # Our example module doesn't use clock and reset, but we show how to use them here anyway.
  clock = Clock(dut.clk, 10, units="us")
  cocotb.start_soon(clock.start())

  # Reset
  dut._log.info("Reset")
  dut.ena.value = 1
  dut.ui_in.value = 0
  dut.uio_in.value = 0
  dut.rst_n.value = 0

  dut._log.info("run for 10 clock cycles and then release reset")
  await ClockCycles(dut.clk, 20)
  dut.rst_n.value = 1

  # Set the both target inputs to 0xF values, wait one clock cycle, wait one clock cycle, then activate MOTION_Input and wait 1 clock cycle, then deactivate Motion Input, then wait 20 clock cycles, then check the output
  dut._log.info("Test")
  dut.ui_in.value = 255
  await ClockCycles(dut.clk, 40)
  
  dut.uio_in.value = 1
  await ClockCycles(dut.clk, 40)
  
  dut.uio_in.value = 0
  await ClockCycles(dut.clk, 1000)
  
  assert dut.uo_out.value == 255
