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
cmslink_pwrm = "'MOX' 'ON' /\n'NEW' 'cms.pwr-all.lib'/\n"

for e in enrichments:
   
    sim_name_nobp = 'NOBP{0:.3f}'.format(e).replace('.', 'p')
    nobp = 'NOBP{0:.3f}'.format(e)
    f = open(nobp, 'w')
    f.write(template_nobp.format(sim_name_nobp, e))
    f.close()

    sim_name_ifba = 'IFBA{0:.3f}'.format(e).replace('.', 'p')
    ifba = 'IFBA{0:.3f}'.format(e)
    f = open(nobp, 'w')
    f.write(template_ifba.format(sim_name_ifba, e))
    f.close()

    casmo_script += 'casmo4 -k {0}.inp\n'.format(nobp)
    casmo_script += 'casmo4 -k {0}.inp\n'.format(ifba)

    cmslink_pwrm += "'CAS' '{0}.cax' '{1}'/\n'STA'/\n".format(nobp, sim_name_nobp)
    cmslink_pwrm += "'CAS' '{0}.cax' '{1}'/\n'STA'/\n".format(ifba, sim_name_ifba)
		
    cmslink_script += "cmslink cmspwrm.inp"

cmslink_pwrm += "'END'/"
	
f = open('run_casmo.sh', 'w')
f.write(casmo_script)
f.close()

f = open('cmspwrm.inp', 'w')
f.write(cmslink_pwrm)
f.close()

f = open('run_cmslink.sh', 'w')
f.write(cmslink_script)
f.close()
