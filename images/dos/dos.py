#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 09:56:51 2021

@author: ruben
"""


from rgpytools.orb import Orbitals
import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import os


vaccuum = Orbitals.fromOrb("/home/ruben/lammps/VACCUUM/acetoneOpt.orb")


""" VACCUUM LEVEL """
vac_s = vaccuum.getSingletEnergies()[0] # first singlet level



""" ENERGY SHIFTS """ 

# parse the energy xml file for the singlets
singletEnergies = []
for index in range(1,115):
    singletFile = f"/home/ruben/remotes/cube3/lammps/RESULTS/iter{index}.xml"
    tree2 = ET.parse(singletFile)
    root2 = tree2.getroot()
    # Extract the energies
    energiesSing = []
    failed = False
    for job in root2.findall('job'):
        if (job.find('status').text == "FAILED"):
            failed = True
            break
        energiesSing.append(float(job.find('output/E_tot').text))
    if (not failed):
        singletEnergies.append(energiesSing[1] - energiesSing[0])

singletEnergies = np.array(singletEnergies)


""" MAKING A PICTURE """
plt.close("all")

# the histogram of the data
nrOfBins = 40
limits = (3.9, 5)
plt.figure(figsize=(6,7))
n, bins, patches = plt.hist(singletEnergies, nrOfBins, limits, label='Density of states')
plt.axvline(x=vac_s, color = 'k', label="vaccuum singlet energy")
plt.legend(loc=1)
plt.title('Density of states based on 110 snap shots')
plt.xlabel('Energy (eV)')
plt.ylabel('Count')
plt.tight_layout()
plotName = "DOS_shifted.pdf"
plt.savefig(plotName, dpi=150) 
os.system(f"pdfcrop --margin 5 {plotName} {plotName}")
plt.show()
