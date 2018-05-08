"""
Simplified script to generate lots of CASMO inputs, and shell file to 
run them all, and a file to produce the CMSlink-generated SIMULATE library.
"""

import numpy as np

# template files
template_nobp = open('nobp.tmpl', 'r').read()
template_ifba = open('ifba.tmpl', 'r').read()

# choose enrichments
increment = 0.25
enrichments = np.arange(2.0, 4.5+increment, increment)

# generate shell script that runs all the CASMO inputs generated
casmo_script = ''
cmslink_script = ''

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

    casmo_script += 'casmo4 -k {}\n'.format(nobp)
    casmo_script += 'casmo4 -k {}\n'.format(ifba)

    cmslink_script

f = open('run_casmo.sh', 'w')
f.write(casmo_script)
f.close()

f = open('run_cmslink.sh', 'w')
f.write(cmslink_script)
f.close()
