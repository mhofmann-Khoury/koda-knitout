import cast_ons;
import bind_offs;
import random;
import needles;

left_miss = f0;
right_miss = None;
with Carrier as yarn:{
	width = (randomized_reps * 4)+ 2;
	cast_ons.alt_tuck_cast_on(width, first_needle=2, tuck_lines=1, knit_lines=0);
	in Leftward direction:{
		knit Loops;
	}
	right_miss = Front_Loops[-1] + 2;
}

used_color = False;

for _ in range(0, height):{
	to_back = [];
	to_left_first = [];
	to_right_first = [];
	to_left_second = [];
	to_right_second = [];
	tucks = [];
	right_tucked_color = [];
	colored = [];
	purls = [];
	xfer Back_Loops across to Front bed;
	color_in_row = False;
	more_tucks = [];
	for i, n in enumerate(Front_Loops[0::2]):{
		rep_position = i%2;
		n2 = n+1;
		if rep_position%2 == 1:{
			texture = random.choice(textures);
			if texture == "left_decrease":{
				to_back.append(n2);
				to_left_first.append(n2.opposite());
				tucks.append(n2);
			} elif texture == "right_decrease":{
				to_back.append(n);
				to_right_first.append(n.opposite());
				tucks.append(n);
			} elif texture == "left_cable":{
				to_back.append(n);
				to_back.append(n2);
				to_left_first.append(n2.opposite());
				to_right_second.append(n.opposite());
			} elif texture == "right_cable":{
				to_back.append(n);
				to_back.append(n2);
				to_right_first.append(n.opposite());
				to_left_second.append(n2.opposite());
			} elif texture == "colored_knit":{
				used_color = True;
				color_in_row = True;
				right_tucked_color.extend(more_tucks);
				more_tucks = [];
				colored.append(n);
				colored.append(n2);
			} elif texture == "purl":{
				purls.append(n);
				purls.append(n2);
			}
		} elif color_in_row:{
			more_tucks.append(n);
		}
	}

	left_tucked_color = [n+1 for n in right_tucked_color];

	xfer to_back across to Back Bed; // prepare cables and decreases
	xfer to_left_first 1 to Leftward to Front Bed; // left decreases and left cables
	xfer to_right_first 1 to Rightward to Front Bed; // right decreases and right cables
	xfer to_left_second 1 to Leftward to Front Bed; // finish right cables
	xfer to_right_second 1 to Rightward to Front Bed; // finish left cables

	uncolored=Loops;
	if len(colored) > 0:{
		with Carrier as color_yarn:{
			in Rightward direction:{
				knit colored;
				tuck right_tucked_color;
			}
			in Rightward direction:{
				miss right_miss;
			}
		}
		releasehook;
	}
	xfer purls across to Back Bed;
	return_purls = Last_Pass.values();
	uncolored = [l for l in Loops if l not in colored];

	with Carrier as yarn:{
		in Rightward direction:{
			tuck tucks;
			knit uncolored;
		}
		in Leftward direction:{
			knit uncolored;
			knit tucks;
		}
	}
	if len(colored) > 0:{
		xfer return_purls across to Front bed;
		with Carrier as color_yarn:{
			in Leftward direction:{
				knit colored;
				tuck left_tucked_color;
			}
			in Leftward direction:{
				miss left_miss;
			}
		}
	}



}

if bind:{
	if used_color:{
		cut color_yarn;
	}
	xfer Back_Loops across to Front Bed;
	with Carrier as yarn:{
		with Carrier as yarn:{
			in reverse direction:{
				knit Loops;
			}
			in reverse direction:{
				knit Loops;
			}
		}
		bind_offs.chain_bind_off(Loops, reverse, extra_knits=6, hold = False);
	}
}