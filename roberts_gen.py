"""
Simplified script to generate lots of CASMO inputs.
"""

import numpy as np

# template files
template_nobp = open('nobp.tmpl', 'r').read()
template_ifba = open('ifba.tmpl', 'r').read()

# choose enrichments
increment = 0.25
enrichments = np.arange(2.0, 4.5+increment, increment)

# generate run script for running these all at once
# but not in python
run_script = ''

for e in enrichments:
   
    sim_name = 'NOBP{:.3f}'.format(e).replace('.', 'p')
    nobp = 'NOBP{:.3f}.inp'.format(e)
    f = open(nobp, 'w')
    f.write(template_nobp.format(sim_name, e))
    f.close()

    sim_name = 'IFBA{:.3f}'.format(e).replace('.', 'p')
    ifba = 'IFBA{:.3f}.inp'.format(e)
    f = open(nobp, 'w')
    f.write(template_ifba.format(sim_name, e))
    f.close()

    run_script += 'casmo4 -k {}\n'.format(nobp)
    run_script += 'casmo4 -k {}\n'.format(ifba)

f = open('run_casmo.sh', 'w')
f.write(run_script)
f.close()
