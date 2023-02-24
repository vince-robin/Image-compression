echo "=> cleaning"
rm -rf work*.cf *.o

echo "=> analysis package"
echo ghdl -a pkg.vhd
ghdl -a pkg.vhd

echo "=> analysis design file"
echo ghdl -a zigzag.vhd
ghdl -a zigzag.vhd

echo "=> analysis test bench"
echo ghdl -a  zigzag_tb.vhd
ghdl -a  zigzag_tb.vhd

echo "=> elaboration"
echo ghdl -e zigzag_tb
ghdl -e zigzag_tb

echo "=> run"
echo ghdl -r zigzag_tb
ghdl -r zigzag_tb --wave=zigzag_tb.ghw

echo "=> result analysis"
gtkwave zigzag_tb.ghw zigzag_tb.sav
