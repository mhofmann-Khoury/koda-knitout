import cast_ons;
import needles;
import bind_offs;

def rightward_cable(loop_1, loop_2):{
	xfer [loop_1, loop_2] across to Back bed;
	xfer Back_Loops[0] 1 to Rightward to Front bed;
	xfer Back_Loops 1 to Leftward to Front bed;
	in Rightward direction:{
		knit [loop_1, loop_2];
	}
}

def leftward_cable(loop_1, loop_2):{
	xfer [loop_1, loop_2] across to Back bed;
	xfer Back_Loops[1] 1 to Leftward to Front bed;
	xfer Back_Loops 1 to Rightward to Front bed;
	in Rightward direction:{
		knit [loop_1, loop_2];
	}

}

def knit_two(loop_1, loop_2):{
	in Rightward direction:{
		knit [loop_1, loop_2];
	}
}

with Carrier as yarn:{
	width = (cable_reps * 8)+2;
	cast_ons.alt_tuck_cast_on(width, tuck_lines=1, knit_lines=0);

	for _ in range(0, height):{
		in reverse direction:{
			knit Loops;
		}
		for i, n in enumerate(Front_Loops[0::2]):{
			rep_position = i%4;
			if rep_position == 1:{
				rightward_cable(n, n+1);
			} elif rep_position == 3:{
				leftward_cable(n, n+1);
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