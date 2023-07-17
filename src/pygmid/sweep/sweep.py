from .config import Config
from .simulator import SpectreSimulator

class Sweep:
    def __init__(self, configfile: str):
        self.__cfg = Config(configfile)
        spectre_args = ['+escchars', 
                '=log', 
                './sweep/psf/spectre.out', 
                '-format', 
                'psfascii', 
                '-raw', 
                './sweep/psf']

        self.__simulator = SpectreSimulator(*spectre_args)
    
    def run(self):
        Ls = self.__cfg['SWEEP']['LENGTH']
        VSBs = self.__cfg['SWEEP']['VSB']
        nch = self.__cfg.generate_m_dict()
        pch = self.__cfg.generate_m_dict()
        dimshape = (len(Ls),len(nch['VGS']),len(nch['VDS']),len(VSBs))
        for outvar in self.__cfg['outvars']:
            nch[outvar] = np.zeros(dimshape, order='F')
            pch[outvar] = np.zeros(dimshape, order='F')

        for outvar in self.__cfg['outvars_noise']:
            nch[outvar] = np.zeros(dimshape, order='F')
            pch[outvar] = np.zeros(dimshape, order='F')

        # TODO: every time a simulation thread completes add a parsing thread to the queue
        # Have a look at the multiprocessing package
        for i, L in enumerate(Ls):
            print(f"L={L}")
            for j, VSB in enumerate(VSBs):
                self.__write_params(length=L, sb=VSB)
                
                self.__simulator.run('pysweep.scs')

                params = [ k[0].split(':')[1] for k in self.__cfg['n'] ]

                # TODO: parallelise the below file parsing
                (n_dict, p_dict) = self.__extract_sweep_params(params)

                for n,p in zip(self.__cfg['n'],self.__cfg['p']):
                    params_n = n
                    values_n = n_dict[params_n[0]]
                    params_p = p
                    values_p = p_dict[params_p[0]]
                    for m, outvar in enumerate(self.__cfg['outvars']):
                        nch[outvar][i,:,:,j] = np.squeeze(nch[outvar][i,:,:,j] + values_n*params_n[2][m])
                        pch[outvar][i,:,:,j] = np.squeeze(pch[outvar][i,:,:,j] + values_p*params_p[2][m])
                
                params = [ k[0].split(':')[1] for k in self.__cfg['n_noise'] ]
                
                (n_dict, p_dict) = self.__extract_sweep_params(params, sweep_type="NOISE")

                for n,p in zip(self.__cfg['n_noise'],self.__cfg['p_noise']):
                    params_n = n
                    values_n = n_dict[params_n[0]]
                    params_p = p
                    values_p = p_dict[params_p[0]]
                    for m, outvar in enumerate(self.__cfg['outvars_noise']):
                        nch[outvar][i,:,:,j] += np.squeeze(values_n)
                        pch[outvar][i,:,:,j] += np.squeeze(values_p)

                # TODO: uncomment this and clean the temporary files up from the runs
                # self.__cleanup()

        # save data to file
        with open(f"{self.__cfg['MODEL']['SAVEFILEN']}.pkl", 'wb') as f:
            pickle.dump(nch, f)
        with open(f"{self.__cfg['MODEL']['SAVEFILEP']}.pkl", 'wb') as f:
            pickle.dump(pch, f)
    
    def __write_params(self, sb=0, length=1):
        with open('params.scs', 'w') as outfile:
            outfile.write(f"parameters length={length}\n")
            outfile.write(f"parameters sb={sb}")
    
    def __cleanup(self):
        try:
            shutil.rmtree("./sweep")
        except OSError as e:
            print("Could not perform cleanup:\nFile - {e.filename}\nError - {e.strerror}")

    def __extract_number_regex(self, string):
        pattern = r'\d+'  # Matches one or more digits
        match = re.search(pattern, string)
        if match:
            return int(match.group())  # Extracted number as an integer
        else:
            return None

    def __extract_sweep_params(self, params, sweep_type="DC"):
        """
        Params  -> list of strings
        size    -> len(VGS) x len(VDS)
        """
        # directory should be taken from config file, but could be hardcoded ?
        directory = f"./sweep/psf"
        # filename pattern should be taken from config file, but could also be hardcoded ?
        if sweep_type == "DC":
            filename_pattern = 'sweepvds-*_sweepvgs.dc'
        elif sweep_type == "NOISE":
            filename_pattern = 'sweepvds_noise-*_sweepvgs_noise.noise'

        file_paths = glob.glob(os.path.join(directory, filename_pattern))
        # remove directory in case it contains number. Only want to sort based on filename itself
        filelist = sorted([os.path.basename(f) for f in file_paths], key=self.__extract_number_regex)
        # psf = PSF( os.path.join(directory, filelist[0]) , use_cache=False, update_cache=False)
        
        nmos = {f"mn:{param}" : [] for param in params}
        pmos = {f"mp:{param}" : [] for param in params}
        for i, f in enumerate(filelist):
            # reconstruct path
            file_path = os.path.join(directory, f)
            # TODO: try out libpsf
            # need to extract parameter from PSFs
            psf = PSF( file_path )
            
            for param in params:
                # TODO: set these arrays to be the correct length and not use .append
                # nmos first
                nmos[f'mn:{param}'].append( (psf.get_signal(f"mn:{param}").ordinate).T )
                # pmos next
                pmos[f'mp:{param}'].append( (psf.get_signal(f"mp:{param}").ordinate).T )
                
        nmos = { k:np.stack(v).T for k,v in nmos.items() }
        pmos = { k:np.stack(v).T for k,v in pmos.items() }

        return (nmos, pmos)