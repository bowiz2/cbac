analyze -format vhdl i8051_lib.vhd
analyze -format vhdl i8051_ctr.vhd

vhdlout_architecture_name = "SYN"
vhdlout_use_packages = {"IEEE.std_logic_1164", "IEEE.std_logic_arith.all", "LSI_10K.COMPONENTS.all"}

elaborate i8051_ctr
compile
write -format vhdl -hierarchy -output i8051_ctr_gate.vhd
write -format db -hierarchy -output i8051_ctr_gate.db
report_area
report_timing

exit