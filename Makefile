PWD 		= $(shell pwd)
SRC_DIR 	= $(PWD)/src
AXI2UI_DIR 	= $(SRC_DIR)/axi2ui
RTL_DIR 	= $(PWD)/rtl
WAIVER_DIR 	= $(PWD)/src
TRACE_DIR 	= $(PWD)/test/data
TRACE_FILE 	= $(TRACE_DIR)/cactusADM_0_rand100w.txt

init:
	picker export --autobuild=false $(RTL_DIR)/osmc_axi_top.sv -w $(PWD)/axi2ui.fst --sname osmc_axi_top --tdir $(AXI2UI_DIR) --lang python -e -c --sim verilator
	$(MAKE) -C $(AXI2UI_DIR)

test:
	python3 $(PWD)/main.py $(TRACE_FILE)
	gtkwave axi2ui.fst

clean:
	rm -rf $(AXI2UI_DIR)
	
.PHONY: init test