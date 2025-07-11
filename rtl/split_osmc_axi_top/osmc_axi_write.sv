// Generated by CIRCT firtool-1.62.0
module osmc_axi_write(	// src/main/scala/AXI2UI/osmc_axi_write.scala:10:7
  input          clock,	// src/main/scala/AXI2UI/osmc_axi_write.scala:10:7
                 reset,	// src/main/scala/AXI2UI/osmc_axi_write.scala:10:7
  input  [7:0]   io_axi_awio_awid,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
  input  [35:0]  io_axi_awio_awaddr,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
  input  [7:0]   io_axi_awio_awlen,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
  input  [2:0]   io_axi_awio_awsize,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
  input  [1:0]   io_axi_awio_awburst,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
  input          io_axi_awio_awuser,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
  input  [3:0]   io_axi_awio_awqos,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
  input          io_axi_awio_awvalid,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
  output         io_axi_awio_awready,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
  input  [255:0] io_axi_wio_wdata,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
  input  [31:0]  io_axi_wio_wstrb,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
  input          io_axi_wio_wlast,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_axi_wio_wvalid,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
  output         io_axi_wio_wready,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
  output [7:0]   io_axi_bio_bid,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
  output         io_axi_bio_buser,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_axi_bio_bvalid,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
  input          io_axi_bio_bready,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_ui_awio_ready,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
  output         io_ui_awio_valid,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
  output [35:0]  io_ui_awio_bits_addr,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
  output [9:0]   io_ui_awio_bits_token,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
  input          io_ui_wio_ready,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
  output         io_ui_wio_valid,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
  output [511:0] io_ui_wio_bits_wdata,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
  output [63:0]  io_ui_wio_bits_wstrb,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
  input  [9:0]   io_token_inio_awtoken,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
  output         io_token_countio_token_awen,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
  input          io_ready_stall,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_wconsis,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
  output [71:0]  io_consis_addr_io_addr_start_0,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_start_1,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_start_2,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_start_3,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_start_4,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_start_5,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_start_6,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_start_7,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_start_8,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_start_9,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_start_10,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_start_11,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_start_12,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_start_13,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_start_14,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_start_15,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_start_16,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_start_17,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_start_18,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_start_19,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_start_20,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_start_21,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_start_22,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_start_23,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_start_24,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_start_25,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_start_26,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_start_27,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_start_28,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_start_29,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_start_30,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_start_31,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_start_32,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_end_0,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_end_1,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_end_2,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_end_3,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_end_4,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_end_5,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_end_6,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_end_7,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_end_8,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_end_9,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_end_10,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_end_11,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_end_12,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_end_13,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_end_14,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_end_15,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_end_16,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_end_17,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_end_18,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_end_19,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_end_20,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_end_21,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_end_22,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_end_23,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_end_24,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_end_25,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_end_26,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_end_27,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_end_28,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_end_29,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_end_30,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_end_31,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_addr_end_32,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
  output [4:0]   io_consis_addr_io_axi_ptr,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_consis_addr_io_ui_ptr,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
  output [31:0]  io_ui_wtcmd_counter,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
                 io_axi_wtcmd_counter,	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
  input          io_apb_config_done	// src/main/scala/AXI2UI/osmc_axi_write.scala:63:12
);

  wire         io_axi_bio_bvalid_0;	// src/main/scala/AXI2UI/osmc_axi_write.scala:166:64
  wire         io_axi_wio_wready_0;	// src/main/scala/AXI2UI/osmc_axi_write.scala:158:102
  wire         _u_axi_awb_fifo_out_io_fifo_wio_full;	// src/main/scala/AXI2UI/osmc_axi_write.scala:125:32
  wire [8:0]   _u_axi_awb_fifo_out_io_fifo_rio_rdata;	// src/main/scala/AXI2UI/osmc_axi_write.scala:125:32
  wire         _u_axi_awb_fifo_out_io_fifo_rio_empty;	// src/main/scala/AXI2UI/osmc_axi_write.scala:125:32
  wire         _u_axi_wb_fifo_io_fifo_wio_full;	// src/main/scala/AXI2UI/osmc_axi_write.scala:120:27
  wire         _u_axi_wb_fifo_io_fifo_rio_empty;	// src/main/scala/AXI2UI/osmc_axi_write.scala:120:27
  wire         _u_ui_write_data_io_fifol2_wrio_ren;	// src/main/scala/AXI2UI/osmc_axi_write.scala:114:29
  wire         _u_ui_write_cmd_io_ui_awio_valid;	// src/main/scala/AXI2UI/osmc_axi_write.scala:109:29
  wire [35:0]  _u_ui_write_cmd_io_ui_awio_bits_addr;	// src/main/scala/AXI2UI/osmc_axi_write.scala:109:29
  wire         _u_ui_write_cmd_io_fifol2_awrio_ren;	// src/main/scala/AXI2UI/osmc_axi_write.scala:109:29
  wire         _u_axi_w_fifol2_io_fifo_wio_full;	// src/main/scala/AXI2UI/osmc_axi_write.scala:104:28
  wire [575:0] _u_axi_w_fifol2_io_fifo_rio_rdata;	// src/main/scala/AXI2UI/osmc_axi_write.scala:104:28
  wire         _u_axi_w_fifol2_io_fifo_rio_empty;	// src/main/scala/AXI2UI/osmc_axi_write.scala:104:28
  wire         _u_axi_w_fifol1_io_fifo_wio_full;	// src/main/scala/AXI2UI/osmc_axi_write.scala:99:29
  wire [288:0] _u_axi_w_fifol1_io_fifo_rio_rdata;	// src/main/scala/AXI2UI/osmc_axi_write.scala:99:29
  wire         _u_axi_w_fifol1_io_fifo_rio_empty;	// src/main/scala/AXI2UI/osmc_axi_write.scala:99:29
  wire         _u_axi_aw_fifol2_io_fifo_wio_full;	// src/main/scala/AXI2UI/osmc_axi_write.scala:95:29
  wire [45:0]  _u_axi_aw_fifol2_io_fifo_rio_rdata;	// src/main/scala/AXI2UI/osmc_axi_write.scala:95:29
  wire         _u_axi_aw_fifol2_io_fifo_rio_empty;	// src/main/scala/AXI2UI/osmc_axi_write.scala:95:29
  wire         _u_axi_aw_fifol1_io_fifo_wio_full;	// src/main/scala/AXI2UI/osmc_axi_write.scala:89:29
  wire [53:0]  _u_axi_aw_fifol1_io_fifo_rio_rdata;	// src/main/scala/AXI2UI/osmc_axi_write.scala:89:29
  wire         _u_axi_aw_fifol1_io_fifo_rio_empty;	// src/main/scala/AXI2UI/osmc_axi_write.scala:89:29
  wire         _u_axi_write_burst_clip_io_fifol1_awrio_ren;	// src/main/scala/AXI2UI/osmc_axi_write.scala:82:36
  wire         _u_axi_write_burst_clip_io_fifol2_awwio_wen;	// src/main/scala/AXI2UI/osmc_axi_write.scala:82:36
  wire [45:0]  _u_axi_write_burst_clip_io_fifol2_awwio_wdata;	// src/main/scala/AXI2UI/osmc_axi_write.scala:82:36
  wire         _u_axi_write_burst_clip_io_fifol1_wrio_ren;	// src/main/scala/AXI2UI/osmc_axi_write.scala:82:36
  wire         _u_axi_write_burst_clip_io_fifol2_wwio_wen;	// src/main/scala/AXI2UI/osmc_axi_write.scala:82:36
  wire [575:0] _u_axi_write_burst_clip_io_fifol2_wwio_wdata;	// src/main/scala/AXI2UI/osmc_axi_write.scala:82:36
  reg  [35:0]  addr0;	// src/main/scala/AXI2UI/osmc_axi_write.scala:66:23
  reg  [7:0]   len;	// src/main/scala/AXI2UI/osmc_axi_write.scala:67:23
  reg  [2:0]   size;	// src/main/scala/AXI2UI/osmc_axi_write.scala:68:23
  reg  [1:0]   burst;	// src/main/scala/AXI2UI/osmc_axi_write.scala:69:23
  reg  [3:0]   qos;	// src/main/scala/AXI2UI/osmc_axi_write.scala:70:23
  reg          avalid;	// src/main/scala/AXI2UI/osmc_axi_write.scala:71:23
  reg          aready;	// src/main/scala/AXI2UI/osmc_axi_write.scala:72:23
  reg  [7:0]   awid;	// src/main/scala/AXI2UI/osmc_axi_write.scala:73:23
  reg          awuser;	// src/main/scala/AXI2UI/osmc_axi_write.scala:74:23
  reg          cmd_end0;	// src/main/scala/AXI2UI/osmc_axi_write.scala:77:28
  reg          cmd_hold;	// src/main/scala/AXI2UI/osmc_axi_write.scala:78:28
  reg  [31:0]  axi_wtcmd_cnt;	// src/main/scala/AXI2UI/osmc_axi_write.scala:79:30
  wire         _u_axi_awb_fifo_out_io_fifo_wio_wen_T = avalid & aready;	// src/main/scala/AXI2UI/osmc_axi_write.scala:71:23, :72:23, :87:29
  wire         _u_axi_aw_fifol1_io_fifo_wio_wen_T_5 =
    (_u_axi_awb_fifo_out_io_fifo_wio_wen_T | cmd_hold)
    & ~_u_axi_aw_fifol1_io_fifo_wio_full & ~io_wconsis;	// src/main/scala/AXI2UI/osmc_axi_write.scala:78:28, :87:29, :89:29, :92:{65,79,114,116}
  wire         _u_axi_wb_fifo_io_fifo_wio_wen_T = io_axi_wio_wvalid & io_axi_wio_wready_0;	// src/main/scala/AXI2UI/osmc_axi_write.scala:101:63, :158:102
  wire         _u_axi_awb_fifo_out_io_fifo_rio_ren_T =
    io_axi_bio_bvalid_0 & io_axi_bio_bready;	// src/main/scala/AXI2UI/osmc_axi_write.scala:123:60, :166:64
  wire         io_axi_awio_awready_0 =
    ~_u_axi_aw_fifol1_io_fifo_wio_full & ~io_wconsis & ~cmd_hold
    & ~_u_axi_awb_fifo_out_io_fifo_wio_full & io_apb_config_done;	// src/main/scala/AXI2UI/osmc_axi_write.scala:78:28, :89:29, :92:{79,116}, :125:32, :157:{83,96,134}
  assign io_axi_wio_wready_0 =
    ~_u_axi_w_fifol1_io_fifo_wio_full & ~_u_axi_wb_fifo_io_fifo_wio_full
    & io_apb_config_done;	// src/main/scala/AXI2UI/osmc_axi_write.scala:99:29, :120:27, :158:{27,69,102}
  assign io_axi_bio_bvalid_0 =
    ~_u_axi_wb_fifo_io_fifo_rio_empty & ~_u_axi_awb_fifo_out_io_fifo_rio_empty;	// src/main/scala/AXI2UI/osmc_axi_write.scala:120:27, :125:32, :166:{30,64,67}
  wire         cmd_en = io_axi_awio_awvalid & io_axi_awio_awready_0;	// src/main/scala/AXI2UI/osmc_axi_write.scala:147:37, :157:134
  always @(posedge clock) begin	// src/main/scala/AXI2UI/osmc_axi_write.scala:10:7
    if (reset) begin	// src/main/scala/AXI2UI/osmc_axi_write.scala:10:7
      addr0 <= 36'h0;	// src/main/scala/AXI2UI/osmc_axi_write.scala:66:23
      len <= 8'h0;	// src/main/scala/AXI2UI/osmc_axi_write.scala:67:23
      size <= 3'h0;	// src/main/scala/AXI2UI/osmc_axi_write.scala:68:23
      burst <= 2'h0;	// src/main/scala/AXI2UI/osmc_axi_write.scala:69:23
      qos <= 4'h0;	// src/main/scala/AXI2UI/osmc_axi_write.scala:70:23
      cmd_hold <= 1'h0;	// src/main/scala/AXI2UI/osmc_axi_write.scala:78:28
      axi_wtcmd_cnt <= 32'h0;	// src/main/scala/AXI2UI/osmc_axi_write.scala:79:30
    end
    else begin	// src/main/scala/AXI2UI/osmc_axi_write.scala:10:7
      if (cmd_en) begin	// src/main/scala/AXI2UI/osmc_axi_write.scala:147:37
        addr0 <= io_axi_awio_awaddr;	// src/main/scala/AXI2UI/osmc_axi_write.scala:66:23
        len <= io_axi_awio_awlen;	// src/main/scala/AXI2UI/osmc_axi_write.scala:67:23
        size <= io_axi_awio_awsize;	// src/main/scala/AXI2UI/osmc_axi_write.scala:68:23
        burst <= io_axi_awio_awburst;	// src/main/scala/AXI2UI/osmc_axi_write.scala:69:23
        qos <= io_axi_awio_awqos;	// src/main/scala/AXI2UI/osmc_axi_write.scala:70:23
      end
      else if (_u_axi_aw_fifol1_io_fifo_wio_wen_T_5) begin	// src/main/scala/AXI2UI/osmc_axi_write.scala:92:114
        addr0 <= 36'h0;	// src/main/scala/AXI2UI/osmc_axi_write.scala:66:23
        len <= 8'h0;	// src/main/scala/AXI2UI/osmc_axi_write.scala:67:23
        size <= 3'h0;	// src/main/scala/AXI2UI/osmc_axi_write.scala:68:23
        burst <= 2'h0;	// src/main/scala/AXI2UI/osmc_axi_write.scala:69:23
        qos <= 4'h0;	// src/main/scala/AXI2UI/osmc_axi_write.scala:70:23
      end
      cmd_hold <=
        cmd_end0 & _u_axi_aw_fifol1_io_fifo_wio_full | io_wconsis & cmd_end0
        | ~_u_axi_aw_fifol1_io_fifo_wio_wen_T_5 & cmd_hold;	// src/main/scala/AXI2UI/osmc_axi_write.scala:77:28, :78:28, :89:29, :92:114, :146:{24,35,85,109}
      if (_u_axi_awb_fifo_out_io_fifo_wio_wen_T)	// src/main/scala/AXI2UI/osmc_axi_write.scala:87:29
        axi_wtcmd_cnt <= axi_wtcmd_cnt + 32'h1;	// src/main/scala/AXI2UI/osmc_axi_write.scala:79:30, :87:54
    end
    avalid <= io_axi_awio_awvalid;	// src/main/scala/AXI2UI/osmc_axi_write.scala:71:23
    aready <= io_axi_awio_awready_0;	// src/main/scala/AXI2UI/osmc_axi_write.scala:72:23, :157:134
    awid <= io_axi_awio_awid;	// src/main/scala/AXI2UI/osmc_axi_write.scala:73:23
    awuser <= io_axi_awio_awuser;	// src/main/scala/AXI2UI/osmc_axi_write.scala:74:23
    cmd_end0 <= cmd_en;	// src/main/scala/AXI2UI/osmc_axi_write.scala:77:28, :147:37
  end // always @(posedge)
  osmc_axi_write_burst_clip u_axi_write_burst_clip (	// src/main/scala/AXI2UI/osmc_axi_write.scala:82:36
    .clock                       (clock),
    .reset                       (reset),
    .io_fifol1_awrio_ren         (_u_axi_write_burst_clip_io_fifol1_awrio_ren),
    .io_fifol1_awrio_rdata       (_u_axi_aw_fifol1_io_fifo_rio_rdata),	// src/main/scala/AXI2UI/osmc_axi_write.scala:89:29
    .io_fifol1_awrio_empty       (_u_axi_aw_fifol1_io_fifo_rio_empty),	// src/main/scala/AXI2UI/osmc_axi_write.scala:89:29
    .io_fifol2_awwio_wen         (_u_axi_write_burst_clip_io_fifol2_awwio_wen),
    .io_fifol2_awwio_wdata       (_u_axi_write_burst_clip_io_fifol2_awwio_wdata),
    .io_fifol2_awwio_full        (_u_axi_aw_fifol2_io_fifo_wio_full),	// src/main/scala/AXI2UI/osmc_axi_write.scala:95:29
    .io_fifol1_wrio_ren          (_u_axi_write_burst_clip_io_fifol1_wrio_ren),
    .io_fifol1_wrio_rdata        (_u_axi_w_fifol1_io_fifo_rio_rdata),	// src/main/scala/AXI2UI/osmc_axi_write.scala:99:29
    .io_fifol1_wrio_empty        (_u_axi_w_fifol1_io_fifo_rio_empty),	// src/main/scala/AXI2UI/osmc_axi_write.scala:99:29
    .io_fifol2_wwio_wen          (_u_axi_write_burst_clip_io_fifol2_wwio_wen),
    .io_fifol2_wwio_wdata        (_u_axi_write_burst_clip_io_fifol2_wwio_wdata),
    .io_fifol2_wwio_full         (_u_axi_w_fifol2_io_fifo_wio_full),	// src/main/scala/AXI2UI/osmc_axi_write.scala:104:28
    .io_token_inio_awtoken       (io_token_inio_awtoken),
    .io_token_countio_token_awen (io_token_countio_token_awen)
  );
  fwft_sync_fifo u_axi_aw_fifol1 (	// src/main/scala/AXI2UI/osmc_axi_write.scala:89:29
    .clock             (clock),
    .reset             (reset),
    .io_fifo_wio_wen   (_u_axi_aw_fifol1_io_fifo_wio_wen_T_5),	// src/main/scala/AXI2UI/osmc_axi_write.scala:92:114
    .io_fifo_wio_wdata ({1'h0, addr0, burst, len, size, qos}),	// src/main/scala/AXI2UI/osmc_axi_write.scala:66:23, :67:23, :68:23, :69:23, :70:23, :78:28, :93:41
    .io_fifo_wio_full  (_u_axi_aw_fifol1_io_fifo_wio_full),
    .io_fifo_rio_ren   (_u_axi_write_burst_clip_io_fifol1_awrio_ren),	// src/main/scala/AXI2UI/osmc_axi_write.scala:82:36
    .io_fifo_rio_rdata (_u_axi_aw_fifol1_io_fifo_rio_rdata),
    .io_fifo_rio_empty (_u_axi_aw_fifol1_io_fifo_rio_empty)
  );
  fwft_sync_fifo_1 u_axi_aw_fifol2 (	// src/main/scala/AXI2UI/osmc_axi_write.scala:95:29
    .clock             (clock),
    .reset             (reset),
    .io_fifo_wio_wen   (_u_axi_write_burst_clip_io_fifol2_awwio_wen),	// src/main/scala/AXI2UI/osmc_axi_write.scala:82:36
    .io_fifo_wio_wdata (_u_axi_write_burst_clip_io_fifol2_awwio_wdata),	// src/main/scala/AXI2UI/osmc_axi_write.scala:82:36
    .io_fifo_wio_full  (_u_axi_aw_fifol2_io_fifo_wio_full),
    .io_fifo_rio_ren   (_u_ui_write_cmd_io_fifol2_awrio_ren),	// src/main/scala/AXI2UI/osmc_axi_write.scala:109:29
    .io_fifo_rio_rdata (_u_axi_aw_fifol2_io_fifo_rio_rdata),
    .io_fifo_rio_empty (_u_axi_aw_fifol2_io_fifo_rio_empty)
  );
  fwft_sync_fifo_2 u_axi_w_fifol1 (	// src/main/scala/AXI2UI/osmc_axi_write.scala:99:29
    .clock             (clock),
    .reset             (reset),
    .io_fifo_wio_wen   (_u_axi_wb_fifo_io_fifo_wio_wen_T),	// src/main/scala/AXI2UI/osmc_axi_write.scala:101:63
    .io_fifo_wio_wdata ({io_axi_wio_wdata, io_axi_wio_wstrb, io_axi_wio_wlast}),	// src/main/scala/AXI2UI/osmc_axi_write.scala:102:48
    .io_fifo_wio_full  (_u_axi_w_fifol1_io_fifo_wio_full),
    .io_fifo_rio_ren   (_u_axi_write_burst_clip_io_fifol1_wrio_ren),	// src/main/scala/AXI2UI/osmc_axi_write.scala:82:36
    .io_fifo_rio_rdata (_u_axi_w_fifol1_io_fifo_rio_rdata),
    .io_fifo_rio_empty (_u_axi_w_fifol1_io_fifo_rio_empty)
  );
  fwft_sync_fifo_3 u_axi_w_fifol2 (	// src/main/scala/AXI2UI/osmc_axi_write.scala:104:28
    .clock             (clock),
    .reset             (reset),
    .io_fifo_wio_wen   (_u_axi_write_burst_clip_io_fifol2_wwio_wen),	// src/main/scala/AXI2UI/osmc_axi_write.scala:82:36
    .io_fifo_wio_wdata (_u_axi_write_burst_clip_io_fifol2_wwio_wdata),	// src/main/scala/AXI2UI/osmc_axi_write.scala:82:36
    .io_fifo_wio_full  (_u_axi_w_fifol2_io_fifo_wio_full),
    .io_fifo_rio_ren   (_u_ui_write_data_io_fifol2_wrio_ren),	// src/main/scala/AXI2UI/osmc_axi_write.scala:114:29
    .io_fifo_rio_rdata (_u_axi_w_fifol2_io_fifo_rio_rdata),
    .io_fifo_rio_empty (_u_axi_w_fifol2_io_fifo_rio_empty)
  );
  osmc_ui_write_cmd u_ui_write_cmd (	// src/main/scala/AXI2UI/osmc_axi_write.scala:109:29
    .clock                 (clock),
    .reset                 (reset),
    .io_ui_awio_ready      (io_ui_awio_ready),
    .io_ui_awio_valid      (_u_ui_write_cmd_io_ui_awio_valid),
    .io_ui_awio_bits_addr  (_u_ui_write_cmd_io_ui_awio_bits_addr),
    .io_ui_awio_bits_token (io_ui_awio_bits_token),
    .io_fifol2_awrio_ren   (_u_ui_write_cmd_io_fifol2_awrio_ren),
    .io_fifol2_awrio_rdata (_u_axi_aw_fifol2_io_fifo_rio_rdata),	// src/main/scala/AXI2UI/osmc_axi_write.scala:95:29
    .io_fifol2_awrio_empty (_u_axi_aw_fifol2_io_fifo_rio_empty),	// src/main/scala/AXI2UI/osmc_axi_write.scala:95:29
    .io_ready_stall        (io_ready_stall),
    .io_ui_wtcmd_counter   (io_ui_wtcmd_counter)
  );
  osmc_ui_write_data u_ui_write_data (	// src/main/scala/AXI2UI/osmc_axi_write.scala:114:29
    .io_ui_wio_ready      (io_ui_wio_ready),
    .io_ui_wio_valid      (io_ui_wio_valid),
    .io_ui_wio_bits_wdata (io_ui_wio_bits_wdata),
    .io_ui_wio_bits_wstrb (io_ui_wio_bits_wstrb),
    .io_fifol2_wrio_ren   (_u_ui_write_data_io_fifol2_wrio_ren),
    .io_fifol2_wrio_rdata (_u_axi_w_fifol2_io_fifo_rio_rdata),	// src/main/scala/AXI2UI/osmc_axi_write.scala:104:28
    .io_fifol2_wrio_empty (_u_axi_w_fifol2_io_fifo_rio_empty)	// src/main/scala/AXI2UI/osmc_axi_write.scala:104:28
  );
  fwft_sync_fifo_4 u_axi_wb_fifo (	// src/main/scala/AXI2UI/osmc_axi_write.scala:120:27
    .clock             (clock),
    .reset             (reset),
    .io_fifo_wio_wen   (_u_axi_wb_fifo_io_fifo_wio_wen_T & io_axi_wio_wlast),	// src/main/scala/AXI2UI/osmc_axi_write.scala:101:63, :121:80
    .io_fifo_wio_full  (_u_axi_wb_fifo_io_fifo_wio_full),
    .io_fifo_rio_ren   (_u_axi_awb_fifo_out_io_fifo_rio_ren_T),	// src/main/scala/AXI2UI/osmc_axi_write.scala:123:60
    .io_fifo_rio_empty (_u_axi_wb_fifo_io_fifo_rio_empty)
  );
  fwft_sync_fifo_5 u_axi_awb_fifo_out (	// src/main/scala/AXI2UI/osmc_axi_write.scala:125:32
    .clock             (clock),
    .reset             (reset),
    .io_fifo_wio_wen
      ((_u_axi_awb_fifo_out_io_fifo_wio_wen_T | cmd_hold)
       & ~_u_axi_aw_fifol1_io_fifo_wio_full & ~io_wconsis),	// src/main/scala/AXI2UI/osmc_axi_write.scala:78:28, :87:29, :89:29, :92:{79,116}, :126:{67,116}
    .io_fifo_wio_wdata ({awid, awuser}),	// src/main/scala/AXI2UI/osmc_axi_write.scala:73:23, :74:23, :127:50
    .io_fifo_wio_full  (_u_axi_awb_fifo_out_io_fifo_wio_full),
    .io_fifo_rio_ren   (_u_axi_awb_fifo_out_io_fifo_rio_ren_T),	// src/main/scala/AXI2UI/osmc_axi_write.scala:123:60
    .io_fifo_rio_rdata (_u_axi_awb_fifo_out_io_fifo_rio_rdata),
    .io_fifo_rio_empty (_u_axi_awb_fifo_out_io_fifo_rio_empty)
  );
  osmc_axi_consis_table w_axi_consis_table (	// src/main/scala/AXI2UI/osmc_axi_write.scala:130:32
    .clock                           (clock),
    .reset                           (reset),
    .io_axi_aio_aaddr                (io_axi_awio_awaddr),
    .io_axi_aio_alen                 (io_axi_awio_awlen),
    .io_axi_aio_asize                (io_axi_awio_awsize),
    .io_axi_aio_avalid               (io_axi_awio_awvalid),
    .io_axi_aio_aready               (io_axi_awio_awready_0),	// src/main/scala/AXI2UI/osmc_axi_write.scala:157:134
    .io_ui_aio_addr                  (_u_ui_write_cmd_io_ui_awio_bits_addr),	// src/main/scala/AXI2UI/osmc_axi_write.scala:109:29
    .io_ui_hsio_ready                (io_ui_awio_ready),
    .io_ui_hsio_valid                (_u_ui_write_cmd_io_ui_awio_valid),	// src/main/scala/AXI2UI/osmc_axi_write.scala:109:29
    .io_consis_addr_io_addr_start_0  (io_consis_addr_io_addr_start_0),
    .io_consis_addr_io_addr_start_1  (io_consis_addr_io_addr_start_1),
    .io_consis_addr_io_addr_start_2  (io_consis_addr_io_addr_start_2),
    .io_consis_addr_io_addr_start_3  (io_consis_addr_io_addr_start_3),
    .io_consis_addr_io_addr_start_4  (io_consis_addr_io_addr_start_4),
    .io_consis_addr_io_addr_start_5  (io_consis_addr_io_addr_start_5),
    .io_consis_addr_io_addr_start_6  (io_consis_addr_io_addr_start_6),
    .io_consis_addr_io_addr_start_7  (io_consis_addr_io_addr_start_7),
    .io_consis_addr_io_addr_start_8  (io_consis_addr_io_addr_start_8),
    .io_consis_addr_io_addr_start_9  (io_consis_addr_io_addr_start_9),
    .io_consis_addr_io_addr_start_10 (io_consis_addr_io_addr_start_10),
    .io_consis_addr_io_addr_start_11 (io_consis_addr_io_addr_start_11),
    .io_consis_addr_io_addr_start_12 (io_consis_addr_io_addr_start_12),
    .io_consis_addr_io_addr_start_13 (io_consis_addr_io_addr_start_13),
    .io_consis_addr_io_addr_start_14 (io_consis_addr_io_addr_start_14),
    .io_consis_addr_io_addr_start_15 (io_consis_addr_io_addr_start_15),
    .io_consis_addr_io_addr_start_16 (io_consis_addr_io_addr_start_16),
    .io_consis_addr_io_addr_start_17 (io_consis_addr_io_addr_start_17),
    .io_consis_addr_io_addr_start_18 (io_consis_addr_io_addr_start_18),
    .io_consis_addr_io_addr_start_19 (io_consis_addr_io_addr_start_19),
    .io_consis_addr_io_addr_start_20 (io_consis_addr_io_addr_start_20),
    .io_consis_addr_io_addr_start_21 (io_consis_addr_io_addr_start_21),
    .io_consis_addr_io_addr_start_22 (io_consis_addr_io_addr_start_22),
    .io_consis_addr_io_addr_start_23 (io_consis_addr_io_addr_start_23),
    .io_consis_addr_io_addr_start_24 (io_consis_addr_io_addr_start_24),
    .io_consis_addr_io_addr_start_25 (io_consis_addr_io_addr_start_25),
    .io_consis_addr_io_addr_start_26 (io_consis_addr_io_addr_start_26),
    .io_consis_addr_io_addr_start_27 (io_consis_addr_io_addr_start_27),
    .io_consis_addr_io_addr_start_28 (io_consis_addr_io_addr_start_28),
    .io_consis_addr_io_addr_start_29 (io_consis_addr_io_addr_start_29),
    .io_consis_addr_io_addr_start_30 (io_consis_addr_io_addr_start_30),
    .io_consis_addr_io_addr_start_31 (io_consis_addr_io_addr_start_31),
    .io_consis_addr_io_addr_start_32 (io_consis_addr_io_addr_start_32),
    .io_consis_addr_io_addr_end_0    (io_consis_addr_io_addr_end_0),
    .io_consis_addr_io_addr_end_1    (io_consis_addr_io_addr_end_1),
    .io_consis_addr_io_addr_end_2    (io_consis_addr_io_addr_end_2),
    .io_consis_addr_io_addr_end_3    (io_consis_addr_io_addr_end_3),
    .io_consis_addr_io_addr_end_4    (io_consis_addr_io_addr_end_4),
    .io_consis_addr_io_addr_end_5    (io_consis_addr_io_addr_end_5),
    .io_consis_addr_io_addr_end_6    (io_consis_addr_io_addr_end_6),
    .io_consis_addr_io_addr_end_7    (io_consis_addr_io_addr_end_7),
    .io_consis_addr_io_addr_end_8    (io_consis_addr_io_addr_end_8),
    .io_consis_addr_io_addr_end_9    (io_consis_addr_io_addr_end_9),
    .io_consis_addr_io_addr_end_10   (io_consis_addr_io_addr_end_10),
    .io_consis_addr_io_addr_end_11   (io_consis_addr_io_addr_end_11),
    .io_consis_addr_io_addr_end_12   (io_consis_addr_io_addr_end_12),
    .io_consis_addr_io_addr_end_13   (io_consis_addr_io_addr_end_13),
    .io_consis_addr_io_addr_end_14   (io_consis_addr_io_addr_end_14),
    .io_consis_addr_io_addr_end_15   (io_consis_addr_io_addr_end_15),
    .io_consis_addr_io_addr_end_16   (io_consis_addr_io_addr_end_16),
    .io_consis_addr_io_addr_end_17   (io_consis_addr_io_addr_end_17),
    .io_consis_addr_io_addr_end_18   (io_consis_addr_io_addr_end_18),
    .io_consis_addr_io_addr_end_19   (io_consis_addr_io_addr_end_19),
    .io_consis_addr_io_addr_end_20   (io_consis_addr_io_addr_end_20),
    .io_consis_addr_io_addr_end_21   (io_consis_addr_io_addr_end_21),
    .io_consis_addr_io_addr_end_22   (io_consis_addr_io_addr_end_22),
    .io_consis_addr_io_addr_end_23   (io_consis_addr_io_addr_end_23),
    .io_consis_addr_io_addr_end_24   (io_consis_addr_io_addr_end_24),
    .io_consis_addr_io_addr_end_25   (io_consis_addr_io_addr_end_25),
    .io_consis_addr_io_addr_end_26   (io_consis_addr_io_addr_end_26),
    .io_consis_addr_io_addr_end_27   (io_consis_addr_io_addr_end_27),
    .io_consis_addr_io_addr_end_28   (io_consis_addr_io_addr_end_28),
    .io_consis_addr_io_addr_end_29   (io_consis_addr_io_addr_end_29),
    .io_consis_addr_io_addr_end_30   (io_consis_addr_io_addr_end_30),
    .io_consis_addr_io_addr_end_31   (io_consis_addr_io_addr_end_31),
    .io_consis_addr_io_addr_end_32   (io_consis_addr_io_addr_end_32),
    .io_consis_addr_io_axi_ptr       (io_consis_addr_io_axi_ptr),
    .io_consis_addr_io_ui_ptr        (io_consis_addr_io_ui_ptr)
  );
  assign io_axi_awio_awready = io_axi_awio_awready_0;	// src/main/scala/AXI2UI/osmc_axi_write.scala:10:7, :157:134
  assign io_axi_wio_wready = io_axi_wio_wready_0;	// src/main/scala/AXI2UI/osmc_axi_write.scala:10:7, :158:102
  assign io_axi_bio_bid = _u_axi_awb_fifo_out_io_fifo_rio_rdata[8:1];	// src/main/scala/AXI2UI/osmc_axi_write.scala:10:7, :125:32, :163:65
  assign io_axi_bio_buser = _u_axi_awb_fifo_out_io_fifo_rio_rdata[0];	// src/main/scala/AXI2UI/osmc_axi_write.scala:10:7, :125:32, :165:65
  assign io_axi_bio_bvalid = io_axi_bio_bvalid_0;	// src/main/scala/AXI2UI/osmc_axi_write.scala:10:7, :166:64
  assign io_ui_awio_valid = _u_ui_write_cmd_io_ui_awio_valid;	// src/main/scala/AXI2UI/osmc_axi_write.scala:10:7, :109:29
  assign io_ui_awio_bits_addr = _u_ui_write_cmd_io_ui_awio_bits_addr;	// src/main/scala/AXI2UI/osmc_axi_write.scala:10:7, :109:29
  assign io_axi_wtcmd_counter = axi_wtcmd_cnt;	// src/main/scala/AXI2UI/osmc_axi_write.scala:10:7, :79:30
endmodule

