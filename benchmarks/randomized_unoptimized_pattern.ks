import cast_ons;
import needles;
import random;
import bind_offs;

def send_loop_to_front(loop):{
	xfer loop across to Front bed;
	if len(Last_Pass) > 0:{
		loop= list(Last_Pass.values())[0];
	}
	return loop;
}

def send_loop_to_back(loop):{
	xfer loop across to Back bed;
	if len(Last_Pass) > 0:{
		loop= list(Last_Pass.values())[0];
	}
	return loop;
}

def rightward_cable(loop_1, loop_2):{
	loop_1 = send_loop_to_front(loop_1);
	loop_2 = send_loop_to_front(loop_2);
	xfer loop_1 across to Back bed;
	right_loop = Last_Pass.values();
	xfer loop_2 across to Back bed;
	left_loop = Last_Pass.values();
	xfer right_loop 1 to Rightward to Front bed;
	xfer left_loop 1 to Leftward to Front bed;
	with Carrier as yarn:{
		in Rightward direction:{
			knit loop_1;
			knit loop_2;
		}
	}
}

def leftward_cable(loop_1, loop_2):{
	loop_1 = send_loop_to_front(loop_1);
	loop_2 = send_loop_to_front(loop_2);
	xfer loop_1 across to Back bed;
	right_loop = Last_Pass.values();
	xfer loop_2 across to Back bed;
	left_loop = Last_Pass.values();
	xfer left_loop 1 to Leftward to Front bed;
	xfer right_loop 1 to Rightward to Front bed;
	with Carrier as yarn:{
		in Rightward direction:{
			knit loop_1;
			knit loop_2;
		}
	}

}
def purl_rib(loop_1, loop_2):{
	loop_1 = send_loop_to_back(loop_1);
	loop_2 = send_loop_to_back(loop_2);
	with Carrier as yarn:{
		in Rightward direction:{
			knit loop_1;
			knit loop_2;
		}
	}
}

def knit_rib(loop_1, loop_2):{
	loop_1 = send_loop_to_front(loop_1);
	loop_2 = send_loop_to_front(loop_2);
	with Carrier as color_yarn:{
		xfer Back_Loops across to Front bed;
		return_purls = Last_Pass.values();
		in Rightward direction:{
			knit loop_1;
			knit loop_2;
		}
		releasehook;
		xfer return_purls across to Back bed;
	}
	return [loop_1, loop_2];
}

def left_decrease(loop_1, loop_2):{
	loop_1 = send_loop_to_front(loop_1);
	loop_2 = send_loop_to_front(loop_2);
	xfer loop_2 across to Back bed;
	xfer Last_Pass.values() 1 to Leftward to Front bed;
	with Carrier as yarn:{
		in Rightward direction:{
			knit loop_1;
			tuck loop_2;
		}
	}
}
def right_decrease(loop_1, loop_2):{
	loop_1 = send_loop_to_front(loop_1);
	loop_2 = send_loop_to_front(loop_2);
	xfer loop_1 across to Back bed;
	xfer Last_Pass.values() 1 to Rightward to Front bed;
	with Carrier as yarn:{
		in Rightward direction:{
			tuck loop_1;
			knit loop_2;
		}
	}
}
def knit_two(loop_1, loop_2):{
	loop_1 = send_loop_to_front(loop_1);
	loop_2 = send_loop_to_front(loop_2);
	with Carrier as yarn:{
		in Rightward direction:{
			knit loop_1;
			knit loop_2;
		}
	}
}


with Carrier as yarn:{
	width = (randomized_reps * 4)+ 2;
	cast_ons.alt_tuck_cast_on(width, tuck_lines=1, knit_lines=0);
	in Leftward direction:{
		knit Loops;
	}
}
used_color = False;
for _ in range(0, height):{
	sorted_loops = needles.direction_sorted_needles(Loops, Rightward);
	colored_loops = [];
	for i, n in enumerate(sorted_loops[0::2]):{
		n2 = n+1;
		rep_position = i%2;
		if rep_position%2 == 0:{
			knit_two(n, n2);
		} else:{
			texture = random.choice(textures);
			if texture == "left_decrease":{
				left_decrease(n, n2);
			} elif texture == "right_decrease":{
				right_decrease(n, n2);
			} elif texture == "left_cable":{
				leftward_cable(n, n2);
			} elif texture == "right_cable":{
				rightward_cable(n, n2);
			} elif texture == "colored_knit":{
				used_color = True;
				colored_loops.append(n);
				colored_loops.append(n2);
			} elif texture == "purl":{
				purl_rib(n, n2);
			}
		}
	}
	xfer Back_Loops across to Front bed;
	un_colored_loops = Loops;
	if len(colored_loops) > 0:{
		with Carrier as color_yarn:{
			in Leftward direction:{
				knit colored_loops;
			}
			in Rightward direction:{
				knit colored_loops;
			}
		}
		releasehook;
		un_colored_loops = [l for l in Loops if l not in colored_loops];
	}
	with Carrier as yarn:{
		in Leftward direction:{
			knit un_colored_loops;
		}
	}
}
if bind:{
	if used_color:{
		cut color_yarn;
	}
	xfer Back_Loops across to Front Bed;
	with Carrier as yarn:{
		bind_offs.chain_bind_off(Loops, reverse, extra_knits=6, hold = False);
	}
}