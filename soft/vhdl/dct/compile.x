echo "=> cleaning"
rm -rf work*.cf *.o

echo "=> analysis package"
echo ghdl -a pkg.vhd
ghdl -a pkg.vhd

echo "=> analysis design file"
echo ghdl -a dct.vhd
ghdl -a dct.vhd

echo "=> analysis test bench"
echo ghdl -a  dct_tb.vhd
ghdl -a  dct_tb.vhd

echo "=> elaboration"
echo ghdl -e dct_tb
ghdl -e dct_tb

echo "=> run"
echo ghdl -r dct_tb
ghdl -r dct_tb --wave=dct_tb.ghw

echo "=> result analysis"
gtkwave dct_tb.ghw dct_tb.sav
