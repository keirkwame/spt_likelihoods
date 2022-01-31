#!python3
from cosmosis.datablock import names
import numpy as np
import spt3g_2020 as spt3g

def setup(options):
    """Setup likelihood class."""
    likelihood_instance = spt3g.TEEE()
    return likelihood_instance

def execute(block, config):
    """Execute likelihood calculation for input theory TE and EE angular power spectra"""
    likelihood_instance = config

    #Fix foreground parameters (might want to vary these from block)
    fg_params = dict(
        kappa=0.0,
        Dl_Poisson_90x90=0.1,
        Dl_Poisson_90x150=0.1,
        Dl_Poisson_90x220=0.1,
        Dl_Poisson_150x150=0.1,
        Dl_Poisson_150x220=0.1,
        Dl_Poisson_220x220=0.1,
        TDust=19.6,
        ADust_TE_150=0.1647,
        BetaDust_TE=1.59,
        AlphaDust_TE=-2.42,
        ADust_EE_150=0.0236,
        BetaDust_EE=1.59,
        AlphaDust_EE=-2.42,
        mapTcal90=1.0,
        mapTcal150=1.0,
        mapTcal220=1.0,
        mapPcal90=1.0,
        mapPcal150=1.0,
        mapPcal220=1.0,
    )

    #Load theory TE and EE angular power spectra from block
    ell = block[names.cmb_cl, "ell"]
    te = block[names.cmb_cl, "te"]
    ee = block[names.cmb_cl, "ee"]

    #Fix l_min
    if ell.min() != 0:
        start_ell = np.arange(ell.min(), dtype=np.int32)
        start_cl = np.zeros(len(start_ell))
        ell = np.concatenate([start_ell, ell])
        te = np.concatenate([start_cl, te])
        ee = np.concatenate([start_cl, ee])

    #Check l_max
    if ell.max() < likelihood_instance.lmax + 1:
        raise ValueError("""
    You need to calculate the CMB spectra to ell>{} to use the SPTpol data.
    This setting can be changed in your camb/class section.""".format(likelihood_instance.lmax + 1))

    #Check have all l
    if not np.all(ell == np.arange(len(ell))):
        raise ValueError("""
    For some reason your ell values do not include all the integers - there are gaps.
    The default modules should not do this so probably you messed with something. Raise an issue if not.""")

    #Convert to D_ell
    #dl_te = te * ell * (ell + 1)
    #dl_ee = ee * ell * (ell + 1)

    #Save D_ell for test
    #np.save('ell.npy', ell)
    #np.save('dl_te.npy', te)
    #np.save('dl_ee.npy', ee)

    #Calculate log-likelihood
    log_like = likelihood_instance.loglike(te, ee, **fg_params)

    #Print log-likelihood
    print('log_like =', log_like)

    #Save log-likelihood to block
    block[names.likelihoods, "spt3g_like"] = log_like

    return 0

def cleanup(config):
    """Cleanup."""
    pass
