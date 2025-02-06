from knit_script.interpret_knit_script import knit_script_to_knitout_to_dat

knit_script_to_knitout_to_dat("video_sample.ks", "video_sample.k", "video_sample.dat", pattern_is_filename=True,
                              yarn=3, width=60, height=60)

knit_script_to_knitout_to_dat("video_opt.ks", "video_opt.k", "video_opt.dat", pattern_is_filename=True,
                              yarn=3, width=60, height=60)
