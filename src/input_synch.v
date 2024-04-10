module input_synch
(
	input wire clk,
	input wire reset,
	output wire sync_reset,
	input wire synch_in,
	output wire synch_out
);
	reg [1:0] chain0, chain1;
	
	// the reset output is asynchronous when activated and becomes synchronous when deactivated because of the chain0 pipeline
	always @ (posedge clk)
	begin
		chain0[1:0] <= {(chain0[0] & !reset), reset};
		chain1[1:0] <= {chain1[0], synch_in};
	end	

	assign synch_reset = (chain0[1] & !reset);
	assign synch_out	 = (chain1[1] & !reset);
	
endmodule
