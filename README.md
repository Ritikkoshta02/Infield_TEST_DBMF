# Infield_TEST_DBMF

Digital microfluidic biochips (DMFBs) have emerged
as a transformative technology in biomedical applications, en-
abling programmable droplet manipulation for tasks such as
drug discovery, clinical diagnostics, and point-of-care testing.
Among their many advantages, DMFBs offer programmability,
flexibility in fluidic operations, and versatile droplet mobility.
However, their reliability can be compromised by factors such
as manufacturing defects, electrode degradation, or dielectric
breakdown, leading to incorrect fluidic behavior. Ensuring reli-
able operation is especially critical in safety-critical bioassays. In
prior work, SAT solvers have been employed for in-field testing to
determine optimal paths for test droplets. These droplets traverse
the chip concurrently with ongoing bioassays to verify electrode
functionality while maintaining assay integrity. Although SAT-
based methods are robust, their scalability is significantly limited
by the computational complexity associated with larger grids
and complex bioassays, resulting in prohibitive test completion
times. To overcome these challenges, we propose a reinforcement
learning (RL)-based approach for optimizing test droplet routing
in DMFBs. By leveraging RL to learn efficient and reliable
paths under predefined constraints, our method ensures rapid
and effective in-field testing without disrupting ongoing assays.
Experimental results demonstrate that the RL-based solution not
only scales efficiently to larger grids but also achieves significant
reductions in test completion time, thereby enhancing the relia-
bility and scalability of DMFB testing. This work represents a
critical step forward in ensuring the dependability of DMFBs in
real-world biomedical applications.