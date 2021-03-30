from pynwb import NWBHDF5IO
import ndx_mies

from datetime import datetime
from dateutil.tz import tzlocal
from pynwb import NWBFile
import numpy as np

def test_basics():

    nwbfile = NWBFile('my first synthetic recording', 'EXAMPLE_ID', datetime.now(tzlocal()),
                      experimenter='Dr. Bilbo Baggins',
                      lab='Bag End Laboratory',
                      institution='University of Middle Earth at the Shire',
                      experiment_description='I went on an adventure with thirteen dwarves to reclaim vast treasures.',
                      session_id='LONELYMTN')

    device = nwbfile.create_device(name='Heka ITC-1600')

    elec = nwbfile.create_icephys_electrode(name="elec0",
                                            description='a mock intracellular electrode',
                                            device=device)

    from pynwb.icephys import CurrentClampStimulusSeries

    ccss = CurrentClampStimulusSeries(
        name="ccss", data=[1, 2, 3, 4, 5], starting_time=123.6, rate=10e3, electrode=elec, gain=0.02, sweep_number=0)

    nwbfile.add_stimulus(ccss)

    stimset_waveform = ndx_mies.StimulusSetWaveform("myThirdPartStimset", data = np.empty([1]))

    referencedWaveForm_1 = ndx_mies.StimulusSetReferencedWaveform("myCustomWave_1", data=np.empty([1]))
    stimulusSetFolder_1 = ndx_mies.StimulusSetReferencedFolder(name = "myCustomFolder_1", stimulus_set_referenced_waveforms = referencedWaveForm_1)

    referencedWaveForm_0 = ndx_mies.StimulusSetReferencedWaveform("myCustomWave_0", data=np.empty([0]))
    stimulusSetFolder_0 = ndx_mies.StimulusSetReferencedFolder(name = "myCustomFolder_0", stimulus_set_referenced_waveforms = referencedWaveForm_0)

    stimulusSetReferenced = ndx_mies.StimulusSetReferenced(stimulus_set_referenced_folders = [stimulusSetFolder_0, stimulusSetFolder_1])
    stimulusSets = ndx_mies.StimulusSets(name="myname", stimulus_set_referenced = stimulusSetReferenced)

    labnotebookDevice = ndx_mies.LabNotebookDevice(device.name,
                                                   lab_notebook_numerical_values =
                                                   ndx_mies.LabNotebookNumericalValues(name="numericalValues", data=np.empty([0, 0, 0])),
                                                   lab_notebook_numerical_keys =
                                                   ndx_mies.LabNotebookNumericalKeys(name="numericalKeys", data=np.empty([3, 0])),
                                                   lab_notebook_textual_values =
                                                   ndx_mies.LabNotebookTextualValues(name="textualValues", data=np.empty([0, 9, 0])),
                                                   lab_notebook_textual_keys =
                                                   ndx_mies.LabNotebookTextualKeys(name="textualKeys", data=np.empty([3, 0])))

    labnotebook = ndx_mies.LabNotebook(name = "labnotebook", lab_notebook_device = labnotebookDevice)

    # userCommentString = ndx_mies.UserCommentString(name="userComment", data="my comment")
    # userCommentDevice = ndx_mies.UserCommentDevice(device.name, user_comment_string = userCommentString)
    # userComment = ndx_mies.UserComment(name="user_comment", user_comment_device = userCommentDevice)

    generatedBy = ndx_mies.GeneratedBy(name="generated_by", data=np.empty([0, 2]))

    testpulseRawData_0 = ndx_mies.TestpulseRawData(name="testpulse_0", data=np.empty([0]))
    testpulseRawData_1 = ndx_mies.TestpulseRawData(name="testpulse_1", data=np.empty([0]))
    testpulseMetaData_0 = ndx_mies.TestpulseMetadata(name="tpstorage_0", data=np.empty([0, 0, 0]))
    testpulseMetaData_1 = ndx_mies.TestpulseMetadata(name="tpstorage_1", data=np.empty([0, 0, 0]))
    testpulseDevice = ndx_mies.TestpulseDevice(name = device.name,
                                               testpulse_metadatas = [testpulseMetaData_0, testpulseMetaData_1],
                                               testpulse_raw_datas = [testpulseRawData_0, testpulseRawData_1])
    testpulse = ndx_mies.Testpulse(name="testpulse", testpulse_device = testpulseDevice)

    metadata = ndx_mies.MIESMetaData(name="MIES",
                                     lab_notebook=labnotebook,
                                     generated_by = generatedBy,
                                     stimulus_sets = stimulusSets,
                                     testpulse = testpulse)

    nwbfile.add_lab_meta_data(metadata)

    from pynwb import NWBHDF5IO

    with NWBHDF5IO('icephys_example.nwb', 'w') as io:
       io.write(nwbfile)

    with NWBHDF5IO('icephys_example.nwb', 'r') as io:
       nwbfile = io.read()
       print(nwbfile)

    # assert 1 == 1
    # io = NWBHDF5IO('../data/ndx-mies-test-data-compressed.nwb', 'r')
    # nwbfile = io.read()
    # print(ndx_mies.GeneratedBy)
    # # elem = nwbfile.get_lab_meta_data('GeneratedBy')
    # # print("meta: ", nwbfile.add_container(GeneratedBy))
    # # elem = ndx_mies.MIESMetaData
    # # nwbfile.add_lab_meta_data(elem)
    # # print(nwbfile.all_children())
    # # print(ndx_mies.MIESMetaData)
