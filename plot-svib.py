#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import yaml
import os

T_list = np.arange(2000, 4001, 1000)
cmap = plt.cm.rainbow

QHA_path = ["cdd.12-2-4", "stb.fe-hcp", "stb.fe2o-tet", "stb.ni-fcc"] 
QHA_name = ["Fe$_{12}$Ni$_2$O$_4$", "Fe$^{hcp}$", "Fe$_2$O$^{Tet.}$", "Ni$^{fcc}$"]

linestyles = ["-", "--", "-.", ":"]
linewidth  = [2.5, 1.5, 2.5, 1.5 ]
markerstyle= ['s', '+', 'o', '^']

# QHA_path = ["cdd.8-2-4", "stb.fe2o-tet", "stb.ni-fcc"]
# QHA_name = ["Fe$_{8}$Ni$_2$O$_4$", "Fe$_2$O$^{Tet.}$", "Ni$^{fcc}$"]
# 
# linestyles = ["-", "-.", "--"]   
# linewidth  = [2.5, 2.5, 2.5 ]
# markerstyle= ['s', 'o', '^']

def main():

    fig, ax = plt.subplots(figsize=(8,6))

    #================== QHA data ================#
    for path, nm, ls, lw, mk in zip(QHA_path, QHA_name, linestyles, linewidth, markerstyle):

        first_curve = True

        for T in T_list:
            filename = os.path.join(path, f"analysis/{T}.dat")
            data = np.loadtxt(filename, skiprows=1)

            P = data[:, 3]     
            Fvib = data[:, 6]     
            Svib = data[:, 7]* 1000


            color = cmap(T_list.tolist().index(T) / (len(T_list)-1))

            label = nm if first_curve else None
            first_curve = False
            ax.plot(P, Svib, linestyle=ls, marker=mk, color=color, linewidth=lw, label=label, markersize=8)

    #=============== plot ==================#
    # ax.set_xlim(280, 360)
    ax.set_ylim(0.5, 0.8)
    ax.set_xlabel("P (GPa)", fontsize=16)
    ax.set_ylabel("Svib (meV/K/atom)", fontsize=16)
    ax.tick_params(labelsize=16)
    ax.grid(True)

    norm = plt.Normalize(vmin=T_list.min(), vmax=T_list.max())
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax)
    cbar.set_label("T (K)", fontsize=16)
    cbar.ax.tick_params(labelsize=14)

    ax.legend(loc='best', ncol=2, fontsize=16)
    plt.tight_layout()
    plt.savefig("svib.png", dpi=300)
    # plt.show()


if __name__ == "__main__":
    main()

