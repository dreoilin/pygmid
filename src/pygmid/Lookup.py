import copy

import numpy as np
import scipy.io
from scipy.interpolate import interpn
import pickle

from .constants import eps
from .numerical import interp1

class Lookup:
    def __init__(self, filename="MOS.mat", **kwargs):
        self.__setup(filename, **kwargs)
        self.__modefuncmap = {1 : self._SimpleLK,
                              2 : self._SimpleLK,  
                              3 : self._RatioVRatioLK}

    def __setup(self, filename, **kwargs):
        """
        Setup the Lookup object

        Assigns loaded data and defaults
        to the DATA member variable

        Args:
            filename
        Kwargs:
            Keyword arguments can be used to
            set default values for the lookup
            function. METHOD sets the method
            used for interpolation at the end of lookup
            mode 3. pchip by default
        """
        data = self.__load(filename)
        if data is not None:
            self.__DATA = data
        else:
            raise RuntimeError(f"Data could not be loaded from {filename}")

        kwargs = {k.upper(): v for k, v in kwargs.items()} # convert kwargs to upper
        self.__default = {
            'L'     :   kwargs.get('L', min(self.__DATA['L'])),
            'VGS'   :   kwargs.get('VGS', self.__DATA['VGS']),
            'VDS'   :   kwargs.get('VDS', max(self.__DATA['VDS'])/2),
            'VSB'   :   kwargs.get('VSB', 0.0),
            'METHOD':   kwargs.get('METHOD', 'pchip'),
            'VGB'   :   kwargs.get('VGB', None),
            'GM_ID' :   kwargs.get('GM_ID', None),
            'ID_W'  :   kwargs.get('ID_W', None),
            'VDB'   :   kwargs.get('VDB', None)
        }

    def __load(self, filename):
        """
        Function to load data from file

        Loads array data from file. Currently supports .mat files only.
        .mat is parsed to convert MATLAB cell data into a dictionary of
        arrays. Data is loaded from value with first non-header key. 
        Python interprets MATLAB cell structures as 1-D nests. Nested 
        data is accessed and deep copied to member DATA variable

        Args:
            filename

        Returns:
            First MATLAB variable encountered in file as data
        """
        if filename.endswith('.mat'):
            # parse .mat file into dict object
            mat = scipy.io.loadmat(filename, matlab_compatible=True)

            for k in mat.keys():
                if not( k.startswith('__') and k.endswith('__') ):
                    mat = mat[k]
                    data = {k.upper():copy.deepcopy(np.squeeze(mat[k][0][0])) for k in mat.dtype.names}
                    return data   
        
        elif filename.endswith('.pkl'):
            with open(filename, 'rb') as f:
                data = pickle.load(f)
                return data

        # !TODO add functionality to load other data structures
        return None

    def __contains__(self, key):
        return key in self.__DATA.keys()

    def __getitem__(self, key):
        """
        __getitem__ dunder method overwritten to allow convenient
        pseudo array access to member data. Returns a copy of the
        member array.
        """
        if key not in self:
            raise ValueError(f"Lookup table does not contain this data")

        return np.copy(self.__DATA[key])

    def _modeset(self, outkey, varkey):
        """
        Function to set lookup mode
            MODE1: output is single variable, variable arg is single
            MODE2: output is ratio, variable arg is single
            MODE3: output is ratio, variable arg is ratio

        Args:
            outkey: keywords (list) of output argument
            varkey: keywords (list) of variable argument

        Returns:
            mode (integer). Error if invalid mode selected
        """
        out_ratio = isinstance(outkey, list) and len(outkey) > 1
        var_ratio = isinstance(varkey, list) and len(varkey) > 1
        if out_ratio and var_ratio:
            mode = 3
        elif out_ratio and (not var_ratio):
            mode = 2
        elif (not out_ratio) and (not var_ratio):
            mode = 1
        else:
            raise ValueError("Invalid syntax or usage mode! Please check documentation.")
        
        return mode

    def lookup(self, out, **kwargs):
        """
        Alias for look_up() function
        """
        return self.look_up(out, **kwargs)

    def look_up(self, out, **kwargs):
        """
        Entry method for lookup functionality

        Sanitises input. Extracts the variable key as first key value pair
        in kwargs dict. Both the outkey and varkey are converted to lists.
        String is split based on _ character.

        Mode is determined and appropriate lookup function is called from
        modefuncmap dict

        Args:
            out: desired variable to be interpolated 'GM', 'ID' etc
            kwargs: keyword arguments (dict). First key-value pair is
                    variable argument

        Returns:
            y: interpolated data, [] if erroneous mode selected
        """
        outkeys = out.upper().split('_')
        varkeys, vararg = next(iter((kwargs.items()))) if kwargs else (None, None)
        varkeys = str(varkeys).upper().split('_')

        kwargs = {k.upper(): v for k, v in kwargs.items()} # convert kwargs to upper
        defaultdict = {k:self.__default.get(k) for k in ['L', 'VGS', 'VDS', 'VSB', 'METHOD']}
        pars = {k:kwargs.get(k, v) for k, v in defaultdict.items()} # extracts parameters from kwargs
        
        # common kwargs for interpolating functions
        ipkwargs = {'bounds_error': False,
                    'fill_value' : None}

        try:
            mode = self._modeset(outkeys, varkeys)
        except:
            return []
        # appropriate lookup function is called with modefuncmap dict
        y = self.__modefuncmap.get(mode) (outkeys, varkeys, vararg, pars, **ipkwargs)
        
        return y

    def _SimpleLK(self, outkeys, varkeys, vararg, pars, **ipkwargs):
        """
        Lookup for Modes 1 and 2

        Args:
            outkeys: list of keys for desired output e.g ['GM', 'ID'] for 'GM_ID'
            varkeys: unused
            pars: dict containing L, VGS, VDS and VSB data
        Output:
            output: interpolated data specified by outkeys Squeezed to remove extra
                    dimensions
        """

        if len(outkeys) > 1:
            num, den = outkeys
            with np.errstate(divide='ignore',invalid='ignore'):
                ydata =  self.__DATA[num]/self.__DATA[den]
                # nan causing issues with interpn extrapolation
                ydata[np.isnan(ydata)] = 0.0
        else:
            outkey = outkeys[0]
            ydata = self.__DATA[outkey]

        points = (self.__DATA['L'], self.__DATA['VGS'], self.__DATA['VDS'],\
            self.__DATA['VSB'])
        xi_mesh = np.array(np.meshgrid(pars['L'], pars['VGS'], pars['VDS'], pars['VSB'], indexing='ij'))
        xi = np.rollaxis(xi_mesh, 0, 5)
        xi = xi.reshape(int(xi_mesh.size/4), 4)

        output = interpn(points, ydata, xi, **ipkwargs).reshape(len(np.atleast_1d(pars['L'])), \
            len(np.atleast_1d(pars['VGS'])), len(np.atleast_1d(pars['VDS'])),\
                 len(np.atleast_1d(pars['VSB'])) )
        
        # remove extra dimensions
        output = np.squeeze(output)

        return output

    def _RatioVRatioLK(self, outkeys, varkeys, vararg, pars, **ipkwargs):
        """
        Lookup for Mode 3

        Args:
            outkeys: list of keys for desired output e.g ['GM', 'ID'] for 'GM_ID'
            varkeys: list of keys for ratio input e.g ['GM', 'ID'] for 'GM_ID'
            pars: dict containing L, VGS, VDS and VSB data
        Output:
            output: interpolated data specified by outkeys. Squeezed to remove extra
                    dimensions
        """
        with np.errstate(divide='ignore',invalid='ignore'):    
            # unpack outkeys and ydata
            num, den = outkeys
            ydata =  self.__DATA[num]/self.__DATA[den]
            ydata[np.isnan(ydata)] = 0.0
            # unpack varkeys and xdata
            num, den = varkeys
            xdata = self.__DATA[num]/self.__DATA[den]
            xdata[np.isnan(xdata)] = 0.0

        xdesired = np.atleast_1d(vararg)
        
        points = (self.__DATA['L'], self.__DATA['VGS'], self.__DATA['VDS'],\
            self.__DATA['VSB'])
        xi_mesh = np.array(np.meshgrid(pars['L'], pars['VGS'], pars['VDS'], pars['VSB'], indexing='ij'))
        xi = np.rollaxis(xi_mesh, 0, 5)
        xi = xi.reshape(int(xi_mesh.size/4), 4)

        x = interpn(points, xdata, xi, **ipkwargs).reshape(len(np.atleast_1d(pars['L'])), \
            len(np.atleast_1d(pars['VGS'])), len(np.atleast_1d(pars['VDS'])),\
                 len(np.atleast_1d(pars['VSB'])))
        
        y = interpn(points, ydata, xi, **ipkwargs).reshape(len(np.atleast_1d(pars['L'])), \
            len(np.atleast_1d(pars['VGS'])), len(np.atleast_1d(pars['VDS'])),\
                 len(np.atleast_1d(pars['VSB'])))
        
        x = np.array(np.squeeze(np.transpose(x, (1, 0, 2, 3))))
        y = np.array(np.squeeze(np.transpose(y, (1, 0, 2, 3))))
        
        if x.ndim == 1:
            x.shape += (1,)
            y.shape += (1,)

        dim = x.shape
        output = np.zeros((dim[1], len(xdesired)))
        ipkwargs = {
            'kind' : pars['METHOD'],
            'fill_value' : np.NaN
        }
        
        for i in range(0, dim[1]):
            for j in range(0, len(xdesired)):
                m = max(x[:, i])
                idx = np.argmax(x[:, i])
                if (xdesired[j] > m):
                    print(f'Look up warning: {num}_{den} input larger than maximum! Output is NaN')
                if (num.upper() == 'GM') and (den.upper() == 'ID'):
                    x_right = x[idx:-1, i]
                    y_right = y[idx:-1, i]
                    output[i, j] = interp1(x_right, y_right, **ipkwargs)(xdesired[j])
                elif (num.upper() == 'GM') and (den.upper() == 'CGG') or (den.upper() == 'CGG'):
                    x_left = x[:idx, i]
                    y_left = y[:idx, i]
                    output[i, j] = interp1(x_left, y_left, **ipkwargs)(xdesired[j])
                else:
                    crossings = len(np.argwhere(np.diff(np.sign(x[:,i]-xdesired[j]+eps))))
                    if crossings > 1:
                        print('Crossing warning')
                        return []
                    output[i, j] = interp1(x[:,i], y[:, i], **ipkwargs)(xdesired[j])

        output = np.squeeze(output)

        return output

    def lookupVGS(self, **kwargs):
        return self.look_upVGS(**kwargs)

    def look_upVGS(self, **kwargs):
        """
        Companion function to "look_up." Finds transistor VGS for a given inversion level (GM_ID)
        or current density (ID/W) and given terminal voltages. 
        The function interpolates (linear only) when the requested points lie off the simulation grid
        
        There are two basic usage scenarios:
        (1) Lookup VGS with known voltage at the source terminal
        (2) Lookup VGS with unknown source voltage, e.g. when the source of the
        transistor is the tail node of a differential pair
        
        At most one of the input arguments can be a vector; the other must be
        scalars.
        
        Examples of usage modes are given in test_lookupVGS.py
        
        Args:
            pars: dict containing L, VGB, GM_ID and ID_W, VDS, VSB and METHOD
        Output:
            output: 1-d numpy array
        """
        kwargs = {k.upper(): v for k, v in kwargs.items()} # convert kwargs to upper
        defaultdict = {k:self.__default.get(k) for k in ['L', 'VDS', 'VDB', 'VGB', 'GM_ID', 'ID_W', 'VSB', 'METHOD']}
        pars = {k:kwargs.get(k, v) for k,v in defaultdict.items()}

        #Check whether GM_ID or ID_W was passed to function
        ratio_string = 'None'
        ratio_data = None

        if pars['ID_W'] is not None:
            ratio_string = 'ID_W'
            ratio_data = pars['ID_W']

        elif pars['GM_ID'] is not None:
            ratio_string = 'GM_ID'
            ratio_data = pars['GM_ID']
        
        # determining the mode 
        # In usage mode (1), the inputs to the function are GM_ID (or ID/W), L, 
        # VDS and VSB
        if (pars['VGB'] and pars['VDB']) == None:
            mode = 1
        # In usage mode (2), VDB and VGB must be supplied to the function
        elif (pars['VGB'] and pars['VDB']) != None:
            mode = 2
        else:
            print("Invalid syntax or usage mode!")
        
        if mode == 1:
            VGS = self['VGS']
            ratio = self.look_up(ratio_string, VGS = VGS, VDS=pars['VDS'], VSB=pars['VSB'], L=pars['L'])
        
        elif mode == 2:
            step = self['VGS'][0] - self['VGS'][1]
            VSB = np.arange(max(self['VSB']), min(self['VSB']) + step, step)
            VGS = pars['VGB'] - VSB
            VDS = pars['VDB'] - VSB
            ratio = np.array([self.look_up(ratio_string, VGS=VGS[i], VDS=VDS[i], VSB=VSB[i], L=pars['L']).item() for i in range(len(VGS))])
            idx = ~np.isnan(ratio)
            ratio = ratio[idx]
            VGS = VGS[idx]
  
        if (np.size(pars['L']) == 1):
            ratio.shape += (1,)
        else:
            ratio = np.swapaxes(ratio, 0, 1)

        s = ratio.shape
        
        output = np.empty((s[1], len(np.atleast_1d(ratio_data))))
        output[:] = np.NaN
         
        for j in range(s[1]):
            ratio_range = ratio[:,j]
            VGS_range = VGS

            if ratio_string == 'GM_ID':
                m = max(ratio)
                idx = np.argmax(ratio)
                VGS_range = VGS_range[idx:]
                ratio_range = ratio_range[idx:]

                if max(np.atleast_1d(ratio_data)) > m:
                    print('look_upVGS: GM_ID input larger than maximum!')
            
            output[j,:] = interp1(ratio_range, VGS_range)(ratio_data)
            output = output[:]
        
        return np.squeeze(output)
