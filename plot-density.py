#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import yaml
import os

T_list = np.arange(0, 7001, 1000)
cmap = plt.cm.rainbow

# indir_list = ["cdd.6-2-2", "cdd.6-3-3", "cdd.8-2-2", "cdd.8-2-4", "cdd.8-6-2", "cdd.12-2-4"]
# name = ["Fe6Ni2O2", "Fe6Ni3O3", "Fe8Ni2O2", "Fe8Ni2O4", "Fe8Ni6O2", "Fe12Ni2O4"]
# linestyles = ["-", "--", "-", "--", "-", "--"]

QHA_path = ["cdd.6-2-2", "stb.fe-hcp"]; QHA_name = ["Fe6Ni2O2", "Fe-hcp"]
# QHA_path = ["cdd.6-3-3", "stb.fe-hcp"]; QHA_name = ["Fe6Ni3O3", "Fe-hcp"]
# QHA_path = ["cdd.8-2-2", "stb.fe-hcp"]; QHA_name = ["Fe8Ni2O2", "Fe-hcp"]
# QHA_path = ["cdd.8-2-4", "stb.fe-hcp"]; QHA_name = ["Fe8Ni2O4", "Fe-hcp"]
# QHA_path = ["cdd.8-6-2", "stb.fe-hcp"]; QHA_name = ["Fe8Ni6O2", "Fe-hcp"]
# QHA_path = ["cdd.12-2-4", "stb.fe-hcp"]; QHA_name = ["Fe12Ni2O4", "Fe-hcp"]
# QHA_path = ["stb.fe2o-tet", "stb.fe-hcp"]; QHA_name = ["Fe2O-tet", "Fe-hcp"]

linestyles = ["-", "--"]   

prem_file = "/public/home/jjj/fe2o/006_cij/density/all.txt"

M = {
    "Fe": 55.845,
    "Ni": 58.693,
    "O": 15.999,
}

NA = 6.02214076e23


def load_mass_from_yaml(path):
    with open(os.path.join(path, "data/350_gpa.yaml"), "r") as f:
        d = yaml.safe_load(f)

    nFe, nNi, nO = d["nFe"], d["nNi"], d["nO"]
    mass = 0.001 * (nFe * M["Fe"] + nNi * M["Ni"] + nO * M["O"]) / NA
    return mass  # kg / cell


def main():

    fig, ax = plt.subplots(figsize=(8,6))

    #================== QHA data ================#
    for path, nm, ls in zip(QHA_path, QHA_name, linestyles):

        mass = load_mass_from_yaml(path)
        first_curve = True

        for T in T_list:
            filename = os.path.join(path, f"qha/PG/PG_{T}K.dat")
            data = np.loadtxt(filename, skiprows=1)

            P = data[:, 0]     
            V = data[:, 2]     

            V_m3 = V * 1e-30 # m3 / cell
            rho = mass / V_m3 / 1000.0 # density unit: 10^3 kg/m3

            color = cmap(T_list.tolist().index(T) / (len(T_list)-1))

            label = nm if first_curve else None
            first_curve = False
            ax.plot(P, rho, linestyle=ls, color=color, linewidth=2.5, label=label)

    #============ PREM data ===============#
    prem = np.loadtxt(prem_file, skiprows=1)
    prem_rho = prem[:,1]              # g/cm3 = 10^3 kg/m3
    prem_P   = prem[:,2]              # GPa
    ax.plot(prem_P, prem_rho, color="black", linewidth=3.0, label="PREM")

    #=============== plot ==================#
    ax.set_xlim(310, 360)
    ax.set_ylim(11.5, 14.5)
    ax.set_xlabel("Pressure (GPa)", fontsize=18)
    ax.set_ylabel("Density (10^3 kg/m3)", fontsize=18)
    ax.tick_params(labelsize=16)
    ax.grid(True)

    norm = plt.Normalize(vmin=T_list.min(), vmax=T_list.max())
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax)
    cbar.set_label("Temperature (K)", fontsize=16)
    cbar.ax.tick_params(labelsize=14)

    ax.legend(fontsize=14)
    plt.tight_layout()
    plt.savefig("rho_vs_p.png", dpi=200)
    # plt.show()


if __name__ == "__main__":
    main()

