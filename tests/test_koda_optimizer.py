from unittest import TestCase

from koda_knitout.koda_optimizer import optimize_knitscript


class Test(TestCase):
    def test_optimize_knitscript(self):
        optimize_knitscript("half_rib_half_seed.ks", "half_rib_half_seed.k",
                            "opt_half_rib_half_seed.k", optimized_dat_name="opt_half_rib_half_seed.dat",
                            c=1, width=8, height=4)
