
import numpy as np

def weighted_rate_inversion(times,disps,cohs):
    '''
    times need to be slc dates in float years, size (numSLCs,)
    disps will be size (numIgrams,)
    cohs will also be size (numIgrams,)
    '''
    numIgrams = np.shape(disps)[0]

    # Set up covariance matrix
    # this is date-related/atmospheric noise (instead of coherence/std.dev.s/variances which are speckle/igram-related)
    noise_diags = np.ones(numIgrams)*1.0                  # ones on diagonal 
    noise_off_diags = np.ones(numIgrams-1)*(-0.5)         # -0.5 on off diagonals
    # date/atm-related noise covariance matrix
    covi = np.diag(noise_diags,0)+np.diag(noise_off_diags,-1) \
        +np.diag(noise_off_diags,1) 
    # coherence at that pixel over the interval, use this to calc variance.
    variances = (-2*np.log(cohs))                         # got this formula from Rowena's cor_sigma_test.m file 
    vars_diag = np.diag(variances,0)
    # Combine date-related and igram-related noise into proper covariance matrix 
    covi2 = covi + vars_diag                              # account for noise in individual igrams, ~speckle (not associated w/ a date, 2 igrams)
    icov = np.linalg.inv(covi2)

    # Make our G (design) matrix
    dt = np.diff(times.T)[0]
    G_disps = dt.reshape((numIgrams,1))
    
    # Now invert for the weighted displacement rate
    Gg_disps_weighted = np.linalg.inv(G_disps.T.dot(icov).dot(G_disps)).dot(G_disps.T).dot(icov)
    model_disp_rates = Gg_disps_weighted.dot(disps)       # weighted inversion directly from ints 
    disp_rate = model_disp_rates[0]                       # this just gives a velocity, no intercept 

    # now output that inverted rate
    return disp_rate
