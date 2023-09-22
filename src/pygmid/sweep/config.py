import numpy as np
import json
import ast
import configparser

def matrange(start, step, stop):
    num = round((stop - start) / step + 1)
    
    return np.linspace(start, stop, num)

def toupper(option):
    return option.upper()

class Config:
    def __init__(self, config_file_path: str):
        self._configParser = configparser.ConfigParser()
        #self._configParser.optionxform = lambda option: option.upper()		
        self._configParser.optionxform = toupper
        self._configParser.read(config_file_path)
        self._config = {s:dict(self._configParser.items(s)) for s in self._configParser.sections()}
        self._parse_ranges()
        self._generate_netlist()        
        
        n = []
        p = []
        self._config['outvars'] = 	['ID','VT','IGD','IGS','GM','GMB','GDS','CGG','CGS','CSG','CGD','CDG','CGB','CDD','CSS']
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
        self._config['n'] = n		

        p.append( ['mp:ids','A',   	[-1,    0,    0,    0,    0,   0,    0,    0,    0,    0,    0,    0,    0,    0,    0  ]])
        p.append( ['mp:vth','V',   	[ 0,   -1,    0,    0,    0,   0,    0,    0,    0,    0,    0,    0,    0,    0,    0  ]])
        p.append( ['mp:igd','A',   	[ 0,    0,   -1,    0,    0,   0,    0,    0,    0,    0,    0,    0,    0,    0,    0  ]])
        p.append( ['mp:igs','A',   	[ 0,    0,    0,   -1,    0,   0,    0,    0,    0,    0,    0,    0,    0,    0,    0  ]])
        p.append( ['mp:gm','S',    	[ 0,    0,    0,    0,    1,   0,    0,    0,    0,    0,    0,    0,    0,    0,    0  ]])
        p.append( ['mp:gmbs','S',  	[ 0,    0,    0,    0,    0,   1,    0,    0,    0,    0,    0,    0,    0,    0,    0  ]])
        p.append( ['mp:gds','S',   	[ 0,    0,    0,    0,    0,   0,    1,    0,    0,    0,    0,    0,    0,    0,    0  ]])
        p.append( ['mp:cgg','F',   	[ 0,    0,    0,    0,    0,   0,    0,    1,    0,    0,    0,    0,    0,    0,    0  ]])
        p.append( ['mp:cgs','F',   	[ 0,    0,    0,    0,    0,   0,    0,    0,   -1,    0,    0,    0,    0,    0,    0  ]])
        p.append( ['mp:cgd','F',   	[ 0,    0,    0,    0,    0,   0,    0,    0,    0,    0,   -1,    0,    0,    0,    0  ]])
        p.append( ['mp:cgb','F',   	[ 0,    0,    0,    0,    0,   0,    0,    0,    0,    0,    0,    0,   -1,    0,    0  ]])
        p.append( ['mp:cdd','F',   	[ 0,    0,    0,    0,    0,   0,    0,    0,    0,    0,    0,    0,    0,    1,    0  ]])
        p.append( ['mp:cdg','F',   	[ 0,    0,    0,    0,    0,   0,    0,    0,    0,    0,    0,   -1,    0,    0,    0  ]])
        p.append( ['mp:css','F',   	[ 0,    0,    0,    0,    0,   0,    0,    0,    0,    0,    0,    0,    0,    0,    1  ]])
        p.append( ['mp:csg','F',   	[ 0,    0,    0,    0,    0,   0,    0,    0,    0,   -1,    0,    0,    0,    0,    0  ]])
        p.append( ['mp:cjd','F',   	[ 0,    0,    0,    0,    0,   0,    0,    0,    0,    0,    0,    0,    0,    1,    0  ]])
        p.append( ['mp:cjs','F',   	[ 0,    0,    0,    0,    0,   0,    0,    0,    0,    0,    0,    0,    0,    0,    1  ]])
        self._config['p'] = p	
        
        self._config['outvars_noise'] = ['STH','SFL']
        n_noise = []
        p_noise = []
        n_noise.append(['mn:id', ''])
        n_noise.append(['mn:fn', ''])
        self._config['n_noise'] = n_noise
        
        p_noise.append(['mp:id', ''])
        p_noise.append(['mp:fn', ''])
        self._config['p_noise'] = p_noise

    def __getitem__(self, key):
        if key not in self._config.keys():
            raise ValueError(f"Lookup table does not contain this data")
    
        return self._config[key]
        
    def _parse_ranges(self):
        # parse numerical ranges		
        for k in ['VGS', 'VDS', 'VSB', 'LENGTH']:
            v = ast.literal_eval(self._config['SWEEP'][k])
            v = [v] if type(v) is not list else v
            v = [matrange(*r) for r in v]
            v = [val for r in v for val in r] 
            self._config['SWEEP'][k] = v
    
        for k in ['WIDTH', 'NFING']:
            self._config['SWEEP'][k] = int(self._config['SWEEP'][k])
    
    def generate_m_dict(self):
        return {
            'INFO' : self._config['MODEL']['INFO'],
            'CORNER' : self._config['MODEL']['CORNER'],
            'TEMP' : self._config['MODEL']['TEMP'],
            'NFING' : self._config['SWEEP']['NFING'],
            'L' : np.array(self._config['SWEEP']['LENGTH']).T,
            'W' : self._config['SWEEP']['WIDTH'],
            'VGS' : np.array(self._config['SWEEP']['VGS']).T,
            'VDS' : np.array(self._config['SWEEP']['VDS']).T,
            'VSB' : np.array(self._config['SWEEP']['VSB']).T 
        }
        
    def _generate_netlist(self):
        modelfile = self._config['MODEL']['FILE']
        paramfile = self._config['MODEL']['PARAMFILE']
        width = self._config['SWEEP']['WIDTH']
        modelp = self._config['MODEL']['MODELP']
        modeln = self._config['MODEL']['MODELN']
        try:
            mn_supplement = '\n\t'.join(json.loads(self._config['MODEL']['MN']))
        except json.decoder.JSONDecodeError:
            raise "Error parsing config: make sure MN has no weird characters in it, and that the list isn't terminated with a trailing ','"
        try:
            mp_supplement = '\n\t'.join(json.loads(self._config['MODEL']['MP']))
        except json.decoder.JSONDecodeError:
            raise "Error parsing config: make sure MP has no weird characters in it, and that the list isn't terminated with a trailing ','"
        temp =int(self._config['MODEL']['TEMP'])-273
        VDS_max = max(self._config['SWEEP']['VDS'])
        VDS_step = self._config['SWEEP']['VDS'][1] - self._config['SWEEP']['VDS'][0] 
        VGS_max = max(self._config['SWEEP']['VGS'])
        VGS_step = self._config['SWEEP']['VGS'][1] - self._config['SWEEP']['VGS'][0]
    
        NFING = self._config['SWEEP']['NFING']
    
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
            f'mp (vdp vgp 0 vbp) {modelp} {mp_supplement}',
            f'\n',	 
            f'mn (vdn vgn 0 vbn) {modeln} {mn_supplement}',
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
