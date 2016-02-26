#!/usr/bin/env python2

########################################################################
### Returns the correct name for the ResearchNet levels whose names
### aren't given on SolutionNet.
def researchnet(num):
  a, b = [int(x) for x in num.split('-')]
  assert a >= 28
  idx = (a - 28) * 3 + (b - 1)
  return published[idx]
published = '''
Cyanamide
Acetic Acid
Combustion Engine
Smelting Iron
Neodymium Magnet
Carbide Swap
Fuel Production
Siliconheart Piece
Raygun Mechanism
Sulfuric Acid
Fuming Nitric Acid
Rocket Fuel
Hydroxides
Nobility
Sortite
Radiation Treatment
Boron Compounds
Photovoltaic Cells
Elementary
Mixed Acids
Squaric Acid
Misproportioned
Narkotikum
Vereinheitlichung
Haber-Bosch
Mustard Oil
Nano Electric Motor
Count
Sharing Is Caring
Reassembly
Cyanogen
Chloromethylsilane
Glyceraldehyde
Ethandiamin
Radikal
Kreisalkanol
Inorganic Pigments
Miller-Urey
Getting Pumped
Lewisite
Novichok
Ribulose
Knockout Drops
Strong Acids
Vitamin B3
1,2,3-Triphenol
1,3-Dimetoxibencene
Think in Spirals
Yellowcake
Thiourea
Downgrade
Wood Alochol
Allyl Alcohol
Propargyl Alcohol
Condensation
Silane
Phosphine
Nuclear Medicine
Oxygen Supply
Red Cross
Fluoromethanes
Exercise
Nanoboxes
'''.strip().split('\n')
