# add the location to NRM
# (assumes the repo is checked out to /home/robertsj/Research/nrm

import sys
sys.path.append('/home/robertsj/Research/nrm')
sys.path.append('/home/robertsj/Research/nrm/examples/casmo4_examples')

# This example computes cycle lengths for 
# various enrichments

import numpy as np
from scipy.optimize import fsolve
import pickle 
import time
import matplotlib.pyplot as plt
from nrm import NRM
from casmo4_model import CASMO4
from nrm.default_models import k_cladding, k_fuel, h_gap

def run_problem():
    # parameter dictionary
    p = {}                 
    p['number_batches'] = 3       
    p['leakage_penalty'] = 0.04
    p['assembly_width'] = 21.5036
    p['assembly_power'] = 3.4/193
    p['active_height'] = 366.0
    p['pin_pitch'] = 1.2598
    p['fuel_radius'] = 0.4096
    p['cladding_inner_radius'] = 0.4180
    p['cladding_outer_radius'] = 0.4750
    p['number_pins'] = 264
    p['power_share'] = 'reactivity'
    p['T_F0'] = 900.0 # nominal fuel temperature (K)
    p['T_C0'] = 580.0 # nominal coolant temperatur (K)
    p['C_B0'] = 900.0 # nominal boron concentration (ppm)

    T_F = p['T_F0']*np.ones(p['number_batches']) # batch fuel temperatures (K)
    T_C = p['T_C0']*np.ones(p['number_batches']) # batch moderator temperatures (K)


    enrich = np.array([2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0])
    num_enrich = len(enrich)
    B_c_equal = np.zeros(num_enrich)
    B_c_reactivity = np.zeros(num_enrich)

    for i in range(num_enrich):
        
        # Set enrichment
        p['enrichment'] = enrich[i]

        # Make model
        c = CASMO4(p, degree=2, run=True)
        
        # Make solver
        solver = NRM(p, rho=c.rho, m2=c.m2, tolerance=0.000001)
        
        te = time.time()
        
        print('enrichment = {:.2f}%'.format(enrich[i]))
        
        p['power_share'] = 'equal'
        B, ppf, T_F, T_C = solver.solve(T_F, T_C)
        B_c_equal[i] = B[-1]/p['number_batches']
            
        p['power_share'] = 'reactivity'
        B, ppf, T_F, T_C = solver.solve(T_F, T_C)
        B_c_reactivity[i] = B[-1]/p['number_batches']
        
        te = time.time() - te
        
        print("elapsed time: {:.3f} seconds".format(te))
        
        pickle.dump({'enrich': enrich, 
                     'B_c_equal': B_c_equal, 
                     'B_c_reactivity': B_c_reactivity}, 
                    open('example_1.p', 'wb'))

def process_data():
    d = pickle.load(open('example_1.p', 'rb'))
    e = d['enrich']
    be = d['B_c_equal']
    br = d['B_c_reactivity']
    plt.plot(e, be, 'k', e, br, 'r--')
    plt.legend(['equal', 'reactivity'])
    plt.xlabel('enrichment')
    plt.ylabel('cycle length (GWd/t)')
    plt.show()

    # fit reactivity to a polynomial, and then use fsolve to figure out 
    # what the target enrichment is
    f_e = lambda x: np.polyval(np.polyfit(e, be, 4), x) - 18.0
    f_r = lambda x: np.polyval(np.polyfit(e, br, 4), x) - 18.0

    print('based on flat powers, we need enrichment of {:.3f}%'.format(fsolve(f_e, 4.5)[0]))
    print('based on reactivity-weighted powers, we need enrichment of {:.3f}%'.format(fsolve(f_r, 4.5)[0]))

if __name__ == '__main__':
    
    # run_problem()
    process_data()
