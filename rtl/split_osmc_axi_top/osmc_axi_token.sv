// Generated by CIRCT firtool-1.62.0
module osmc_axi_token(
  input        clock,
               reset,
  output [9:0] io_token_io_awtoken,
               io_token_io_artoken,
  input        io_token_countio_token_awen,
               io_token_countio_token_aren
);

  wire [9:0] ar_token_nxt;
  wire       _u_ar_token_fifo_io_fifo_rio_empty;
  wire       _u_aw_token_fifo_io_fifo_rio_empty;
  reg  [8:0] aw_counter;
  reg  [8:0] ar_counter;
  reg        aw_en_reg;
  reg        ar_en_reg;
  reg        aw_fullflag;
  reg        ar_fullflag;
  wire       aw_full = &aw_counter;
  wire       ar_full = &ar_counter;
  wire [1:0] _GEN = {aw_fullflag, ar_fullflag};
  wire       full_flag = ~(_GEN == 2'h0 | (&_GEN)) & (_GEN == 2'h1 | _GEN == 2'h2);
  wire [9:0] _GEN_0 = {1'h0, aw_counter};
  wire [9:0] _GEN_1 = {1'h0, ar_counter};
  assign ar_token_nxt = full_flag ? _GEN_1 + _GEN_0 - 10'h200 : _GEN_1 + _GEN_0;
  always @(posedge clock) begin
    if (reset) begin
      aw_counter <= 9'h0;
      ar_counter <= 9'h0;
      aw_fullflag <= 1'h0;
      ar_fullflag <= 1'h0;
    end
    else begin
      if (io_token_countio_token_awen)
        aw_counter <= aw_counter + 9'h1;
      if (io_token_countio_token_aren)
        ar_counter <= ar_counter + 9'h1;
      aw_fullflag <= aw_full & io_token_countio_token_awen ^ aw_fullflag;
      ar_fullflag <= ar_full & io_token_countio_token_aren ^ ar_fullflag;
    end
    aw_en_reg <= io_token_countio_token_awen;
    ar_en_reg <= io_token_countio_token_aren;
  end // always @(posedge)
  fwft_sync_fifo_11 u_aw_token_fifo (
    .clock             (clock),
    .reset             (reset),
    .io_fifo_wio_wen   (aw_en_reg),
    .io_fifo_wio_wdata (full_flag ? _GEN_0 + _GEN_1 - 10'h200 : _GEN_0 + _GEN_1),
    .io_fifo_rio_ren   (~_u_aw_token_fifo_io_fifo_rio_empty),
    .io_fifo_rio_rdata (io_token_io_awtoken),
    .io_fifo_rio_empty (_u_aw_token_fifo_io_fifo_rio_empty)
  );
  fwft_sync_fifo_11 u_ar_token_fifo (
    .clock             (clock),
    .reset             (reset),
    .io_fifo_wio_wen   (ar_en_reg),
    .io_fifo_wio_wdata (aw_en_reg & ar_en_reg ? ar_token_nxt - 10'h1 : ar_token_nxt),
    .io_fifo_rio_ren   (~_u_ar_token_fifo_io_fifo_rio_empty),
    .io_fifo_rio_rdata (io_token_io_artoken),
    .io_fifo_rio_empty (_u_ar_token_fifo_io_fifo_rio_empty)
  );
endmodule

