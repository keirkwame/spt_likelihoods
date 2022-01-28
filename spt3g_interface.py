#!python3
from cosmosis.datablock import names
import spt3g_2020 as spt3g

def setup(options):
    """Setup likelihood class."""
    likelihood_instance = spt3g.TEEE()
    return likelihood_instance

def execute(block, config):
    """Execute likelihood calculation for input theory TE and EE angular power spectra"""
    likelihood_instance = config

    #Load theory TE and EE angular power spectra from block
    ell = block[names.cmb_cl, "ell"]
    te = block[names.cmb_cl, "te"]
    ee = block[names.cmb_cl, "ee"]

    #Convert to D_ell
    dl_te = te * ell * (ell + 1)
    dl_ee = ee * ell * (ell + 1)
