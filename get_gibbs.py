#!/usr/bin/env python3
from pathlib import Path
import sys
import yaml

# TARGET_P = 350.0  
TARGET_P = float(sys.argv[1])
T_list = list(range(0, 7001, 1000))  


def read_poscar(poscar_path):
    with open(poscar_path, "r") as f:
        lines = f.readlines()

    elems = lines[5].split()
    nums = list(map(int, lines[6].split()))

    counts = {"Fe": 0, "Ni": 0, "O": 0}
    for e, n in zip(elems, nums):
        if e in counts:
            counts[e] = n

    return counts


def extract_G_at_P(dat_path, target_p):
    with open(dat_path, "r") as f:
        for line in f:
            if line.startswith("#"):
                continue
            parts = line.split()
            P = float(parts[0])
            if P == target_p: 
                G = float(parts[1])
                return G

    raise RuntimeError(f"Error: cannot find G at P = {target_p} GPa in {dat_path}")


def main():
    
    counts = read_poscar("POSCAR")
    natoms = counts["Fe"] + counts["Ni"] + counts["O"]

    free_energies = {}

    for T in T_list:
        fname =  Path(f"qha/PG/PG_{T}K.dat")
        if not fname.exists():
            raise FileNotFoundError(f"{fname} not exist")

        G_cell = extract_G_at_P(fname, TARGET_P)
        G_atom = G_cell / natoms
        free_energies[T] = G_atom

    formula = f"Fe{counts['Fe']}Ni{counts['Ni']}O{counts['O']}"

    data = {
        "Formula": formula,
        "nFe": counts["Fe"],
        "nNi": counts["Ni"],
        "nO": counts["O"],
        "P(GPa)": TARGET_P,
        "Free_energy(eV/atom)": free_energies
    }

    with open("gibbs_vs_t.yaml", "w") as f:
        yaml.dump(data, f, sort_keys=False)


if __name__ == "__main__":
    main()

