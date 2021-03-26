import os
import tempfile
import unittest

import numpy as np

packages_path = os.environ.get("COBAYA_PACKAGES_PATH") or os.path.join(
    tempfile.gettempdir(), "SPT_packages"
)


class SPTPolLiteTest(unittest.TestCase):
    def setUp(self):
        from cobaya.install import install

        install({"likelihood": {"spt.SPTPol": None}}, path=packages_path)

    def test_cobaya(self):
        """Test the Cobaya interface to the SPTPol likelihood."""
        from cobaya.model import get_model

        cosmo_params = dict(
            cosmomc_theta=0.010411,
            As=1e-10 * np.exp(3.1),
            ombh2=0.0221,
            omch2=0.1200,
            ns=0.96,
            Alens=1.0,
            tau=0.09,
        )

        fg_params = dict(
            kappa=0.0,
            czero_psTE_150=0.0,
            czero_psEE_150=0.0837416,
            ADust_TE=0.1647,
            ADust_EE=0.0236,
            alphaDust_TE=-2.42,
            alphaDust_EE=-2.42,
            mapTcal=1.0,
            mapPcal=1.0,
            beam1=0.0,
            beam2=0.0,
        )

        info = {
            "debug": True,
            "likelihood": {"spt.SPTPol": None},
            "theory": {"camb": {"extra_args": {"lens_potential_accuracy": 1}}},
            "params": {**cosmo_params, **fg_params},
            "modules": packages_path,
        }

        for use_cl, expected_chi2 in {
            ("te", "ee"): 162.98103875445057,
            ("te",): 74.72963434194682,
            ("ee",): 76.80106189735758,
        }.items():
            info["likelihood"]["spt.SPTPol"] = dict(use_cl=list(use_cl))
            model = get_model(info)
            chi2 = -2 * model.loglike({})[0]
            self.assertAlmostEqual(chi2, expected_chi2, 3)


if __name__ == "__main__":
    unittest.main()
