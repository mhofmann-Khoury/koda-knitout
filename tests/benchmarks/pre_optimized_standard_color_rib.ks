import bind_offs;
import cast_ons;
import needles;

def purl_rib(purl_direction):{
	with Carrier as yarn:{
		in purl_direction direction:{
			knit Back_Loops;
		}
	}
}

def knit_rib(knit_loops, knit_direction):{
	with Carrier as color_yarn:{
		in knit_direction direction:{
			knit knit_loops;
		}
	}
}

with Carrier as yarn:{
	width = (rib_reps*8) +2;
	cast_ons.alt_tuck_cast_on(width, tuck_lines=1, knit_lines=0);
	in Leftward direction:{
		knit Loops;
	}
	xfer Front_Loops[0::4], Front_Loops[1::4] across to Back Bed;
}

for _ in range(0, height):{
	purl_rib(reverse);
	knit_loops = Front_Loops;
	xfer Back_Loops across to Front bed;
	return_purls = Last_Pass.values();
	knit_rib(knit_loops, current);
	knit_rib(knit_loops, reverse);
	releasehook;
	xfer return_purls across to Back bed;
	purl_rib(current);
}

if bind:{
	cut color_yarn;
	with Carrier as yarn:{
		bind_offs.chain_bind_off(Loops, reverse, extra_knits=6, hold = False);
	}
}

