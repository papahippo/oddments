#!/usr/bin/python3
elec_norm = 0.42035 * 807
elec_dal = 0.37195 * 1340
korting = 0.05
elec_both = elec_both = (elec_norm + elec_dal) * (1.0- korting)
elec_terug = 0.05500 * (1469 + 683)
elec_vast =  0.21323 * 365
net_beheer = 0.73338 * 365
elec_total = elec_both + elec_vast - elec_terug

gas = 1.82641 * 683

jaar_verbruik = gas + elec_total
print(f"jaar_verbruik=€{jaar_verbruik} (gas=€{gas} + electric=€{elec_total})")
