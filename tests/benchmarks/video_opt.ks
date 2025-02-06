import cast_ons;


with Carrier as yarn:{
	cast_ons.alt_tuck_cast_on(width);
	in Leftward direction:{
		knit Loops;
	}
	for _ in range(height):{
		xfer Loops[1::4] across;
		tucks = Last_Pass.keys();
		xfer Last_Pass.values() 1 to Right;
		in Rightward direction:{
			knit Loops;
			tuck tucks;
		}
		in Leftward direction:{
			knit Loops;
		}
	}
}