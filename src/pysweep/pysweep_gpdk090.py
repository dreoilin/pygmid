import numpy as np
import ast
import configparser
import logging
from psf_utils import PSF
import subprocess
import sys
import shutil
import os
from subprocess import CalledProcessError
import pickle

import os
import glob
import re

def matrange(start, step, stop):
    num = round((stop - start) / step + 1)
    
    return np.linspace(start, stop, num)

class Config:
    def __init__(self, configfile):
        self.__config = configparser.ConfigParser()
        self.__config.optionxform = lambda option: option.upper()		
        self.__config.read(configfile)
        self.__cfgDict = {s:dict(self.__config.items(s)) for s in self.__config.sections()}
        self.__parse_ranges()
        self.__generate_netlist()		
        
        n = []
        p = []
        self.__cfgDict['outvars'] = 	['ID','VT','IGD','IGS','GM','GMB','GDS','CGG','CGS','CSG','CGD','CDG','CGB','CDD','CSS']
        n.append( ['mn:ids','A',   	[1,    0,   0,    0,    0,   0,    0,    0,    0,    0,    0,    0,    0,    0,    0  ]])
        n.append( ['mn:vth','V',   	[0,    1,   0,    0,    0,   0,    0,    0,    0,    0,    0,    0,    0,    0,    0  ]])
        n.append( ['mn:igd','A',   	[0,    0,   1,    0,    0,   0,    0,    0,    0,    0,    0,    0,    0,    0,    0  ]])
        n.append( ['mn:igs','A',   	[0,    0,   0,    1,    0,   0,    0,    0,    0,    0,    0,    0,    0,    0,    0  ]])
        n.append( ['mn:gm','S',    	[0,    0,   0,    0,    1,   0,    0,    0,    0,    0,    0,    0,    0,    0,    0  ]])
        n.append( ['mn:gmbs','S',  	[0,    0,   0,    0,    0,   1,    0,    0,    0,    0,    0,    0,    0,    0,    0  ]])
        n.append( ['mn:gds','S',   	[0,    0,   0,    0,    0,   0,    1,    0,    0,    0,    0,    0,    0,    0,    0  ]])
        n.append( ['mn:cgg','F',   	[0,    0,   0,    0,    0,   0,    0,    1,    0,    0,    0,    0,    0,    0,    0  ]])
        n.append( ['mn:cgs','F',   	[0,    0,   0,    0,    0,   0,    0,    0,   -1,    0,    0,    0,    0,    0,    0  ]])
        n.append( ['mn:cgd','F',   	[0,    0,   0,    0,    0,   0,    0,    0,    0,    0,   -1,    0,    0,    0,    0  ]])
        n.append( ['mn:cgb','F',   	[0,    0,   0,    0,    0,   0,    0,    0,    0,    0,    0,    0,   -1,    0,    0  ]])
        n.append( ['mn:cdd','F',   	[0,    0,   0,    0,    0,   0,    0,    0,    0,    0,    0,    0,    0,    1,    0  ]])
        n.append( ['mn:cdg','F',   	[0,    0,   0,    0,    0,   0,    0,    0,    0,    0,    0,   -1,    0,    0,    0  ]])
        n.append( ['mn:css','F',   	[0,    0,   0,    0,    0,   0,    0,    0,    0,    0,    0,    0,    0,    0,    1  ]])
        n.append( ['mn:csg','F',   	[0,    0,   0,    0,    0,   0,    0,    0,    0,   -1,    0,    0,    0,    0,    0  ]])
        n.append( ['mn:cjd','F',   	[0,    0,   0,    0,    0,   0,    0,    0,    0,    0,    0,    0,    0,    1,    0  ]])
        n.append( ['mn:cjs','F',   	[0,    0,   0,    0,    0,   0,    0,    0,    0,    0,    0,    0,    0,    0,    1  ]])
        self.__cfgDict['n'] = n		

        p.append( ['mp:ids','A',   	[1,    0,   0,    0,    0,   0,    0,    0,    0,    0,    0,    0,    0,    0,    0  ]])
        p.append( ['mp:vth','V',   	[0,    1,   0,    0,    0,   0,    0,    0,    0,    0,    0,    0,    0,    0,    0  ]])
        p.append( ['mp:igd','A',   	[0,    0,   1,    0,    0,   0,    0,    0,    0,    0,    0,    0,    0,    0,    0  ]])
        p.append( ['mp:igs','A',   	[0,    0,   0,    1,    0,   0,    0,    0,    0,    0,    0,    0,    0,    0,    0  ]])
        p.append( ['mp:gm','S',    	[0,    0,   0,    0,    1,   0,    0,    0,    0,    0,    0,    0,    0,    0,    0  ]])
        p.append( ['mp:gmbs','S',  	[0,    0,   0,    0,    0,   1,    0,    0,    0,    0,    0,    0,    0,    0,    0  ]])
        p.append( ['mp:gds','S',   	[0,    0,   0,    0,    0,   0,    1,    0,    0,    0,    0,    0,    0,    0,    0  ]])
        p.append( ['mp:cgg','F',   	[0,    0,   0,    0,    0,   0,    0,    1,    0,    0,    0,    0,    0,    0,    0  ]])
        p.append( ['mp:cgs','F',   	[0,    0,   0,    0,    0,   0,    0,    0,   -1,    0,    0,    0,    0,    0,    0  ]])
        p.append( ['mp:cgd','F',   	[0,    0,   0,    0,    0,   0,    0,    0,    0,    0,   -1,    0,    0,    0,    0  ]])
        p.append( ['mp:cgb','F',   	[0,    0,   0,    0,    0,   0,    0,    0,    0,    0,    0,    0,   -1,    0,    0  ]])
        p.append( ['mp:cdd','F',   	[0,    0,   0,    0,    0,   0,    0,    0,    0,    0,    0,    0,    0,    1,    0  ]])
        p.append( ['mp:cdg','F',   	[0,    0,   0,    0,    0,   0,    0,    0,    0,    0,    0,   -1,    0,    0,    0  ]])
        p.append( ['mp:css','F',   	[0,    0,   0,    0,    0,   0,    0,    0,    0,    0,    0,    0,    0,    0,    1  ]])
        p.append( ['mp:csg','F',   	[0,    0,   0,    0,    0,   0,    0,    0,    0,   -1,    0,    0,    0,    0,    0  ]])
        p.append( ['mp:cjd','F',   	[0,    0,   0,    0,    0,   0,    0,    0,    0,    0,    0,    0,    0,    1,    0  ]])
        p.append( ['mp:cjs','F',   	[0,    0,   0,    0,    0,   0,    0,    0,    0,    0,    0,    0,    0,    0,    1  ]])
        self.__cfgDict['p'] = p	
        
        self.__cfgDict['outvars_noise'] = ['STH','SFL']
        n_noise = []
        p_noise = []
        n_noise.append(['mn:id', ''])
        n_noise.append(['mn:fn', ''])
        self.__cfgDict['n_noise'] = n_noise
        
        p_noise.append(['mp:id', ''])
        p_noise.append(['mp:fn', ''])
        self.__cfgDict['p_noise'] = p_noise

    def __getitem__(self, key):
        if key not in self.__cfgDict.keys():
            raise ValueError(f"Lookup table does not contain this data")
    
        return self.__cfgDict[key]
        
    def __parse_ranges(self):
        # parse numerical ranges		
        for k in ['VGS', 'VDS', 'VSB', 'LENGTH']:
            v = ast.literal_eval(self.__cfgDict['SWEEP'][k])
            v = [v] if type(v) is not list else v
            v = [matrange(*r) for r in v]
            v = [val for r in v for val in r] 
            self.__cfgDict['SWEEP'][k] = v
    
        for k in ['WIDTH', 'NFING']:
            self.__cfgDict['SWEEP'][k] = int(self.__cfgDict['SWEEP'][k])
    
    def generate_m_dict(self):
        return {
            'INFO' : self.__cfgDict['MODEL']['INFO'],
            'CORNER' : self.__cfgDict['MODEL']['CORNER'],
            'TEMP' : self.__cfgDict['MODEL']['TEMP'],
            'NFING' : self.__cfgDict['SWEEP']['NFING'],
            'L' : np.array(self.__cfgDict['SWEEP']['LENGTH']).T,
            'W' : self.__cfgDict['SWEEP']['WIDTH'],
            'VGS' : np.array(self.__cfgDict['SWEEP']['VGS']).T,
            'VDS' : np.array(self.__cfgDict['SWEEP']['VDS']).T,
            'VSB' : np.array(self.__cfgDict['SWEEP']['VSB']).T 
        }
        
    def __generate_netlist(self):
        modelfile = self.__cfgDict['MODEL']['FILE']
        paramfile = self.__cfgDict['MODEL']['PARAMFILE']
        width = self.__cfgDict['SWEEP']['WIDTH']
        modelp = self.__cfgDict['MODEL']['MODELP']
        modeln = self.__cfgDict['MODEL']['MODELN']
        temp =int(self.__cfgDict['MODEL']['TEMP'])-273
        VDS_max = max(self.__cfgDict['SWEEP']['VDS'])
        VDS_step = self.__cfgDict['SWEEP']['VDS'][1] - self.__cfgDict['SWEEP']['VDS'][0] 
        VGS_max = max(self.__cfgDict['SWEEP']['VGS'])
        VGS_step = self.__cfgDict['SWEEP']['VGS'][1] - self.__cfgDict['SWEEP']['VGS'][0]
    
        NFING = self.__cfgDict['SWEEP']['NFING']
    
        netlist = (
            f"//pysweep.scs",
            f"include {modelfile}",
            f'include "{paramfile}"\n',   
            f'save mn:oppoint',  
            f'save mp:oppoint',
            f'\n',
            f'parameters gs=0.498 ds=0.2 L=length*1e-6 Wtot={width}e-6 W=500n',
            f'\n',
            f'vnoi     (vx  0)         vsource dc=0',  
            f'vdsn     (vdn vx)         vsource dc=ds',   
            f'vgsn     (vgn 0)         vsource dc=gs',   
            f'vbsn     (vbn 0)         vsource dc=-sb',  
            f'vdsp     (vdp vx)         vsource dc=-ds',  
            f'vgsp     (vgp 0)         vsource dc=-gs',  
            f'vbsp     (vbp 0)         vsource dc=sb',  
            f'\n',	 
            f'\n',	 
            f'mp (vdp vgp 0 vbp) {modelp} l=L w=Wtot m=1 simM=1\\',
            f'	ad=(((Wtot) / (1)) < 239.5n) ? ((floor((1) / 2.0) * (((((120n) - 0) + 120n) * 240n) + (((Wtot) / (1)) * 200n))) + ((((1) / 2) - floor((1) / 2) != 0) ? (((100n > (((120n) - 0) + 120n) ? 100n : (((120n) - 0) + 120n)) * 240n) + (((Wtot) / (1)) * 100n)) : 0)) / 1 : ((floor((1) / 2.0) * ((((120n) - 0) + 200n) * ((Wtot) / (1)))) + ((((1) / 2) - floor((1) / 2) != 0) ? ((200n > (((120n) - 0) + 160n) ? 200n : (((120n) - 0) + 160n)) * ((Wtot) / (1))) : 0)) / 1 \\',
            f'	as=(((Wtot) / (1)) < 239.5n) ? ((((100n > (((120n) - 0) + 120n) ? 100n : (((120n) - 0) + 120n)) * 240n) + (((Wtot) / (1)) * 100n)) + (floor(((1) - 1) / 2.0) * (((((120n) - 0) + 120n) * 240n) + (((Wtot) / (1)) * 200n))) + ((((1) / 2) - floor((1) / 2) == 0) ? (((100n > (((120n) - 0) + 120n) ? 100n : (((120n) - 0) + 120n)) * 240n) + (((Wtot) / (1)) * 100n)) : 0)) / 1 : (((200n > (((120n) - 0) + 160n) ? 200n : (((120n) - 0) + 160n)) * ((Wtot) / (1))) + (floor(((1) - 1) / 2.0) * ((((120n) - 0) + 200n) * ((Wtot) / (1)))) + ((((1) / 2) - floor((1) / 2) == 0) ? ((200n > (((120n) - 0) + 160n) ? 200n : (((120n) - 0) + 160n)) * ((Wtot) / (1))) : 0)) / 1 \\',
            f'	pd=(((Wtot) / (1)) < 239.5n) ? ((floor((1) / 2.0) * ((2 * (((120n) - 0) + 120n)) + 880n)) + ((((1) / 2) - floor((1) / 2) != 0) ? ((2 * (100n > (((120n) - 0) + 120n) ? 100n : (((120n) - 0) + 120n))) + 680n) : 0)) / 1 : ((floor((1) / 2.0) * ((2 * (((120n) - 0) + 200n)) + (2 * ((Wtot) / (1))))) + ((((1) / 2) - floor((1) / 2) != 0) ? ((2 * (200n > (((120n) - 0) + 160n) ? 200n : (((120n) - 0) + 160n))) + (2 * ((Wtot) / (1)))) : 0)) / 1 \\',
            f'	ps=(((Wtot) / (1)) < 239.5n) ? (((2 * (100n > (((120n) - 0) + 120n) ? 100n : (((120n) - 0) + 120n))) + 680n) + (floor(((1) - 1) / 2.0) * ((2 * (((120n) - 0) + 120n)) + 880n)) + ((((1) / 2) - floor((1) / 2) == 0) ? ((2 * (100n > (((120n) - 0) + 120n) ? 100n : (((120n) - 0) + 120n))) + 680n) : 0)) / 1 : (((2 * (200n > (((120n) - 0) + 160n) ? 200n : (((120n) - 0) + 160n))) + (2 * ((Wtot) / (1)))) + (floor(((1) - 1) / 2.0) * ((2 * (((120n) - 0) + 200n)) + (2 * ((Wtot) / (1))))) + ((((1) / 2) - floor((1) / 2) == 0) ? ((2 * (200n > (((120n) - 0) + 160n) ? 200n : (((120n) - 0) + 160n))) + (2 * ((Wtot) / (1)))) : 0)) / 1 \\',
            f'\n',	 
            f'mn (vdn vgn 0 vbn) {modeln} l=L w=Wtot m=1 simM=1 \\',
            f'	ad=(((Wtot) / (1)) < 239.5n) ? ((floor((1) / 2.0) * (((((120n) - 0) + 120n) * 240n) + (((Wtot) / (1)) * 200n))) + ((((1) / 2) - floor((1) / 2) != 0) ? (((100n > (((120n) - 0) + 120n) ? 100n : (((120n) - 0) + 120n)) * 240n) + (((Wtot) / (1)) * 100n)) : 0)) / 1 : ((floor((1) / 2.0) * ((((120n) - 0) + 200n) * ((Wtot) / (1)))) + ((((1) / 2) - floor((1) / 2) != 0) ? ((200n > (((120n) - 0) + 160n) ? 200n : (((120n) - 0) + 160n)) * ((Wtot) / (1))) : 0)) / 1 \\',
            f'	as=(((Wtot) / (1)) < 239.5n) ? ((((100n > (((120n) - 0) + 120n) ? 100n : (((120n) - 0) + 120n)) * 240n) + (((Wtot) / (1)) * 100n)) + (floor(((1) - 1) / 2.0) * (((((120n) - 0) + 120n) * 240n) + (((Wtot) / (1)) * 200n))) + ((((1) / 2) - floor((1) / 2) == 0) ? (((100n > (((120n) - 0) + 120n) ? 100n : (((120n) - 0) + 120n)) * 240n) + (((Wtot) / (1)) * 100n)) : 0)) / 1 : (((200n > (((120n) - 0) + 160n) ? 200n : (((120n) - 0) + 160n)) * ((Wtot) / (1))) + (floor(((1) - 1) / 2.0) * ((((120n) - 0) + 200n) * ((Wtot) / (1)))) + ((((1) / 2) - floor((1) / 2) == 0) ? ((200n > (((120n) - 0) + 160n) ? 200n : (((120n) - 0) + 160n)) * ((Wtot) / (1))) : 0)) / 1 \\',
            f'	pd=(((Wtot) / (1)) < 239.5n) ? ((floor((1) / 2.0) * ((2 * (((120n) - 0) + 120n)) + 880n)) + ((((1) / 2) - floor((1) / 2) != 0) ? ((2 * (100n > (((120n) - 0) + 120n) ? 100n : (((120n) - 0) + 120n))) + 680n) : 0)) / 1 : ((floor((1) / 2.0) * ((2 * (((120n) - 0) + 200n)) + (2 * ((Wtot) / (1))))) + ((((1) / 2) - floor((1) / 2) != 0) ? ((2 * (200n > (((120n) - 0) + 160n) ? 200n : (((120n) - 0) + 160n))) + (2 * ((Wtot) / (1)))) : 0)) / 1 \\',
            f'	ps=(((Wtot) / (1)) < 239.5n) ? (((2 * (100n > (((120n) - 0) + 120n) ? 100n : (((120n) - 0) + 120n))) + 680n) + (floor(((1) - 1) / 2.0) * ((2 * (((120n) - 0) + 120n)) + 880n)) + ((((1) / 2) - floor((1) / 2) == 0) ? ((2 * (100n > (((120n) - 0) + 120n) ? 100n : (((120n) - 0) + 120n))) + 680n) : 0)) / 1 : (((2 * (200n > (((120n) - 0) + 160n) ? 200n : (((120n) - 0) + 160n))) + (2 * ((Wtot) / (1)))) + (floor(((1) - 1) / 2.0) * ((2 * (((120n) - 0) + 200n)) + (2 * ((Wtot) / (1))))) + ((((1) / 2) - floor((1) / 2) == 0) ? ((2 * (200n > (((120n) - 0) + 160n) ? 200n : (((120n) - 0) + 160n))) + (2 * ((Wtot) / (1)))) : 0)) / 1 \\', 
            f'\n',	 
            f'simulatorOptions options gmin=1e-13 reltol=1e-4 vabstol=1e-6 iabstol=1e-10 temp={temp} tnom=27',  
            f'sweepvds sweep param=ds start=0 stop={VDS_max} step={VDS_step} {{',  
            f'sweepvgs dc param=gs start=0 stop={VGS_max} step={VGS_step}',  
            f'}}', 
            f'sweepvds_noise sweep param=ds start=0 stop={VDS_max} step={VDS_step} {{', 
            f'	sweepvgs_noise noise freq=1 oprobe=vnoi param=gs start=0 stop={VGS_max} step={VGS_step}', 
            f'}}'
            )
        with open('pysweep.scs', 'w') as outfile:
            outfile.write('\n'.join(netlist))
    
