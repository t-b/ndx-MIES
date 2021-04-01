from pynwb import NWBHDF5IO
import ndx_mies

from datetime import datetime
from dateutil.tz import tzlocal
from pynwb import NWBFile
import numpy as np

from pynwb.icephys import CurrentClampStimulusSeries

def CreateMIESExtensionStructure(device):
    stimset_waveform = ndx_mies.StimulusSetWaveform("myThirdPartStimset", data = np.empty([1]))

    referencedWaveForm_1 = ndx_mies.StimulusSetReferencedWaveform("myCustomWave_1", data=np.empty([1]))
    stimulusSetFolder_1 = ndx_mies.StimulusSetReferencedFolder(name = "myCustomFolder_1", stimulus_set_referenced_waveforms = referencedWaveForm_1)

    referencedWaveForm_0 = ndx_mies.StimulusSetReferencedWaveform("myCustomWave_0", data=np.empty([0]))
    stimulusSetFolder_0 = ndx_mies.StimulusSetReferencedFolder(name = "myCustomFolder_0", stimulus_set_referenced_waveforms = referencedWaveForm_0)

    stimulusSetReferenced = ndx_mies.StimulusSetReferenced(stimulus_set_referenced_folders = [stimulusSetFolder_0, stimulusSetFolder_1])
    stimulusSets = ndx_mies.StimulusSets(name="myname", stimulus_set_referenced = stimulusSetReferenced, stimulus_set_waveforms = [stimset_waveform])

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
                                     lab_notebook = labnotebook,
                                     generated_by = generatedBy,
                                     stimulus_sets = stimulusSets,
                                     testpulse = testpulse)

    return metadata

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

    ccss = CurrentClampStimulusSeries(
        name="ccss", data=[1, 2, 3, 4, 5], starting_time=123.6, rate=10e3, electrode=elec, gain=0.02,
        sweep_number=np.uint32(0))

    nwbfile.add_stimulus(ccss)

    nwbfile.add_lab_meta_data(CreateMIESExtensionStructure(device))

    with NWBHDF5IO('icephys_example.nwb', 'w') as io:
       io.write(nwbfile)

    with NWBHDF5IO('icephys_example.nwb', 'r') as io:
       nwbfile = io.read()
       print(nwbfile)

       assert len(nwbfile.lab_meta_data) == 1

       meta = nwbfile.get_lab_meta_data()
       assert isinstance(meta, ndx_mies.MIESMetaData)

       # Labnotebook
       labnotebook = meta.lab_notebook
       assert isinstance(labnotebook, ndx_mies.LabNotebook)

       labnotebook_device = labnotebook.lab_notebook_device
       assert isinstance(labnotebook_device, ndx_mies.LabNotebookDevice)

       lbn_num_values  = labnotebook_device.lab_notebook_numerical_values
       lbn_num_keys    = labnotebook_device.lab_notebook_numerical_keys
       lbn_text_values = labnotebook_device.lab_notebook_textual_values
       lbn_text_keys   = labnotebook_device.lab_notebook_textual_keys
       assert isinstance(lbn_num_values, ndx_mies.LabNotebookNumericalValues)
       assert isinstance(lbn_num_keys, ndx_mies.LabNotebookNumericalKeys)
       assert isinstance(lbn_text_values, ndx_mies.LabNotebookTextualValues)
       assert isinstance(lbn_text_keys, ndx_mies.LabNotebookTextualKeys)

       # StimulusSets
       stimulus_sets = meta.stimulus_sets
       assert isinstance(stimulus_sets, ndx_mies.StimulusSets)

       stimulus_set_referenced = stimulus_sets.stimulus_set_referenced
       assert isinstance(stimulus_set_referenced, ndx_mies.StimulusSetReferenced)

       # Custom wave

       assert len(stimulus_set_referenced.stimulus_set_referenced_folders) == 2

       folder_0 = stimulus_set_referenced.stimulus_set_referenced_folders["myCustomFolder_0"]
       assert isinstance(folder_0, ndx_mies.StimulusSetReferencedFolder)

       customWave_0 = folder_0["customWave_0"]
       assert isinstance(customWave_0, ndx_mies.StimulusSetReferencedWaveform)

       folder_1 = stimulus_set_referenced.stimulus_set_referenced_folders["myCustomFolder_1"]
       assert isinstance(folder_1, ndx_mies.StimulusSetReferencedFolder)

       customWave_1 = folder_1["customWave_1"]
       assert isinstance(customWave_1, ndx_mies.StimulusSetReferencedWaveform)
