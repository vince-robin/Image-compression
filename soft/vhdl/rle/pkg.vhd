library ieee;
use ieee.std_logic_1164.all;

package pkg is

	constant IN_LENGTH:  natural := 64;
	
    type block_flatten  is array (natural range <>)  of integer;
    
    function run_length_encode(img : block_flatten(0 to (IN_LENGTH-1))) return block_flatten;
          
end pkg;


package body pkg is

  function run_length_encode(img : block_flatten(0 to (IN_LENGTH-1))) return block_flatten is
	  variable i : integer;
	  variable j : integer;
	  variable skip : integer;
	  variable output : block_flatten(0 to (2*IN_LENGTH-1)):=(others=> 0);
	  begin
		  i := 0;
		  j := 0;
		  skip := 0;
		  while(i < IN_LENGTH) loop
				if(img(i) /= 0) then
					 output(j):=img(i);
					 output(j+1):=skip;
					 j := j+2;
					 skip:= 0;
				else 
					 skip := skip+1;
				end if;
				i := i + 1;
		  end loop;
	  return output;
  end run_length_encode;

end package body;