class Spectre:
    def __init__(self, *args):
        self.__args = args
    
    def run(self, filename):
        infile = filename
        try:
            cmd_args = ['spectre', filename] + [*self.__args]
            cp = subprocess.run(cmd_args, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except CalledProcessError as e:
            logging.info(f"Error executing process\n\n{e}")
            return
        logging.info(cp.stdout)

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

        self.__simulator = Spectre(*spectre_args)
    
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

        for i, L in enumerate(Ls):
            print(f"L={L}")
            for j, VSB in enumerate(VSBs):
                self.__write_params(length=L, sb=VSB)
                         
                self.__simulator.run('pysweep.scs')

                params = [ k[0].split(':')[1] for k in self.__cfg['n'] ]

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
            # need to extract parameter from PSFs
            psf = PSF( file_path )
            
            for param in params:
                # nmos first
                nmos[f'mn:{param}'].append( (psf.get_signal(f"mn:{param}").ordinate).T )
                # pmos next
                pmos[f'mp:{param}'].append( (psf.get_signal(f"mp:{param}").ordinate).T )
                
        nmos = { k:np.stack(v).T for k,v in nmos.items() }
        pmos = { k:np.stack(v).T for k,v in pmos.items() }

        return (nmos, pmos)

configfile = str(sys.argv[1])
swp = Sweep(configfile)
swp.run()





    
