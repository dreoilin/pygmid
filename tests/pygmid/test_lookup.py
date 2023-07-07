import os
import numpy as np
import pytest
import scipy

from pygmid import Lookup

def test_lookup_alias(nch):
    VDSs = nch['VDS']       # lookup object has pseudo-array access to data
    VGSs = np.arange(0.4, 0.6, 0.05)

    IDe = nch.look_up('ID', vds=VDSs, vgs=VGSs)
    IDa = nch.lookup('ID', vds=VDSs, vgs=VGSs)
    assert IDa is not None and len(IDa)>0
    assert IDe is not None and len(IDe)>0
    assert np.testing.assert_array_equal(IDe, IDa) is None

# TODO
def test_look_up(nch: Lookup):
#     VDSs = nch['VDS']       # lookup object has pseudo-array access to data
#     VGSs = np.arange(0.4, 0.6, 0.05)

#     # Plot ID versus VDS
#     ID = nch.look_up('ID', vds=VDSs, vgs=VGSs)
    # CHECKME: A rather silly example
    assert nch.look_up('A', a_b='A_B') == []


def test___contains__(nch: Lookup):
    assert 'L' in nch
    assert 'VGS' in nch
    assert 'VDS' in nch
    assert 'VSB' in nch

    assert 'METHOD' not in nch
    
    # Missing
    assert 'VGB' not in nch
    assert 'GM_ID' not in nch
    assert 'ID_W' not in nch
    assert 'VDB' not in nch

    # methods and properties of the object not included
    assert '__init__' not in nch

def test___getitem__(nch: Lookup):
    assert nch['L'] is not None
    assert nch['VGS'] is not None
    assert nch['VDS'] is not None
    assert nch['VSB'] is not None
    # CHECKME: these should not be in the data?
    # assert nch['VGB']
    # assert nch['GM_ID']
    # assert nch['ID_W']
    # assert nch['VDB']

    with pytest.raises(ValueError):
        assert nch['nonexistingkey']

def test_setup(empty_filename, nch_filename):
    with pytest.raises(FileNotFoundError):
        Lookup(filename='FILETHATDOESNTEXIST.mat')

    assert os.path.exists(empty_filename)
    with pytest.raises(scipy.io.matlab._miobase.MatReadError):
        Lookup(filename=empty_filename)
    
    with pytest.raises(RuntimeError):
        Lookup(filename='doesnt end in .mat extension.oops')
    
    lookup = Lookup(filename=nch_filename)
    assert lookup._Lookup__DATA is not None

def test_setup_defaults(nch_filename):
    lookup = Lookup(filename=nch_filename)
    assert lookup._Lookup__default is not None
    assert lookup._Lookup__default['L'] == min(lookup._Lookup__DATA['L'])
    assert np.array_equal(lookup._Lookup__default['VGS'], lookup._Lookup__DATA['VGS'])
    assert lookup._Lookup__default['VDS'] == max(lookup._Lookup__DATA['VDS']/2)
    assert lookup._Lookup__default['VSB'] == 0.0
    assert lookup._Lookup__default['METHOD'] == 'pchip'
    assert lookup._Lookup__default['VGB'] == None
    assert lookup._Lookup__default['GM_ID'] == None
    assert lookup._Lookup__default['ID_W'] == None
    assert lookup._Lookup__default['VDB'] == None

    lookup2 = Lookup(filename=nch_filename, L=1, VGS=1, VDS=1, VSB=1, METHOD='linear', VGB=1, GM_ID=1, ID_W=1, VDB=1)
    assert lookup2._Lookup__default['L'] == 1
    assert lookup2._Lookup__default['VGS'] == 1
    assert lookup2._Lookup__default['VDS'] == 1
    assert lookup2._Lookup__default['VSB'] == 1
    assert lookup2._Lookup__default['METHOD'] == 'linear'
    assert lookup2._Lookup__default['VGB'] == 1
    assert lookup2._Lookup__default['GM_ID'] == 1
    assert lookup2._Lookup__default['ID_W'] == 1
    assert lookup2._Lookup__default['VDB'] == 1

def test_load(nch: Lookup, pch: Lookup, pch_filename):
    loaded_pch_data = nch._Lookup__load(pch_filename)
    assert loaded_pch_data is not None
    # assert all(e[0]==a[0] and np.testing.assert_array_equal(e[1],a[1]) for e, a in zip(pch._Lookup__DATA.items(),loaded_pch_data.items()))
    # assert any(e[0]==a[0] and not np.testing.assert_array_equal(e[1],a[1]) for e, a in zip(nch._Lookup__DATA.items(),loaded_pch_data.items()))

def test_modeset(nch:Lookup):
    assert nch._modeset(1, 1) == 1
    assert nch._modeset([1], [1]) == 1
    assert nch._modeset([1], 1) == 1
    assert nch._modeset(1, [1]) == 1
    assert nch._modeset([1,1], 1) == 2
    assert nch._modeset([1,1], [1]) == 2
    assert nch._modeset([1,1], [1,1]) == 3
    with pytest.raises(ValueError):
        nch._modeset([1], [1,2])
    with pytest.raises(ValueError):
        nch._modeset(1, [1,2])