from pynwb import NWBHDF5IO
import ndx_mies

from datetime import datetime
from dateutil.tz import tzlocal
from pynwb import NWBFile
import numpy as np

from pynwb.icephys import CurrentClampStimulusSeries


def CreateMIESExtensionStructure(device):
    stimset_waveform = ndx_mies.StimulusSetWaveform("myThirdPartStimset", data=np.empty([1]))

    referencedWaveForm_1 = ndx_mies.StimulusSetReferencedWaveform("myCustomWave_1", data=np.empty([1]))
    stimulusSetFolder_1 = ndx_mies.StimulusSetReferencedFolder(
        name="myCustomFolder_1", stimulus_set_referenced_waveforms=referencedWaveForm_1
    )

    referencedWaveForm_0 = ndx_mies.StimulusSetReferencedWaveform("myCustomWave_0", data=np.empty([0]))
    stimulusSetFolder_0 = ndx_mies.StimulusSetReferencedFolder(
        name="myCustomFolder_0", stimulus_set_referenced_waveforms=referencedWaveForm_0
    )

    stimulusSet_0_WP = ndx_mies.StimulusSetWavebuilderParameter("setA_WP", data=np.empty([0, 100, 9]))
    stimulusSet_0_WPT = ndx_mies.StimulusSetWavebuilderParameterText("setA_WPT", data=np.empty([0, 100, 9]))
    stimulusSet_0_SegWvType = ndx_mies.StimulusSetWavebuilderSegmentTypes("setA_SegWvType", data=np.empty([102]))

    stimulusSet_1_WP = ndx_mies.StimulusSetWavebuilderParameter("setB_WP", data=np.empty([0, 100, 9]))
    stimulusSet_1_WPT = ndx_mies.StimulusSetWavebuilderParameterText("setB_WPT", data=np.empty([0, 100, 9]))
    stimulusSet_1_SegWvType = ndx_mies.StimulusSetWavebuilderSegmentTypes("setB_SegWvType", data=np.empty([102]))

    stimulusSetReferenced = ndx_mies.StimulusSetReferenced(
        stimulus_set_referenced_folders=[stimulusSetFolder_0, stimulusSetFolder_1]
    )

    stimulusSets = ndx_mies.StimulusSets(
        name="myname",
        stimulus_set_referenced=stimulusSetReferenced,
        stimulus_set_waveforms=[stimset_waveform],
        stimulus_set_wavebuilder_parameters=[stimulusSet_0_WP, stimulusSet_1_WP],
        stimulus_set_wavebuilder_parameter_texts=[stimulusSet_0_WPT, stimulusSet_1_WPT],
        stimulus_set_wavebuilder_segment_types=[
            stimulusSet_0_SegWvType,
            stimulusSet_1_SegWvType,
        ],
    )

    lbnNumValues = ndx_mies.LabNotebookNumericalValues(name="numericalValues", data=np.empty([0, 0, 0]))
    lbnNumKeys = ndx_mies.LabNotebookNumericalKeys(name="numericalKeys", data=np.empty([3, 0]))
    lbnTextValues = ndx_mies.LabNotebookTextualValues(name="textualValues", data=np.empty([0, 9, 0]))
    lbnTextKeys = ndx_mies.LabNotebookTextualKeys(name="textualKeys", data=np.empty([3, 0]))

    labnotebookDevice = ndx_mies.LabNotebookDevice(
        device.name,
        lab_notebook_numerical_values=lbnNumValues,
        lab_notebook_numerical_keys=lbnNumKeys,
        lab_notebook_textual_values=lbnTextValues,
        lab_notebook_textual_keys=lbnTextKeys,
    )

    labnotebook = ndx_mies.LabNotebook(name="labnotebook", lab_notebook_device=labnotebookDevice)

    # Broken due to https://github.com/NeurodataWithoutBorders/pynwb/issues/1346
    #
    # userCommentString = ndx_mies.UserCommentString(name="userComment", data="my comment")
    # userCommentDevice = ndx_mies.UserCommentDevice(device.name, user_comment_string = userCommentString)
    # userComment = ndx_mies.UserComment(name="user_comment", user_comment_device = userCommentDevice)

    generatedBy = ndx_mies.GeneratedBy(name="generated_by", data=np.empty([0, 2]))

    testpulseRawData_0 = ndx_mies.TestpulseRawData(name="testpulse_0", data=np.empty([0]))
    testpulseRawData_1 = ndx_mies.TestpulseRawData(name="testpulse_1", data=np.empty([0]))
    testpulseMetaData_0 = ndx_mies.TestpulseMetadata(name="tpstorage_0", data=np.empty([0, 0, 0]))
    testpulseMetaData_1 = ndx_mies.TestpulseMetadata(name="tpstorage_1", data=np.empty([0, 0, 0]))

    testpulseDevice = ndx_mies.TestpulseDevice(
        name=device.name,
        testpulse_metadatas=[testpulseMetaData_0, testpulseMetaData_1],
        testpulse_raw_datas=[testpulseRawData_0, testpulseRawData_1],
    )

    testpulse = ndx_mies.Testpulse(name="testpulse", testpulse_device=testpulseDevice)

    metadata = ndx_mies.MIESMetaData(
        name="MIES",
        # user_comment = userComment,
        lab_notebook=labnotebook,
        generated_by=generatedBy,
        stimulus_sets=stimulusSets,
        testpulse=testpulse,
    )

    return metadata


