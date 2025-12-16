import os
import argparse


def ensemble_xyz_to_ensemble_pdb(
    pep_edit_pdb_path: str, ensemble_orca_xyz_path: str, output_dir: str
):
    os.makedirs(output_dir, exist_ok=True)
    with open(pep_edit_pdb_path, "r") as f:
        ref_pdb_lines = f.readlines()

    pdb_atom_lines = [
        i for i, l in enumerate(ref_pdb_lines) if l.startswith(("ATOM", "HETATM"))
    ]
    n_atoms = len(pdb_atom_lines)

    with open(ensemble_orca_xyz_path, "r") as f:
        xyz_lines = f.readlines()

    idx = 0
    conf_id = 0

    while idx < len(xyz_lines):
        line = xyz_lines[idx].strip()
        if not line:
            idx += 1
            continue

        nat = int(line)
        if nat != n_atoms:
            raise ValueError(
                f"Conformer {conf_id}: {nat} atoms in XYZ, " f"{n_atoms} in PDB"
            )

        coords = []
        for i in range(nat):
            parts = xyz_lines[idx + 2 + i].split()
            x, y, z = map(float, parts[1:4])
            coords.append((x, y, z))

        new_pdb = ref_pdb_lines.copy()

        for atom_i, pdb_line_idx in enumerate(pdb_atom_lines):
            x, y, z = coords[atom_i]
            line = new_pdb[pdb_line_idx]
            new_pdb[pdb_line_idx] = line[:30] + f"{x:8.3f}{y:8.3f}{z:8.3f}" + line[54:]

        out_pdb = os.path.join(output_dir, f"conf_{conf_id:06d}.pdb")

        with open(out_pdb, "w") as f:
            f.writelines(new_pdb)

        idx += 2 + nat
        conf_id += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert an ensemble of ORCA XYZ files to PDB format using a reference PDB file for topology information."
    )
    parser.add_argument(
        "pep_edit_pdb_path", type=str, help="Path to the PEP-EDIT generated PDB file."
    )
    parser.add_argument(
        "ensemble_orca_xyz_path", type=str, help="Path to the ensemble ORCA XYZ file."
    )
    parser.add_argument(
        "output_dir", type=str, help="Directory to save the output PDB files."
    )
    args = parser.parse_args()
    ensemble_xyz_to_ensemble_pdb(
        args.pep_edit_pdb_path, args.ensemble_orca_xyz_path, args.output_dir
    )
