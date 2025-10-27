# usage: in top directory: sh ./src/script/fsdbdump.axi.sh
SIG_HEAD=osmc_axi_top_top/osmc_axi_top
fsdbreport axi2ui.fsdb -exp "$SIG_HEAD/clock && $SIG_HEAD/io_ario_arvalid && $SIG_HEAD/io_ario_arready" -s "$SIG_HEAD/io_ario_arid" -csv -of h -o report.arid.txt
fsdbreport axi2ui.fsdb -exp "$SIG_HEAD/clock && $SIG_HEAD/io_rio_rvalid && $SIG_HEAD/io_rio_rready && $SIG_HEAD/io_rio_rlast" -s "$SIG_HEAD/io_rio_rid" -csv -of h -o report.rid.txt
fsdbreport axi2ui.fsdb -exp "$SIG_HEAD/clock && $SIG_HEAD/io_awio_awvalid && $SIG_HEAD/io_awio_awready" -s "$SIG_HEAD/io_awio_awid" -csv -of h -o report.awid.txt
fsdbreport axi2ui.fsdb -exp "$SIG_HEAD/clock && $SIG_HEAD/io_bio_bvalid && $SIG_HEAD/io_bio_bready" -s "$SIG_HEAD/io_bio_bid" -csv -of h -o report.bid.txt
