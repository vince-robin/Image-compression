--------------------------------------------------------------------------------
-- this file was generated automatically by Vertigo Ruby utility
-- date : (d/m/y h:m) 24/02/2023 17:18
-- author : Vincent Robin - 2023
--------------------------------------------------------------------------------
 
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

library work;
use work.pkg.all;

 
entity dct_tb is
end entity;
 
architecture bhv of dct_tb is
  constant HALF_PERIOD : time :=5 ns;
 
  signal clk : std_logic := '0';
  signal reset_n : std_logic := '0';
  signal wr : std_logic := '0';
  signal oe : std_logic := '0';
  signal running : boolean := true;
 
  signal dct_in  : array_2d;
  signal dct_out : array_2d;
 
 
  procedure wait_cycles(n : natural) is 
  begin
    for i in 0 to n-1 loop
      wait until rising_edge(clk);
    end loop;
  end procedure;

begin
  --------------------------------------------------------------------------------
  -- clock and reset
  --------------------------------------------------------------------------------
  reset_n <= '0','1' after 123 ns;
   
  clk <= not(clk) after HALF_PERIOD when running else clk;
  --------------------------------------------------------------------------------
  -- Design Under Test
  --------------------------------------------------------------------------------
  dut : entity work.dct(arch)
    port map (
      clk     => clk    ,
      reset_n => reset_n,
      wr      => wr     ,
      oe      => oe     ,
      dct_in  => dct_in ,
      dct_out => dct_out
    );
  --------------------------------------------------------------------------------
  -- sequential stimuli
  --------------------------------------------------------------------------------
  stim : process
  begin
    report "running testbench for dct(arch)";
    report "waiting for asynchronous reset";
    wait until reset_n='1';
    wait_cycles(10);
    wr <= '1';
    dct_in <= ORIGINAL_BLOCK; 
    wait_cycles(2);   
    oe <= '1';
    wait_cycles(100);
    report "end of simulation";
    running <= false;
    wait;
  end process;
end bhv;
