import os
import numpy as np
import pytest
import scipy

from pygmid import Lookup

arange_endpoint = lambda start, stop, step: np.arange(start, stop+step, step)

@pytest.fixture(scope='module')
def expected_data() -> dict:
    return scipy.io.loadmat('tests/files/gen_test_lookup_data.mat', matlab_compatible=True)

def test_lookup_alias(nch):
    VDSs = nch['VDS']
    VGSs = np.arange(0.4, 0.6, 0.05)

    IDe = nch.look_up('ID', vds=VDSs, vgs=VGSs)
    IDa = nch.lookup('ID', vds=VDSs, vgs=VGSs)
    assert IDa is not None and len(IDa)>0
    assert IDe is not None and len(IDe)>0
    assert np.testing.assert_array_equal(IDe, IDa) is None

def test_lookupVGS_alias(nch: Lookup):
    expected_vgs = nch.look_upVGS(GM_ID = 10, VDS = 0.6, VSB = 0.1, L = 0.18)
    actual_vgs = nch.lookupVGS(GM_ID = 10, VDS = 0.6, VSB = 0.1, L = 0.18)
    assert np.allclose(actual_vgs, expected_vgs)

def test_look_up_vgs(nch: Lookup, expected_data):
    expected_8_vgs  = expected_data['expected_8_vgs']
    expected_9_vgs  = expected_data['expected_9_vgs']
    expected_10_vgs = expected_data['expected_10_vgs']
    expected_11_vgs = expected_data['expected_11_vgs']
    expected_12_vgs = expected_data['expected_12_vgs']
    expected_13_vgs = expected_data['expected_13_vgs']
    
    actual_8_vgs = nch.look_upVGS(GM_ID = 10, VDS = 0.6, VSB = 0.1, L = 0.18)
    # assert np.allclose(actual_8_vgs.flatten(), expected_8_vgs.flatten())

    actual_9_vgs = nch.look_upVGS(GM_ID = arange_endpoint(10, 16, 1), VDS = 0.6, VSB = 0.1, L = 0.18)
    assert np.allclose(actual_9_vgs.flatten(), expected_9_vgs.flatten())

    actual_10_vgs = nch.look_upVGS(ID_W = 1e-4, VDS = 0.6, VSB = 0.1, L = 0.18)
    assert np.allclose(actual_10_vgs.flatten(), expected_10_vgs.flatten())

    actual_11_vgs = nch.look_upVGS(ID_W = 1e-4, VDS = 0.6, VSB = 0.1, L = np.arange(0.18, 0.5, 0.1))
    assert np.allclose(actual_11_vgs.flatten(), expected_11_vgs.flatten())

    actual_12_vgs = nch.look_upVGS(GM_ID = 10, VDB = 0.6, VGB = 1, L = 0.18)
    assert np.allclose(actual_12_vgs.flatten(), expected_12_vgs.flatten())

    actual_13_vgs = nch.look_upVGS(ID_W = 1e-4, VDB = 0.6, VGB = 1, L = 0.18)
    assert np.allclose(actual_13_vgs.flatten(), expected_13_vgs.flatten())

def test_look_up(nch: Lookup, expected_data):

    expected_1_ID     = expected_data['expected_1_ID']
    expected_2_vt     = expected_data['expected_2_vt']
    expected_3_ft     = expected_data['expected_3_ft']
    expected_4_id_w   = expected_data['expected_4_id_w']
    expected_5_id_w   = expected_data['expected_5_id_w']
    expected_6_gm_gds = expected_data['expected_6_gm_gds']
    expected_7_gm_ID  = expected_data['expected_7_gm_ID']

    assert len(nch.look_up('A', a_b='A_B')) == 0

    r_vds = nch['VDS'] 
    r_vgs = arange_endpoint(0.4, 0.6, 0.05)
    actual_1_ID = nch.look_up('ID', vds=r_vds, vgs=r_vgs)
    assert np.allclose(actual_1_ID, expected_1_ID)

    Ls = nch['L']
    actual_2_vt = nch.look_up('VT', vgs=0.6, L=Ls)
    assert np.allclose(actual_2_vt.flatten(), expected_2_vt.flatten())

    gm_ids = arange_endpoint(5, 20, 0.1)
    Ls = np.arange(min(nch['L']),0.3,0.05)
    actual_3_ft = nch.look_up('GM_CGG', GM_ID=gm_ids, L =np.arange(min(Ls),0.3,0.05))/2/np.pi
    assert np.allclose(actual_3_ft, expected_3_ft)

    gm_ids = arange_endpoint(5, 20, 0.1)
    Ls = [0.18, 0.23, 0.28, 0.3]
    actual_4_id_w = nch.look_up('ID_W', GM_ID=gm_ids, L=Ls)
    assert np.allclose(actual_4_id_w, expected_4_id_w)

    gm_ids = arange_endpoint(5, 20, 0.1)
    actual_5_id_w = nch.look_up('ID_W', GM_ID=gm_ids, VDS=[0.8, 1.0, 1.2])
    assert np.allclose(actual_5_id_w, expected_5_id_w)

    gm_ids = arange_endpoint(5, 20, 0.1)
    actual_6_gm_gds = nch.look_up('GM_GDS', GM_ID=gm_ids)
    assert np.allclose(actual_6_gm_gds, expected_6_gm_gds.flatten())

    actual_7_gm_ID = nch.look_up('GM_ID', VDS=arange_endpoint(0.025, 1.2, 0.025), VSB=0.0, L=0.18)
    assert np.allclose(actual_7_gm_ID, expected_7_gm_ID)

def test___contains__(nch: Lookup):
    assert 'L' in nch
    assert 'VGS' in nch
    assert 'VDS' in nch
    assert 'VSB' in nch

    # methods and properties of the object not included
    assert '__init__' not in nch

def test___getitem__(nch: Lookup):
    assert nch['L'] is not None
    assert nch['VGS'] is not None
    assert nch['VDS'] is not None
    assert nch['VSB'] is not None

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