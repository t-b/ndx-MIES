from pynwb import NWBHDF5IO
import ndx_mies

def test_basics():
    assert 1 == 1
    io = NWBHDF5IO('../data/ndx-mies-test-data-compressed.nwb', 'r')
    nwbfile = io.read()
    print(ndx_mies.GeneratedBy)
    # elem = nwbfile.get_lab_meta_data('GeneratedBy')
    # print("meta: ", nwbfile.add_container(GeneratedBy))
    # elem = ndx_mies.MIESMetaData
    # nwbfile.add_lab_meta_data(elem)
    # print(nwbfile.all_children())
    # print(ndx_mies.MIESMetaData)
