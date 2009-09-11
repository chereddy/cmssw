import FWCore.ParameterSet.Config as cms

# Set the HLT paths
import HLTrigger.HLTfilters.hltHighLevel_cfi
ALCARECOSiStripCalZeroBiasHLT = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone(
    andOr = True, # choose logical OR between Triggerbits
#    HLTPaths = [
#        #SiStripCalZeroBias
#        "HLT_ZeroBias",
#        #Random Trigger for Cosmic Runs
#        'RandomPath'
#        ],
    eventSetupPathsKey='SiStripCalZeroBias',
    throw = False # tolerate triggers stated above, but not available
)

# Include masking only from Cabling and O2O
import CalibTracker.SiStripESProducers.SiStripQualityESProducer_cfi
siStripQualityESProducerUnbiased = CalibTracker.SiStripESProducers.SiStripQualityESProducer_cfi.siStripQualityESProducer.clone()
siStripQualityESProducerUnbiased.appendToDataLabel = 'unbiased'
siStripQualityESProducerUnbiased.ListOfRecordToMerge = cms.VPSet(
    cms.PSet(
        record = cms.string( 'SiStripDetCablingRcd' ), # bad components from cabling
        tag = cms.string( '' )
    ),
    cms.PSet(
        record = cms.string( 'SiStripBadChannelRcd' ), # bad components from O2O
        tag = cms.string( '' )
    )
)


# Clusterizer #
import RecoLocalTracker.SiStripClusterizer.SiStripClusterizer_cfi 

ZeroBiasClusterizer = cms.PSet(
    Algorithm = cms.string('ThreeThresholdAlgorithm'),
    ChannelThreshold = cms.double(2.0),
    SeedThreshold = cms.double(3.0),
    ClusterThreshold = cms.double(5.0),
    MaxSequentialHoles = cms.uint32(0),
    MaxSequentialBad = cms.uint32(1),
    MaxAdjacentBad = cms.uint32(0),
    QualityLabel = cms.string('unbiased')
    )


calZeroBiasClusters = RecoLocalTracker.SiStripClusterizer.SiStripClusterizer_cfi.siStripClusters.clone()
calZeroBiasClusters.Clusterizer = ZeroBiasClusterizer

# Not persistent collections needed by the filters in the AlCaReco DQM
import DPGAnalysis.SiStripTools.eventwithhistoryproducerfroml1abc_cfi
ConsecutiveHEs = DPGAnalysis.SiStripTools.eventwithhistoryproducerfroml1abc_cfi.consecutiveHEs.clone()

import DPGAnalysis.SiStripTools.apvcyclephaseproducerfroml1abc_GR09_cfi
apvPhases = DPGAnalysis.SiStripTools.apvcyclephaseproducerfroml1abc_GR09_cfi.APVPhases.clone()

import DPGAnalysis.SiStripTools.apvlatency.fakeapvlatencyessource_cfi
fakeApvLatency = DPGAnalysis.SiStripTools.apvlatency.fakeapvlatencyessource_cfi.fakeapvlatency.clone()
fakeApvLatency.APVLatency = cms.untracked.int32(143)

essapvlatency = cms.ESSource("EmptyESSource",
                              recordName = cms.string("APVLatencyRcd"),
                              firstValid = cms.vuint32(1),
                              iovIsRunNotTime = cms.bool(True)
                              )

# SiStripQuality (only to test the different data labels)#
qualityStatistics = cms.EDFilter("SiStripQualityStatistics",
    TkMapFileName = cms.untracked.string(''),
    dataLabel = cms.untracked.string('unbiased')
)

# Sequence #
seqALCARECOSiStripCalZeroBias = cms.Sequence(ALCARECOSiStripCalZeroBiasHLT*calZeroBiasClusters*apvPhases*ConsecutiveHEs)
