import bind_offs;
import cast_ons;
import needles;

def purl_rib(loop_1, loop_2, purling_direction):{
	xfer loop_1 across to Back bed;
	if len(Last_Pass) > 0:{
		loop_1 = Last_Pass.values();
	}
	xfer loop_2 across to Back bed;
	if len(Last_Pass) > 0:{
		loop_2 = Last_Pass.values();
	}
	with Carrier as yarn:{
		in purling_direction direction:{
			knit loop_1;
			knit loop_2;
		}
	}
	return Last_Pass;
}

def knit_rib(loop_1, loop_2, knitting_direction):{
	with Carrier as color_yarn:{
		in knitting_direction direction:{
			knit loop_1;
			knit loop_2;
		}
	}
}

with Carrier as yarn:{
	width = (rib_reps*8) +2;
	cast_ons.alt_tuck_cast_on(width, tuck_lines=1, knit_lines=0);
	in Leftward direction:{
		knit Loops;
	}
}

for _ in range(0, height):{
	loops_before_course = needles.direction_sorted_needles(Loops, Rightward);
	for i, n in enumerate(loops_before_course[0::2]):{
		n2 = n+1;
		rep_position = i%2;
		if rep_position ==0:{
			purl_rib(n, n2, Rightward);
		}
	}
	xfer Back_Loops across to Front bed;
	purls = Last_Pass.values();
	knits =[];
	for i, n in enumerate(loops_before_course[0::2]):{
		n2 = n+1;
		rep_position = i%2;
		if rep_position == 1:{
			knit_rib(n, n2, Rightward);
			knits.append(n);
			knits.append(n2);
		}
	}
	knits = needles.direction_sorted_needles(knits, Leftward);
	for n in knits[0::2]:{
		n2 = n-1;
		knit_rib(n, n2, Leftward);
	}
	releasehook;
	purls = needles.direction_sorted_needles(purls, Leftward);
	for n in purls[0::2]:{
		n2 = n-1;
		purl_rib(n, n2, Leftward);
	}
}

if bind:{
	cut color_yarn;
	with Carrier as yarn:{
		bind_offs.chain_bind_off(Loops, reverse, extra_knits=6, hold = False);
	}
}