def test_basics():

    nwbfile = NWBFile(
        "A",
        "B",
        datetime.now(tzlocal()),
        experimenter="C",
        lab="D",
        institution="E",
        experiment_description="F",
        session_id="G",
    )

    device = nwbfile.create_device(name="H")

    nwbfile.add_lab_meta_data(CreateMIESExtensionStructure(device))

    with NWBHDF5IO("icephys_example.nwb", "w") as io:
        io.write(nwbfile)

    with NWBHDF5IO("icephys_example.nwb", "r") as io:
        nwbfile = io.read()

        assert len(nwbfile.lab_meta_data) == 1

        meta = nwbfile.get_lab_meta_data()
        assert isinstance(meta, ndx_mies.MIESMetaData)

        # Labnotebook
        labnotebook = meta.lab_notebook
        assert isinstance(labnotebook, ndx_mies.LabNotebook)

        lbnDevice = labnotebook.lab_notebook_device
        assert isinstance(lbnDevice, ndx_mies.LabNotebookDevice)

        lbnNumValues = lbnDevice.lab_notebook_numerical_values
        lbnNumKeys = lbnDevice.lab_notebook_numerical_keys
        lbnTextValues = lbnDevice.lab_notebook_textual_values
        lbnTextKeys = lbnDevice.lab_notebook_textual_keys
        assert isinstance(lbnNumValues, ndx_mies.LabNotebookNumericalValues)
        assert isinstance(lbnNumKeys, ndx_mies.LabNotebookNumericalKeys)
        assert isinstance(lbnTextValues, ndx_mies.LabNotebookTextualValues)
        assert isinstance(lbnTextKeys, ndx_mies.LabNotebookTextualKeys)

        # StimulusSets
        stimulus_sets = meta.stimulus_sets
        assert isinstance(stimulus_sets, ndx_mies.StimulusSets)

        stimulusReferenced = stimulus_sets.stimulus_set_referenced
        assert isinstance(stimulusReferenced, ndx_mies.StimulusSetReferenced)

        # Custom Wave
        assert len(stimulusReferenced.stimulus_set_referenced_folders) == 2

        folder_0 = stimulusReferenced.stimulus_set_referenced_folders["myCustomFolder_0"]
        assert isinstance(folder_0, ndx_mies.StimulusSetReferencedFolder)

        customWave_0 = folder_0["myCustomWave_0"]
        assert isinstance(customWave_0, ndx_mies.StimulusSetReferencedWaveform)

        folder_1 = stimulusReferenced.stimulus_set_referenced_folders["myCustomFolder_1"]
        assert isinstance(folder_1, ndx_mies.StimulusSetReferencedFolder)

        customWave_1 = folder_1["myCustomWave_1"]
        assert isinstance(customWave_1, ndx_mies.StimulusSetReferencedWaveform)

        # third party stimset
        stimulusWaveform = stimulus_sets.stimulus_set_waveforms["myThirdPartStimset"]
        assert isinstance(stimulusWaveform, ndx_mies.StimulusSetWaveform)

        # WP/WPT/SegWvType
        stimulusWPTs = stimulus_sets.stimulus_set_wavebuilder_parameters
        assert len(stimulusWPTs) == 2

        stimulusSet_0_WP = stimulusWPTs["setA_WP"]
        assert isinstance(stimulusSet_0_WP, ndx_mies.StimulusSetWavebuilderParameter)

        stimulusSet_1_WP = stimulusWPTs["setB_WP"]
        assert isinstance(stimulusSet_1_WP, ndx_mies.StimulusSetWavebuilderParameter)

        stimulusWPTs = stimulus_sets.stimulus_set_wavebuilder_parameter_texts
        assert len(stimulusWPTs) == 2

        stimulusSet_0_WPT = stimulusWPTs["setA_WPT"]
        assert isinstance(stimulusSet_0_WPT, ndx_mies.StimulusSetWavebuilderParameterText)

        stimulusSet_1_WPT = stimulusWPTs["setB_WPT"]
        assert isinstance(stimulusSet_1_WPT, ndx_mies.StimulusSetWavebuilderParameterText)

        stimulusSegWvTypes = stimulus_sets.stimulus_set_wavebuilder_segment_types
        assert len(stimulusSegWvTypes) == 2

        stimulusSet_0_SegWvType = stimulusSegWvTypes["setA_SegWvType"]
        assert isinstance(stimulusSet_0_SegWvType, ndx_mies.StimulusSetWavebuilderSegmentTypes)

        stimulusSet_1_SegWvType = stimulusSegWvTypes["setB_SegWvType"]
        assert isinstance(stimulusSet_1_SegWvType, ndx_mies.StimulusSetWavebuilderSegmentTypes)

        # Testpulse
        testpulse = meta.testpulse
        assert isinstance(testpulse, ndx_mies.Testpulse)

        testpulseDevice = meta.testpulse.testpulse_device
        assert isinstance(testpulseDevice, ndx_mies.TestpulseDevice)

        testpulseMetaDatas = testpulseDevice.testpulse_metadatas
        assert len(testpulseMetaDatas) == 2

        testpulseMetaData_0 = testpulseMetaDatas["tpstorage_0"]
        assert isinstance(testpulseMetaData_0, ndx_mies.TestpulseMetadata)

        testpulseMetaData_1 = testpulseMetaDatas["tpstorage_1"]
        assert isinstance(testpulseMetaData_1, ndx_mies.TestpulseMetadata)

        testpulseRawDatas = testpulseDevice.testpulse_raw_datas
        assert len(testpulseRawDatas) == 2

        testpulseRawData_0 = testpulseRawDatas["testpulse_0"]
        assert isinstance(testpulseRawData_0, ndx_mies.TestpulseRawData)

        testpulseRawData_1 = testpulseRawDatas["testpulse_1"]
        assert isinstance(testpulseRawData_1, ndx_mies.TestpulseRawData)

        generatedBy = meta.generated_by
        assert isinstance(generatedBy, ndx_mies.GeneratedBy)

        # TODO add userComment, userCommentString, userCommentDevice
