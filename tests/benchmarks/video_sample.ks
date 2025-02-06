import cast_ons;

def make_decrease(loop):{
	xfer loop across;
	xfer Last_Pass.values() 1 to Right;
	in current direction:{
		tuck loop;
	}
}
with Carrier as yarn:{
	cast_ons.alt_tuck_cast_on(width);
	for _ in range(height):{
		for i, stitch in enumerate(Loops):{
			if i%4 == 1:{
				make_decrease(stitch);
			} else:{
				in Rightward direction:{
					knit stitch;
				}
			}
		}
		in Leftward direction:{
			knit Loops;
		}
	}
}