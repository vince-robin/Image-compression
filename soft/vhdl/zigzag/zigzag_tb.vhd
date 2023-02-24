--------------------------------------------------------------------------------
-- this file was generated automatically by Vertigo Ruby utility
-- date : (d/m/y h:m) 09/02/2023 12:02
-- author : Vincent Robin
--------------------------------------------------------------------------------
 
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

library std;
use std.textio.all;

library work;
use work.pkg.all;

entity zigzag_tb is
end entity;

architecture bhv of zigzag_tb is

  constant number_of_inputs  : integer := BLOCK_SIZE; 
  constant number_of_outputs : integer := BLOCK_SIZE*BLOCK_SIZE; 
  constant HALF_PERIOD : time := 5 ns;

  signal zigzag_in  : one_block;
  signal zigzag_out : block_flatten(0 to number_of_outputs-1);
  
  signal clk : std_logic := '0';
  signal reset_n : std_logic := '0';
  signal oe : std_logic := '0';
  signal wr : std_logic := '0';
  
  signal running : boolean := true;
  
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
  dut : entity work.zigzag(arch)
    port map (
      clk        => clk       ,
      reset_n    => reset_n   ,
	  wr         => wr        ,
      oe         => oe        ,
      zigzag_in  => zigzag_in ,
      zigzag_out => zigzag_out   
    );
  --------------------------------------------------------------------------------
  -- sequential stimuli
  --------------------------------------------------------------------------------
  stim : process 
  
    file INFILE:  text open read_mode is "input.txt";
    variable input_block: one_block;
    variable INPUT_LINE: line;
    variable nb_lines: natural := 0;
 
  begin
	report "running testbench for zigzag_tb(arch)"; 
	oe <= '0';
	wr <= '0';
	
	for i in 0 to (number_of_inputs-1) loop 
		for j in 0 to (number_of_inputs-1) loop
			zigzag_in(i)(j) <= 0;
		end loop;
	end loop;
	
	report "waiting for asynchronous reset";
	wait until reset_n = '1';
	wait_cycles(10);
	   
	while not endfile(INFILE) loop 
		nb_lines := nb_lines + 1;
		for i in 0 to (number_of_inputs-1) loop 
			readline(INFILE, INPUT_LINE);
			for j in 0 to (number_of_inputs-1) loop 
				read(INPUT_LINE,input_block(i)(j));
			end loop;
		end loop; 
    end loop;
    file_close(INFILE);
    
    wr <= '1';
    zigzag_in <= input_block;
    wait_cycles(2);  
    
    oe <= '1';
	wait_cycles(10);  
	
    report "end of simulation";
	running <= false;
	wait;
  end process;

end bhv;
