#!/bin/bash

DATASET=$1
INPUTFILE=$2
YEAR=$3
DATA_MC=$4
INPUTFILEAREA=http://stash.osgconnect.net/+qilongguo/gKK/private_NanoAOD/V1

BASEDIR=`pwd`
echo wget --tries=3 --no-check-certificate $INPUTFILEAREA/$DATASET/$INPUTFILE
wget --tries=3 --no-check-certificate $INPUTFILEAREA/$DATASET/$INPUTFILE
if [ ! -f "$BASEDIR/$INPUTFILE" ]; then
echo $BASEDIR/$INPUTFILE "not exit"
exit 1
else
echo $BASEDIR/$INPUTFILE
fi

echo "base dir"
pwd
ls -lth

export SCRAM_ARCH=slc7_amd64_gcc700
source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_10_6_26/src ] ; then
  echo release CMSSW_10_6_26 already exists
else
  scram p CMSSW CMSSW_10_6_26
fi
cd CMSSW_10_6_26/src
eval `scram runtime -sh`

cd $CMSSW_BASE/src
git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
cd PhysicsTools/NanoAODTools
cmsenv
scram b

echo "PhysicsTools/NanoAODTools dir"
pwd
ls -lth

cd python/postprocessing
git clone https://github.com/gqlcms/XWWNano.git analysis
cd $CMSSW_BASE/src
scram b

cd $CMSSW_BASE/src/PhysicsTools/NanoAODTools/python/postprocessing/analysis
echo "analysis dir"
pwd
ls -lth
source $CMSSW_BASE/src/PhysicsTools/NanoAODTools/python/postprocessing/analysis/init.sh

cd $CMSSW_BASE/src/PhysicsTools/NanoAODTools/python/postprocessing/analysis/test
echo "analysis/test dir"
pwd
ls -lth

echo python run.py -$DATA_MC -i $BASEDIR/$INPUTFILE -o ./ --year $YEAR
python run.py -$DATA_MC -i $BASEDIR/$INPUTFILE -o ./ --year $YEAR

echo "finish run"
echo "analysis/test dir"
pwd
ls -lth

mv tree.root $BASEDIR

cd $BASEDIR
ls -lth