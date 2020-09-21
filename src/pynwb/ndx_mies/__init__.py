import os
from pynwb import load_namespaces, get_class

# Set path of the namespace.yaml file to the expected install location
ndx_mies_specpath = os.path.join(
    os.path.dirname(__file__),
    'spec',
    'ndx-MIES.namespace.yaml'
)

# If the extension has not been installed yet but we are running directly from
# the git repo
if not os.path.exists(ndx_mies_specpath):
    ndx_mies_specpath = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        '..', '..', '..',
        'spec',
        'ndx-MIES.namespace.yaml'
    ))

# Load the namespace
load_namespaces(ndx_mies_specpath)

StimulusSetWavebuilderSegmentTypes = get_class('StimulusSetWavebuilderSegmentTypes', 'ndx-mies')
StimulusSetWavebuilderParameterText = get_class('StimulusSetWavebuilderParameterText', 'ndx-mies')
StimulusSetWavebuilderParameter = get_class('StimulusSetWavebuilderParameter', 'ndx-mies')
StimulusSetWaveform = get_class('StimulusSetWaveform', 'ndx-mies')

StimulusSetReferencedWaveform = get_class('StimulusSetReferencedWaveform', 'ndx-mies')
StimulusSetReferencedFolder = get_class('StimulusSetReferencedFolder', 'ndx-mies')
StimulusSetReferenced = get_class('StimulusSetReferenced', 'ndx-mies')
StimulusSets = get_class('StimulusSets', 'ndx-mies')

LabNotebookTextualKeys = get_class('LabNotebookTextualKeys', 'ndx-mies')
LabNotebookTextualValues = get_class('LabNotebookTextualValues', 'ndx-mies')
LabNotebookNumericalKeys = get_class('LabNotebookNumericalKeys', 'ndx-mies')
LabNotebookNumericalValues = get_class('LabNotebookNumericalValues', 'ndx-mies')

LabNotebookDevice = get_class('LabNotebookDevice', 'ndx-mies')
LabNotebook = get_class('LabNotebook', 'ndx-mies')

TestpulseRawData = get_class('TestpulseRawData', 'ndx-mies')
TestpulseMetadata = get_class('TestpulseMetadata', 'ndx-mies')
TestpulseDevice = get_class('TestpulseDevice', 'ndx-mies')
Testpulse = get_class('Testpulse', 'ndx-mies')

UserCommentString = get_class('UserCommentString', 'ndx-mies')
UserCommentDevice = get_class('UserCommentDevice', 'ndx-mies')
UserComment = get_class('UserComment', 'ndx-mies')

GeneratedBy = get_class('GeneratedBy', 'ndx-mies')

MIESMetaData = get_class('MIESMetaData', 'ndx-mies')
