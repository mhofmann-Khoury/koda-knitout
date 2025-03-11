
import bind_offs;
import cast_ons;
import needles;

def form_decreases():{
	left_gaps = Front_Loops[3::8];
	right_gaps = Front_Loops[6::8];
	xfer left_gaps across to Back bed;
	left_loops = Last_Pass.values();
	tucks = list(Last_Pass.keys());
	xfer right_gaps across to Back bed;
	right_loops = Last_Pass.values();
	tucks.extend(Last_Pass.keys());
	xfer left_loops 1 to Leftward to Front bed;
	xfer right_loops 1 to Rightward to Front bed;
	return tucks;
}

with Carrier as yarn:{
	width = (lace_reps * 8)+2;
	cast_ons.alt_tuck_cast_on(width, tuck_lines=1, knit_lines=0);

	for _ in range(0, height):{
		in reverse direction:{
			knit Loops;
		}
		tucks = form_decreases();
		in reverse direction:{
			tuck tucks;
			knit Loops;
		}
	}
	in reverse direction:{
		knit Loops;
	}
	if bind:{
		bind_offs.chain_bind_off(Loops, reverse, extra_knits=6, hold = False);
	}
}