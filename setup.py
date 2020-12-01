#!/usr/bin/env python
# coding=utf-8


from setuptools import setup

setup(
    name='openmonkeymind',
    version='0.1.0',
    description='OpenMonkeyMind plugins and extension for OpenSesame',
    author='Sebastiaan Mathot',
    author_email='s.mathot@cogsci.nl',
    url='https://github.com/open-cogsci/omm-client',
    classifiers=[
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
    ],
    packages=['openmonkeymind'],
    data_files=[
        (
            'share/opensesame_extensions/OpenMonkeyMind',
            [
                'opensesame_extensions/OpenMonkeyMind/OpenMonkeyMind.py',
                'opensesame_extensions/OpenMonkeyMind/omm-entry-point.osexp',
                'opensesame_extensions/OpenMonkeyMind/omm-template.osexp',
                'opensesame_extensions/OpenMonkeyMind/info.yaml',
                'opensesame_extensions/OpenMonkeyMind/openmonkeymind.ui'
            ]
        ),
        (
            'share/opensesame_plugins/OMMAnnounce',
            [
                'opensesame_plugins/OMMAnnounce/OMMAnnounce.png',
                'opensesame_plugins/OMMAnnounce/OMMAnnounce_large.png',
                'opensesame_plugins/OMMAnnounce/OMMAnnounce.py',
                'opensesame_plugins/OMMAnnounce/info.yaml',
            ]
        ),
        (
            'share/opensesame_plugins/OMMRequestJob',
            [
                'opensesame_plugins/OMMRequestJob/OMMRequestJob_large.png',
                'opensesame_plugins/OMMRequestJob/OMMRequestJob.png',
                'opensesame_plugins/OMMRequestJob/OMMRequestJob.py',
                'opensesame_plugins/OMMRequestJob/info.yaml',
            ]
        ),
        (
            'share/opensesame_plugins/OMMDetectParticipant',
            [
                'opensesame_plugins/OMMDetectParticipant/OMMDetectParticipant_large.png',
                'opensesame_plugins/OMMDetectParticipant/OMMDetectParticipant.png',
                'opensesame_plugins/OMMDetectParticipant/OMMDetectParticipant.py',
                'opensesame_plugins/OMMDetectParticipant/info.yaml',
            ]
        ),
        (
            'share/opensesame_plugins/OMMConditioner',
            [
                'opensesame_plugins/OMMConditioner/OMMConditioner_large.png',
                'opensesame_plugins/OMMConditioner/OMMConditioner.png',
                'opensesame_plugins/OMMConditioner/OMMConditioner.py',
                'opensesame_plugins/OMMConditioner/info.yaml',
            ]
        ),
        (
            'share/opensesame_plugins/OMMConditioner/conditioners',
            [
                'opensesame_plugins/OMMConditioner/conditioners/__init__.py',
                'opensesame_plugins/OMMConditioner/conditioners/_base_conditioner.py',
                'opensesame_plugins/OMMConditioner/conditioners/_dummy.py',
                'opensesame_plugins/OMMConditioner/conditioners/_seed_dispenser.py'
            ]
        )
    ]
)
