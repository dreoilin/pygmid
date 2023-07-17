
class Config:
    def __init__(self, configfile):
        self.__config = configparser.ConfigParser()
        self.__config.optionxform = lambda option: option.upper()		
        self.__config.read(configfile)
        self.__cfgDict = {s:dict(self.__config.items(s)) for s in self.__config.sections()}
        self.__parse_ranges()
        self.__generate_netlist()

        try:
            self.__cfgDict['mn'] = json.loads(self.__cfgDict['MODEL']['MN'])
        except json.decoder.JSONDecodeError:
            raise "Error parsing config: make sure MN has no weird characters in it, and that the list isn't terminated with a trailing ','"
        
        
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
