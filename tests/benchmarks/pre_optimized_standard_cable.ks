import bind_offs;
import cast_ons;
import needles;

def form_cables():{
	left_fronts = Front_Loops[7::8];
	right_backs = Front_Loops[6::8];
	left_backs = Front_Loops[3::8];
	right_fronts = Front_Loops[2::8];
	xfer left_fronts across to Back bed;
	left_fronts = Last_Pass.values();
	xfer right_fronts across to Back bed;
	right_fronts = Last_Pass.values();
	xfer left_backs across to Back bed;
	left_backs = Last_Pass.values();
	xfer right_backs across to Back bed;
	right_backs = Last_Pass.values();
	xfer left_fronts 1 to Leftward to Front bed;
	xfer right_fronts 1 to Rightward to Front bed;
	xfer left_backs 1 to Leftward to Front bed;
	xfer right_backs 1 to Rightward to Front bed;
}

with Carrier as yarn:{
	width = (cable_reps * 8)+2;
	cast_ons.alt_tuck_cast_on(width, tuck_lines=1, knit_lines=0);

	for _ in range(0, height):{
		in reverse direction:{
			knit Loops;
		}
		form_cables();
		in reverse direction:{
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