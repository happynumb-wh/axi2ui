PWD 			= $(shell pwd)
SRC_DIR 		= $(PWD)/src
AXI2UI_DIR 		= $(SRC_DIR)/axi2ui
RTL_DIR 		= $(PWD)/rtl
WAIVER_DIR 		= $(PWD)/src
TRACE_DIR 		= $(PWD)/test/data
TRACE_FILE 		= $(TRACE_DIR)/trace2/bzip2_liberty_0_rand500w.txt
INTERNAL_FILE 	= $(PWD)/internal.yaml

init:
	picker export --autobuild=false $(RTL_DIR)/osmc_axi_top.sv -w $(PWD)/axi2ui.fst --sname osmc_axi_top --tdir $(AXI2UI_DIR) --lang python -e -c --sim verilator --internal $(INTERNAL_FILE)
	$(MAKE) -C $(AXI2UI_DIR)

test:
	python3 $(SRC_DIR)/main.py $(TRACE_FILE)

run:
	pytest --toffee-report -sv $(SRC_DIR)

clean:
	rm -rf $(AXI2UI_DIR)
	
.PHONY: init test