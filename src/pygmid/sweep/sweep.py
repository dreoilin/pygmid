import concurrent.futures
import glob
import multiprocessing as mp
import os
import pickle
import re
import shutil

import numpy as np
import psf_utils
from tqdm import tqdm

from .config import Config
from .simulator import SpectreSimulator


class Sweep:
    def __init__(self, config_file_path: str):
        self._config = Config(config_file_path)
        spectre_args = ['+escchars', 
                '=log', 
                './sweep/psf/spectre.out', 
                '-format', 
                'psfascii', 
                '-raw', 
                './sweep/psf']

        self._simulator = SpectreSimulator(*spectre_args)
    
    def run(self):
        
        Ls = self._config['SWEEP']['LENGTH']
        VSBs = self._config['SWEEP']['VSB']

        nch = self._config.generate_m_dict()
        pch = self._config.generate_m_dict()
        dimshape = (len(Ls),len(nch['VGS']),len(nch['VDS']),len(VSBs))
        for outvar in self._config['outvars']:
            nch[outvar] = np.zeros(dimshape, order='F')
            pch[outvar] = np.zeros(dimshape, order='F')

        for outvar in self._config['outvars_noise']:
            nch[outvar] = np.zeros(dimshape, order='F')
            pch[outvar] = np.zeros(dimshape, order='F')
        
        with concurrent.futures.ProcessPoolExecutor(max_workers=mp.cpu_count()) as executor:
            # A list to store futures for data parsing
            futures = []
            for i, L in enumerate(tqdm(Ls,desc="Sweeping L")):
                for j, VSB in enumerate(tqdm(VSBs, desc="Sweeping VSB", leave=False)):
                    self._write_params(length=L, sb=VSB)
                    
                    sim_path = f"./sweep/psf_{i}_{j}"
                    self._simulator.directory = sim_path
                    cp = self._simulator.run('pysweep.scs')

                    futures.append(executor.submit(self.parse_sim, *[sim_path]))
            
            concurrent.futures.wait(futures)

        for f in futures:
            i, j , n_dict, p_dict, nn_dict, pn_dict = f.result()
            for n,p in zip(self._config['n'],self._config['p']):
                params_n = n
                values_n = n_dict[params_n[0]]
                params_p = p
                values_p = p_dict[params_p[0]]
                for m, outvar in enumerate(self._config['outvars']):
                    nch[outvar][i,:,:,j] += np.squeeze(values_n*params_n[2][m])
                    pch[outvar][i,:,:,j] += np.squeeze(values_p*params_p[2][m])

            for n,p in zip(self._config['n_noise'],self._config['p_noise']):
                params_n = n
                values_n = nn_dict[params_n[0]]
                params_p = p
                values_p = pn_dict[params_p[0]]
                for m, outvar in enumerate(self._config['outvars_noise']):
                    nch[outvar][i,:,:,j] += np.squeeze(values_n)
                    pch[outvar][i,:,:,j] += np.squeeze(values_p)
        
        self._cleanup()
        # then save data to file
        modeln_file_path = f"{self._config['MODEL']['SAVEFILEN']}.pkl"
        modelp_file_path = f"{self._config['MODEL']['SAVEFILEP']}.pkl"
        with open(modeln_file_path, 'wb') as f:
            pickle.dump(nch, f)
        with open(modelp_file_path, 'wb') as f:
            pickle.dump(pch, f)
        return (modeln_file_path, modelp_file_path)
    
    def parse_sim(self, filepath):
        
        fileparts = filepath.split("_")
        i = int(fileparts[-2])
        j = int(fileparts[-1])
        
        (n_dict, p_dict) = self._extract_sweep_params(filepath)
        
        (nn_dict, pn_dict) = self._extract_sweep_params(filepath, sweep_type="NOISE")

        return i, j, n_dict, p_dict, nn_dict, pn_dict

    def _write_params(self, sb=0, length=1):
        with open('params.scs', 'w') as outfile:
            outfile.write(f"parameters length={length}\n")
            outfile.write(f"parameters sb={sb}")
    
    def _cleanup(self):
        try:
            shutil.rmtree("./sweep")
            os.remove("pysweep.scs")
            os.remove("params.scs")
        except OSError as e:
            print("Could not perform cleanup:\nFile - {e.filename}\nError - {e.strerror}")

    def _extract_number_regex(self, string):
        pattern = r'\d+'  # Matches one or more digits
        match = re.search(pattern, string)
        if match:
            return int(match.group())  # Extracted number as an integer
        else:
            return None

    def _extract_sweep_params(self, sweep_output_directory, sweep_type="DC"):
        """
        Params  -> list of strings
        size    -> len(VGS) x len(VDS)
        """
        if sweep_type == "DC":
            filename_pattern = 'sweepvds-*_sweepvgs.dc'
            params = [ k[0].split(':')[1] for k in self._config['n'] ]
        elif sweep_type == "NOISE":
            filename_pattern = 'sweepvds_noise-*_sweepvgs_noise.noise'
            params = [ k[0].split(':')[1] for k in self._config['n_noise'] ]

        file_paths = glob.glob(os.path.join(sweep_output_directory, filename_pattern))
        # remove directory in case it contains number. Only want to sort based on filename itself
        filelist = sorted([os.path.basename(f) for f in file_paths], key=self._extract_number_regex)

        nmos = {f"mn:{param}" : np.zeros((len(self._config['SWEEP']['VGS']), len(self._config['SWEEP']['VDS']))) for param in params}
        pmos = {f"mp:{param}" : np.zeros((len(self._config['SWEEP']['VGS']), len(self._config['SWEEP']['VDS']))) for param in params}
        for VDS_i, f in enumerate(filelist):
            # reconstruct path
            file_path = os.path.join(sweep_output_directory, f)
            # need to extract parameter from PSFs
            psf = psf_utils.PSF( file_path )
            
            for param in params:
                nmos[f'mn:{param}'][:,VDS_i] = (psf.get_signal(f"mn:{param}").ordinate).T
                pmos[f'mp:{param}'][:,VDS_i] = (psf.get_signal(f"mp:{param}").ordinate).T
        
        return (nmos, pmos)