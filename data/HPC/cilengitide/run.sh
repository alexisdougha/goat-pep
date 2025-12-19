#!/bin/bash

#SBATCH -A antioxydant 
#SBATCH -p ipop-up 
#SBATCH --ntasks=8 
#SBATCH -o cilengitide_log.out
#SBATCH -e cilengitide_log.err
#SBATCH --job-name=cilengitide
#SBATCH --mem=250GB
#SBATCH --nodelist=cpu-node142

export PATH=/shared/projects/antioxydant/openmpi_conda/bin:$PATH
export LD_LIBRARY_PATH=/shared/projects/antioxydant/openmpi_conda/lib:$LD_LIBRARY_PATH

/shared/projects/antioxydant/orca_folder_AMcs/orca /shared/projects/antioxydant/pep_edit/goat/cilengitide/cilengitide.inp > /shared/projects/antioxydant/pep_edit/goat/cilengitide/cilengitide.log
