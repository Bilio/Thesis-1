#!/usr/bin/env python
# -*- coding: utf-8 -*-

#---------#
# Imports #
#---------#

import sys
import os
import errno

#-------------------#
# utility functions #
#-------------------#

def createDirectory(dirPath):
    """ Create directory at a given path (absolute).

    Args:
        dirPath (str): absolute path for new directory.
    """
    if not os.path.exists(os.path.expanduser(dirPath)):
        try:
            os.makedirs(os.path.expanduser(dirPath))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise

#---------------------#
# Working Directories #
#---------------------#

thesisBaseDir     = '/home/pierpaolo/Documents/University/6_Anno_Poli/7_Thesis/'
paramBaseDir      = thesisBaseDir + 'Data/Parameters/'
inputBaseDir      = thesisBaseDir + 'Data/Input/'
outputBaseDir     = thesisBaseDir + 'Data/Output/'
debugBaseDir      = thesisBaseDir + 'Data/Debug/'
postProcessingDir = thesisBaseDir + 'Code/Postprocessing/'

#-----------------------#
# Experiment parameters #
#-----------------------#

params = {'riskFreeRate'      : 0.0,
          'deltaP'            : 0.0000,
          'deltaF'            : 0.0,
          'deltaS'            : 0.0000,
          'numDaysObserved'   : 5,
          'lambda'            : 0.9,
          'alphaConstActor'   : 1.0,
          'alphaExpActor'     : 0.8,
          'alphaConstCritic'  : 1.0,
          'alphaExpCritic'    : 0.7,
          'alphaConstBaseline': 1.0,
          'alphaExpBaseline'  : 0.6,
          'numExperiments'    : 5,
          'numEpochs'         : 1001,
          'numTrainingSteps'  : 1000,
          'numTestSteps'      : 100}

riskSensitive = False
synthetic     = False
multiAsset    = False

#--------------------------------------#
# Input, Output and Debug destinations #
#--------------------------------------#

if synthetic:
    if not multiAsset:
        inputFile = 'synthetic.csv'
    else:
        inputFile = 'cointegrated.csv'
else:
    if not multiAsset:
        inputFile = 'historical_single.csv'
    else:
        inputFile = 'historical_multi.csv'

inputFilePath = inputBaseDir + inputFile
print inputFilePath

experimentCode = ('Multi_' if multiAsset else 'Single_') + \
                 ('Synth_' if synthetic else 'Hist_') + \
                 ('RS_' if riskSensitive else 'RN_') + \
                 'P' + str(int(params['deltaP'] * 10000)) + '_' + \
                 'F' + str(int(params['deltaF'] * 10000)) + '_' + \
                 'S' + str(int(params['deltaS'] * 10000)) + '_' + \
                 'N' + str(params['numDaysObserved'])

outputDir = outputBaseDir + experimentCode + '/'
debugDir  = debugBaseDir + experimentCode + '/'

#-------------------------------#
# Write parameters to .pot file #
#-------------------------------#

parametersFile = paramBaseDir + experimentCode + '.pot'
with open(os.path.expanduser(parametersFile), 'w+') as f:
    for key, value in params.items():
        f.write('%s = %s\n' % (key, value))

#----------------------------------#
# Define list of algorithms to run #
#----------------------------------#

if riskSensitive:
    algorithmsList = ['RSARAC', 'RSPGPE', 'RSNPGPE']
else:
    algorithmsList = ['ARAC', 'PGPE', 'NPGPE']

#-------------------------#
# Run learning algorithms #
#-------------------------#

execPath = thesisBaseDir + 'Code/Thesis/examples/main_thesis'

for algo in algorithmsList:

    outputDirAlgo = outputDir + algo + '/'
    createDirectory(outputDirAlgo)

    debugDirAlgo  = debugDir + algo + '/'
    createDirectory(debugDirAlgo)

    os.system(execPath +
              " -a " + algo +
              " -p " + parametersFile +
              " -i " + inputFilePath +
              " -o " + outputDirAlgo +
              " -d " + debugDirAlgo)

#-------------------------#
# Postprocessing analysis #
#-------------------------#

sys.path.insert(0, "../Code/Postprocessing/")
from postprocessing import postprocessing

postprocessing(debugDir, outputDir)










