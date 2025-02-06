import bind_offs;
import cast_ons;
import needles;

def left_decrease(loop_1, loop_2):{
	xfer loop_2 across to Back bed;
	xfer Last_Pass.values() 1 to Leftward to Front bed;
	in Rightward direction:{
		knit loop_1;
		tuck loop_2;
	}
}
def right_decrease(loop_1, loop_2):{
	xfer loop_1 across to Back bed;
	xfer Last_Pass.values() 1 to Rightward to Front bed;
	in Rightward direction:{
		tuck loop_1;
		knit loop_2;
	}
}
def knit_two(loop_1, loop_2):{
	in Rightward direction:{
		knit [loop_1, loop_2];
	}
}

with Carrier as yarn:{
	width = (lace_reps*8) + 2;
	cast_ons.alt_tuck_cast_on(width, tuck_lines=1, knit_lines=0);

	for _ in range(0, height):{
		in reverse direction:{
			knit Loops;
		}
		for i, n in enumerate(Front_Loops[0::2]):{
			rep_position = i%4;
			if rep_position == 1:{
				left_decrease(n, n+1);
			} elif rep_position == 3:{
				right_decrease(n, n+1);
			} else:{
				knit_two(n, n+1);
			}
		}
	}
	in reverse direction:{
		knit Loops;
	}
	if bind:{
		bind_offs.chain_bind_off(Loops, reverse, extra_knits=6, hold = False);
	}
}