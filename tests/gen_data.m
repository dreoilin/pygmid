% Generate data for test files
clearvars;
close all;

% load data in strcuture format
% all nmos data is contained in structure nch
% all pmos data is contained in structure pch
load 180nch.mat;
load 180pch.mat;
device = nch;
L = device.L;

vds = device.VDS;
vgs = 0.4:0.05:0.6;
expected_1_ID = look_up(device, 'ID', 'VDS', vds, 'VGS', vgs);

expected_2_vt = look_up(device, 'VT', 'VGS', 0.6, 'L', L);

gm_id = 5:0.1:20;
expected_3_ft = look_up(device, 'GM_CGG', 'GM_ID', gm_id, 'L', min(L):0.05:0.3)/2/pi;

gm_id = 5:0.1:20;
expected_4_id_w = look_up(device, 'ID_W', 'GM_ID', gm_id, 'L', [0.18 0.23 0.28 0.3]);

gm_id = 5:0.1:20;
expected_5_id_w = look_up(device, 'ID_W', 'GM_ID', gm_id, 'VDS', [0.8 1.0 1.2]);

gm_id = 5:0.1:20;
expected_6_gm_gds = look_up(device,'GM_GDS','GM_ID', gm_id);

expected_7_gm_ID = look_up(device, 'GM_ID', 'VDS', [0.025:0.025:1.2], VSB=0.0, L=0.18);

expected_8_vgs = look_upVGS(device, 'GM_ID', 10, 'VDS', 0.6, 'L', 0.18);
expected_9_vgs = look_upVGS(device, 'GM_ID', [10:1:16], 'VDS', 0.6, 'VSB', 0.1, 'L', 0.18);
expected_10_vgs = look_upVGS(device, 'ID_W', 1e-4, 'VDS', 0.6, 'VSB', 0.1, 'L', 0.18);
expected_11_vgs = look_upVGS(device, 'ID_W', 1e-4, 'VDS', 0.6, 'VSB', 0.1, 'L', [0.18:0.1:0.5]);
expected_12_vgs = look_upVGS(device, 'GM_ID', 10, 'VDB', 0.6, 'VGB', 1, 'L', 0.18);
expected_13_vgs = look_upVGS(device, 'ID_W', 1e-4, 'VDB', 0.6, 'VGB', 1, 'L', 0.18);

save("gen_test_lookup_data.mat", "expected_1_ID", "expected_2_vt", "expected_3_ft", "expected_4_id_w", "expected_5_id_w" , "expected_6_gm_gds", "expected_7_gm_ID", "expected_8_vgs", "expected_9_vgs", "expected_10_vgs", "expected_11_vgs", "expected_12_vgs", "expected_13_vgs", "-v7","-nocompression")
