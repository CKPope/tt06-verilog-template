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

  # INCREMENTING TEST: Set the both target inputs to 0xF values for each axis, wait one clock cycle, then activate MOTION_Input and wait 2 clock cycles, then deactivate Motion Input, then run 20 clock cycles, then check the output for test1

  dut._log.info("Test1")
  dut.ui_in.value = 255
  await ClockCycles(dut.clk, 1)
  
  dut.uio_in.value = 1
  await ClockCycles(dut.clk, 2)
  
  dut.uio_in.value = 0
  await ClockCycles(dut.clk, 20)
  
  assert dut.uo_out.value == 255

  # INDEPENDENT DECREMENTING TEST:Set the both target inputs to 7 values (0 for one axis, 7 for the other axis), wait one clock cycle, then activate MOTION_Input and wait 2 clock cycles, then deactivate Motion Input, then run 20 clock cycles, then check the output for test2
  dut._log.info("Test2")
  dut.ui_in.value = 7
  await ClockCycles(dut.clk, 1)
  
  dut.uio_in.value = 1
  await ClockCycles(dut.clk, 2)
  
  dut.uio_in.value = 0
  await ClockCycles(dut.clk, 20)
  
  assert dut.uo_out.value == 7
