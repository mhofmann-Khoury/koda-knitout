import cast_ons;
import needles;

with Carrier as c:{
	cast_ons.alt_tuck_cast_on(width, tuck_lines=2, knit_lines=0);
	releasehook;
	xfer Front_Loops[0::2] across;
	left_half = needles.direction_sorted_needles(Loops, Rightward)[0:int(width/2)];
	for _ in range(0, height, 2):{
		in Leftward direction:{
			knit Loops;
		}
		in Rightward direction:{
			knit left_half;
		}
		right_half = needles.direction_sorted_needles(Loops, Leftward)[0:int(width/2)];
		xfer right_half across;
		in Rightward direction:{
			knit Last_Pass.values();
		}
		xfer Last_Pass across;
	}
}