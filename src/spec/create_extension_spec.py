#!python
#
# -*- coding: utf-8 -*-
#
# All references commits are from the MIES repository at https://github.com/AllenInstitute/MIES
#
# References:
# - https://github.com/AllenInstitute/IPNWB/blob/master/Readme.rst
# - Various files created by MIES

import os.path

from pynwb.spec import (NWBNamespaceBuilder, export_spec, NWBGroupSpec, NWBDatasetSpec)


def main():

    # BEGIN normal parameter waves and raw stimsets

    stimset_parameter_segments = NWBDatasetSpec(doc='Stimulus set parameters for the full set. '
                                                'See also https://alleninstitute.github.io/MIES/file/_m_i_e_s___wave_data_folder_getters_8ipf.html#_CPPv418GetSegmentTypeWavev.',
                                                neurodata_type_def='StimulusSetWavebuilderSegmentTypes',
                                                neurodata_type_inc='NWBData',
                                                shape=(102,))

    stimset_parameter_textual = NWBDatasetSpec(doc='Textual part of the stimulus set parameter waves for recreating the stimset in MIES. '
                                               'Rows are the data entries, Columns are the index of the segment/epoch (last index holds '
                                               'settings for the full set) and Layers hold different stimulus waveform types. '
                                               'See also https://alleninstitute.github.io/MIES/file/_m_i_e_s___wave_data_folder_getters_8ipf.html#_CPPv427GetWaveBuilderWaveTextParamv.',
                                               neurodata_type_def='StimulusSetWavebuilderParameterText',
                                               neurodata_type_inc='NWBData',
                                               shape=(None, 100, 9))

    stimset_parameter_numerical = NWBDatasetSpec(doc='Numerical part of the stimulus set parameter waves for recreating the stimset in MIES. '
                                                 'Rows are the data entries, Columns are the index of the segment/epoch '
                                                 'and Layers hold different stimulus waveform types. '
                                                 'See also https://alleninstitute.github.io/MIES/file/_m_i_e_s___wave_data_folder_getters_8ipf.html#_CPPv423GetWaveBuilderWaveParamv.',
                                                 neurodata_type_def='StimulusSetWavebuilderParameter',
                                                 neurodata_type_inc='NWBData',
                                                 shape=(None, 100, 9))

    stimset_waveform = NWBDatasetSpec(doc='Stimulus set waveform data. This is only present if not all three parameter waves could be found '
                                      'or a third-party stimset was used. One column per sweep.',
                                      neurodata_type_def='StimulusSetWaveform',
                                      neurodata_type_inc='NWBData',
                                      shape=(None, None))

    # END normal parameter waves and raw stimsets

    # BEGIN custom wave handling

    stimset_referenced_waveform = NWBDatasetSpec(doc='Additional stimulus set waveform data. Some epoch types for stimulus sets allow to include arbitrary waveform data. '
                                                 'These waveforms are stored in a tree structure here. The stimulus set parameter referencing these waveforms has the path '
                                                 'to these entries with colons (:) separated.',
                                                 neurodata_type_def='StimulusSetReferencedWaveform')

    stimset_referenced_folder = NWBGroupSpec(doc='Folder',
                                             neurodata_type_def='StimulusSetReferencedFolder',
                                             datasets=[NWBDatasetSpec(doc='Additional stimulus set waveform data. Some epoch types for stimulus sets allow to include arbitrary waveform data. '
                                                                      'These waveforms are stored in a tree structure here. The stimulus set parameter referencing these waveforms has the path '
                                                                      'to these entries with colons (:) separated.',
                                                                      neurodata_type_inc='StimulusSetReferencedWaveform',
                                                                      quantity='*')
                                                      ],
                                             # groups=[NWBGroupSpec(doc='Nested Folder',
                                             #                      neurodata_type_inc='StimulusSetReferencedFolder',
                                             #                      quantity='*')
                                             #        ],
                                             )

    stimset_referenced = NWBGroupSpec(doc='Additional stimulus set waveform data is store here in tree structure.',
                                      neurodata_type_def='StimulusSetReferenced',
                                      groups=[NWBGroupSpec(doc='Folder',
                                                           neurodata_type_inc='StimulusSetReferencedFolder',
                                                           quantity='*')
                                             ])

    # END custom wave handling

    stimsets = NWBGroupSpec(doc='Stimulus Sets: Parameter waves, referenced custom waves and third-party stimsets',
                            neurodata_type_def='StimulusSets',
                            groups = [NWBGroupSpec(doc='Additional stimulus set waveform data is store here in tree structure.',
                                                   neurodata_type_inc='StimulusSetReferenced')
                                     ],
                            datasets=[NWBDatasetSpec(doc='Stimulus set parameters for the full set. '
                                                     'See also https://alleninstitute.github.io/MIES/file/_m_i_e_s___wave_data_folder_getters_8ipf.html#_CPPv418GetSegmentTypeWavev.',
                                                     neurodata_type_inc='StimulusSetWavebuilderSegmentTypes',
                                                     quantity='*'),
                                      NWBDatasetSpec(doc='Textual part of the stimulus set parameter waves for recreating the stimset in MIES. '
                                                     'Rows are the data entries, Columns are the index of the segment/epoch (last index holds '
                                                     'settings for the full set) and Layers hold different stimulus waveform types. '
                                                     'See also https://alleninstitute.github.io/MIES/file/_m_i_e_s___wave_data_folder_getters_8ipf.html#_CPPv427GetWaveBuilderWaveTextParamv.',
                                                     neurodata_type_inc='StimulusSetWavebuilderParameterText',
                                                     quantity='*'),
                                      NWBDatasetSpec(doc='Numerical part of the stimulus set parameter waves for recreating the stimset in MIES. '
                                                     'Rows are the data entries, Columns are the index of the segment/epoch '
                                                     'and Layers hold different stimulus waveform types. '
                                                     'See also https://alleninstitute.github.io/MIES/file/_m_i_e_s___wave_data_folder_getters_8ipf.html#_CPPv423GetWaveBuilderWaveParamv.',
                                                     neurodata_type_inc='StimulusSetWavebuilderParameter',
                                                     quantity='*'),
                                      NWBDatasetSpec(doc='Stimulus set waveform data. This is only present if not all three parameter waves could be found '
                                                     'or a third-party stimset was used. One column per sweep.',
                                                     neurodata_type_inc='StimulusSetWaveform',
                                                     quantity='*'),
                                      ]
                            )

    textual_keys = NWBDatasetSpec(doc='Textual labnotebook keys: First row is the name, second row is the unit and third row is the tolerance. '
                                  'Columns are the running index. '
                                  'See also https://alleninstitute.github.io/MIES/labnotebook-docs.html.',
                                  neurodata_type_def='LabNotebookTextualKeys',
                                  neurodata_type_inc='NWBData',
                                  shape=(3, None))

    textual_values = NWBDatasetSpec(doc='Textual labnotebook values: Rows are the '
                                    'running index, Columns hold the different entry names, Layers (up to nine) hold '
                                    'the headstage dependent data in the first 8 and the headstage independent data in the 9th layer. '
                                    'See also https://alleninstitute.github.io/MIES/labnotebook-docs.html.',
                                    neurodata_type_def='LabNotebookTextualValues',
                                    neurodata_type_inc='NWBData',
                                    shape=(None, None, None))

    numerical_keys = NWBDatasetSpec(doc='Numerical labnotebook keys: First row is the name, second row is the unit and third row is the tolerance. '
                                    'Columns are the running index. '
                                    'See also https://alleninstitute.github.io/MIES/labnotebook-docs.html.',
                                    neurodata_type_def='LabNotebookNumericalKeys',
                                    neurodata_type_inc='NWBData',
                                    shape=(3, None))

    numerical_values = NWBDatasetSpec(doc='Numerical labnotebook values: Rows are the '
                                      'running index, Columns hold the different entry names, Layers (up to nine) hold '
                                      'the headstage dependent data in the first 8 and the headstage independent data in the 9th layer. '
                                      'See also https://alleninstitute.github.io/MIES/labnotebook-docs.html.',
                                      neurodata_type_def='LabNotebookNumericalValues',
                                      neurodata_type_inc='NWBData',
                                      shape=(None, None, None))

    labnotebook_device = NWBGroupSpec(doc='Device for the labnotebooks',
                                      neurodata_type_def='LabNotebookDevice',
                                      neurodata_type_inc='Device',
                                      datasets=[NWBDatasetSpec(doc='Numerical labnotebook values: Rows are the '
                                                               'running index, Columns hold the different entry names, Layers (up to nine) hold '
                                                               'the headstage dependent data in the first 8 and the headstage independent data in the 9th layer. '
                                                               'See also https://alleninstitute.github.io/MIES/labnotebook-docs.html.',
                                                               neurodata_type_inc='LabNotebookNumericalValues'),
                                                NWBDatasetSpec(doc='Numerical labnotebook keys: First row is the name, second row is the unit and third row is the tolerance. '
                                                               'Columns are the running index. '
                                                               'See also https://alleninstitute.github.io/MIES/labnotebook-docs.html.',
                                                               neurodata_type_inc='LabNotebookNumericalKeys'),
                                                NWBDatasetSpec(doc='Textual labnotebook keys: First row is the name, second row is the unit and third row is the tolerance. '
                                                               'Columns are the running index. '
                                                               'See also https://alleninstitute.github.io/MIES/labnotebook-docs.html.',
                                                               neurodata_type_inc='LabNotebookTextualKeys'),
                                                NWBDatasetSpec(doc='Textual labnotebook values: Rows are the '
                                                               'running index, Columns hold the different entry names, Layers (up to nine) hold '
                                                               'the headstage dependent data in the first 8 and the headstage independent data in the 9th layer. '
                                                               'See also https://alleninstitute.github.io/MIES/labnotebook-docs.html.',
                                                               neurodata_type_inc='LabNotebookTextualValues')
                                                ])

    labnotebook = NWBGroupSpec(doc='Labnotebooks',
                               neurodata_type_def='LabNotebook',
                               groups=[NWBGroupSpec(doc='Device for the labnotebooks',
                                                    neurodata_type_inc='LabNotebookDevice')
                                      ])

    # Since 05cb3ffe (NWB: Export single test pulses as well on interactive use, 2017-11-07)

    stored_testpulses = NWBDatasetSpec(doc='Raw AD testpulse data',
                                       neurodata_type_def='TestpulseRawData',
                                       neurodata_type_inc='NWBData',
                                       shape=(None,))

    # See da33596f (Rework TPStorage completely, 2018-10-18) for the switch
    # from active AD to headstages
    #
    # Since 916f26e4 (TPStorage: Keep all data in one wave, 2018-10-17) we
    # only have one TPStorage

    tpstorage = NWBDatasetSpec(doc='Metadata about the Testpulse: Rows are the running index, Columns are active AD channels '
                               '(up to version <= 7) or headstages (version >= 8), the data is in the Layers.',
                               neurodata_type_def='TestpulseMetadata',
                               neurodata_type_inc='NWBData',
                               shape=(None, None, None))

    testpulse_device = NWBGroupSpec(doc='Device for the testpulse data',
                                    neurodata_type_def='TestpulseDevice',
                                    datasets=[NWBDatasetSpec(doc='Metadata about the Testpulse: Rows are the running index, Columns are active AD channels '
                                                             '(up to version <= 7) or headstages (version >= 8), the data is in the Layers.',
                                                             neurodata_type_inc='TestpulseMetadata',
                                                             quantity='*'),
                                              NWBDatasetSpec(doc='Raw AD testpulse data',
                                                             neurodata_type_inc='TestpulseRawData',
                                                             quantity='*')
                                             ])

    testpulse = NWBGroupSpec(doc='Testpulse data',
                             neurodata_type_def='Testpulse',
                             groups=[NWBGroupSpec(doc='Device for the testpulse data',
                                                  neurodata_type_inc='TestpulseDevice')
                                    ])

    user_comment_device_string = NWBDatasetSpec('device specific user text notes',
                                                neurodata_type_def='UserCommentString',
                                                neurodata_type_inc='NWBData')

    user_comment_device = NWBGroupSpec('Device for the user text notes',
                                       neurodata_type_def='UserCommentDevice',
                                       neurodata_type_inc='Device',
                                       datasets=[NWBDatasetSpec('device specific user text notes',
                                                                neurodata_type_inc='UserCommentString')
                                                ])

    user_comment = NWBGroupSpec(doc='Free form text notes from the experimenter',
                                neurodata_type_def='UserComment',
                                groups=[NWBGroupSpec('Device for the user text notes',
                                                     neurodata_type_inc='UserCommentDevice')
                                       ])

    generated_by = NWBDatasetSpec(doc='Software provenance information as key '
                                  '(first column) value (second column) pairs.',
                                  neurodata_type_def='GeneratedBy',
                                  neurodata_type_inc='NWBData',
                                  shape=(None, 2))

    mies_general = NWBGroupSpec(doc='Additional data and metadata from MIES',
                                neurodata_type_def='MIESMetaData',
                                neurodata_type_inc='LabMetaData',
                                datasets=[NWBDatasetSpec(doc='Software provenance information as key (first column) value (second column) pairs.',
                                                         neurodata_type_inc='GeneratedBy')
                                         ],
                                groups=[NWBGroupSpec(doc='Free form text notes from the experimenter',
                                                     neurodata_type_inc='UserComment',
                                                     quantity='?'),
                                        NWBGroupSpec(doc='Testpulse data',
                                                     neurodata_type_inc='Testpulse',
                                                     quantity='?'),
                                        NWBGroupSpec(doc='Labnotebooks',
                                                     neurodata_type_inc='LabNotebook'),
                                        NWBGroupSpec(doc='Stimulus Sets: Parameter waves, referenced custom waves and third-party stimsets',
                                                     neurodata_type_inc='StimulusSets',
                                                     quantity='?'),
                                       ])

    # these arguments were auto-generated from your cookiecutter inputs
    ns_builder=NWBNamespaceBuilder(
        doc=("""An NWB:N extension for data and metadata from the Multichannel Igor Electrophysiology Suite (MIES)"""),
        name="""ndx-mies""",
        version="""0.1.0""",
        author=list(map(str.strip, """Thomas Braun""".split(','))),
        contact=list(map(str.strip, """thomas.braun@byte-physics.de""".split(',')))
    )

    # include referenced types
    # ns_builder.include_type('Data', namespace='hdmf-common')
    # ns_builder.include_type('Container', namespace='hdmf-common')
    # ns_builder.include_type('DynamicTable', namespace='hdmf-common')
    # ns_builder.include_type('NWBData', namespace='core')
    # ns_builder.include_type('NWBDataInterface', namespace='core')
    # ns_builder.include_type('NWBFile', namespace='core')
    # ns_builder.include_type('NWBContainer', namespace='core')
    # ns_builder.include_type('LabMetaData', namespace='core')
    # ns_builder.include_type('Units', namespace='core')
    # ns_builder.include_type('ProcessingModule', namespace='core')
    # ns_builder.include_type('TimeSeries', namespace='core')
    # ns_builder.include_type('Subject', namespace='core')
    # ns_builder.include_type('Device', namespace='core')
    # ns_builder.include_type('SweepTable', namespace='core')
    # ns_builder.include_type('VectorData', namespace='core')
    # ns_builder.include_type('VectorIndex', namespace='core')
    # ns_builder.include_type('Index', namespace='core')
    # ns_builder.include_type('ElementIdentifiers', namespace='core')
    # ns_builder.include_type('IntracellularElectrode', namespace='core')

    # add all of your new data types to this list
    new_data_types=[user_comment, user_comment_device,
                      user_comment_device_string, testpulse, testpulse_device, tpstorage,
                      generated_by, stored_testpulses, labnotebook,
                      numerical_values, numerical_keys, textual_values, textual_keys,
                      stimsets, stimset_waveform, stimset_parameter_numerical, stimset_parameter_textual, stimset_parameter_segments,
                      stimset_referenced, stimset_referenced_folder, stimset_referenced_waveform,
                      labnotebook_device, mies_general]

    # export the spec to yaml files in the spec folder
    output_dir=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'spec'))
    export_spec(ns_builder, new_data_types, output_dir)


if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
