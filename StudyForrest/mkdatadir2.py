# Create session folder and make soft link of fmri data into run dir
import os
import re


def mkfreesurferdir(subid):
    """
    Make soft link of subs from studyforrest/rawdata/freesurfer to studyforrest/anat.

    Examples
    --------
        >>softlinkdir('sub001')
        softlink: '/nfs/s1/studyforrest/rawdata/freesurfer/sub-01/' >>> '/nfs/s1/studyforrest/anat/sub001'
    """
    rawsubid = mksubid('sub-', subid)
    newsubid = mksubid('sub0', subid)
    srcdir = '/nfs/s1/studyforrest/rawdata/freesurfer/'
    dstdir = '/nfs/s1/studyforrest/anat/'
    src = os.path.join(srcdir, rawsubid)
    dst = os.path.join(dstdir, newsubid)
    os.symlink(src, dst)


def mkphase2dir(subid, scan):
    """
    Make soft link of subid in phase2 from studyforrest/rawdata/ to studyforrest/.

    Examples
    --------
        >>mkphase2dir('sub001, ')
        softlink: '/nfs/s1/studyforrest/rawdata/phase2/sub-01/ses-movie/func/files'
                    >>> '/nfs/s1/studyforrest/sub001/audiovisual3T/runid/files'
    """
    scanlist['audiovisual3T'] = ['movie']
    scanlist['retinotopy3T'] = ['retmapccw', 'retmapclw', 'retmapcon', 'retmapexp']
    scanlist['localizer3T'] = ['movielocalizer', 'objectcategories']

    if scan not in scanlist:
        raise IOError('Parameter scan={0} is unavailable. \n'
                      'Available scan name: {1}'.format(scan, scanlist.keys()))

    rawrootdir = '/nfs/s1/studyforrest/rawdata'
    newrootdir = '/nfs/s1/studyforrest'
    rawsubid = mksubid('sub-', subid)
    newsubid = mksubid('sub0', subid)
    tasks = scanlist[scan]
    if scan == 'audiovisual3T':
        rawscan = 'ses-movie'
    else:
        rawscan = 'ses-localizer'
    softlinkphase2(rawrootdir, newrootdir, rawsubid, newsubid, rawscan, scan, tasks)


def softlinkphase2(rawrootdir, newrootdir, rawsubid, newsubid, rawscan, scan, tasks):
    """
    Make soft link of subid in phase2 from studyforrest/rawdata/ to studyforrest/.

    Examples
    --------
        >>mkphase2dir('sub001, ')
        softlink: '/nfs/s1/studyforrest/rawdata/phase2/sub-01/ses-movie/func/files'
                    >>> '/nfs/s1/studyforrest/sub001/audiovisual3T/runid/files'
    """
    for task in tasks:
        rawmodalitys = None
        newfilenames = None

        if task == 'movie':
            rawmodalitys = ['bold.nii.gz', 'events.tsv', 'eyelinkraw.asc.gz', 'recording-eyegaze_physio.tsv.gz']
            newfilenames = ['raw.nii.gz', 'events.tsv', 'eyelinkraw.asc.gz', 'eyegaze_physio.tsv.gz']

        if task == 'objectcategories':
            rawmodalitys = ['bold.nii.gz', 'recording-cardresp_physio.tsv.gz', 'events.tsv']
            newfilenames = [task+'_raw.nii.gz', task+'_cardresp_physio.tsv.gz', task+'_events.tsv']

        if task == 'movielocalizer':
            rawmodalitys = ['bold.nii.gz', 'recording-cardresp_physio.tsv.gz']
            newfilenames = ['movieframe_raw.nii.gz', 'movieframe_cardresp_physio.tsv.gz']

        if task in ['retmapccw', 'retmapclw', 'retmapcon', 'retmapexp']:
            rawmodalitys = ['bold.nii.gz', 'recording-cardresp_physio.tsv.gz']
            newfilenames = [task+'_raw.nii.gz', task+'_recording-cardresp_physio.tsv.gz']

        if not rawmodalitys or not newfilenames:
            raise ValueError("Please check input task name.")

        srcdir = os.path.join(rawrootdir, 'phase2', rawsubid, rawscan, 'func')
        dstdir = os.path.join(newrootdir, newsubid, scan)

        # TODO get runid
        
        for rawmodality, newfilename in zip(rawmodalitys, newfilenames):
            rawfilename = rawsubid + '_' + rawscan + '_task-' + task + '_run-' + runid + '_' + rawmodality
            src = os.path.join(srcdir, rawfilename)
            dst = os.path.join(dstdir, newfilename)
            os.symlink(src, dst)

def mksubid(prefix, subid):
    """
    Use 'prefix' and the last two number of 'subid' to make new subid.

    Examples
    --------
        >>mkrawsubid('sub0', 'sub-01')
            sub001
        >>mkrawsubid('sub-', 'sub001')
            sub-01
    """
    if not isinstance(subid, str):
        subid = str(subid)

    subnum = ''.join(re.findall('[0-9]', subid)[-2:])  # find the last two number of subid
    while len(subnum) < 2:
        subnum = '0' + subnum
    return prefix + subnum


if __name__ == '__main__':
    path_source='/nfs/s1/studyforrest/rawdata'
    path_target='/nfs/s1/studyforrest'
    rawsublist = ['sub-01', 'sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06', 'sub-07', 'sub-08', 'sub-09', 'sub-10', 'sub-11', 'sub-12', 'sub-13', 'sub-14', 'sub-15', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20']
    runidlist = ["001", "002", "003", "004", "005", "006", "007", "008"]

    # softlink freesurfer anat
    path_dst = os.path.join(path_target, 'anat')
    for rawsubid in rawsublist:
        softlinkdir(path_source, 'freesurfer', rawsubid, '', path_dst, '')

    # softlink phase2 movie and localizer data
    phase2_moviemodality = ['bold.nii.gz', 'defacemask.nii.gz', 'events.tsv', 'eyelinkraw.asc.gz', 'recording-eyegaze_physio.tsv.gz']
    phase2_localizermodality = ['bold.nii.gz', 'defacemask.nii.gz', 'recording-cardresp_physio.tsv.gz']
    phase2_localizertask = ['movielocalizer', 'objectcategories']
    phaes2_retinotask = ['retmapccw', 'retmapclw', 'retmapcon', 'retmapexp']

    softlinkphase2(rawrootdir=path_source, rawdataname='phase2', rawsubid='sub-01', rawfsub='ses-movie', rawtask='movie', rawrunid='1', modality=moviemodality, newrootdir=path_target, newfsub='audiovisual3T', newtask='')
    softlinkphase2(rawrootdir=path_source, rawdataname='phase2', rawsubid='sub-01', rawfsub='ses-localizer', localizertask, rawrunid='1', modality=localizermodality, newrootdir=path_target, newfsub='localizer3T', newtask=localizertask)
    softlinkphase2(rawrootdir=path_source, rawdataname='phase2', rawsubid='sub-01', rawfsub='ses-localizer', retinotask, rawrunid='1', modality=localizermodality, newrootdir=path_target, newfsub='retinotopy3T', newtask=localizertask)

    # softlink T1w, T2w, SWI, Angio
    struct_modality = ['highres001.nii.gz', 't2w001.nii.gz', 'dti001.nii.gz', 'swi001_mag.nii.gz', 'swi001_pha.nii.gz', 'angio001.nii.gz']
    newfsublist = {'highres001.nii.gz': 't1w3T', 't2w001.nii.gz': 't2w3T', 'dti001.nii.gz': 'dti3T', 'swi001_mag.nii.gz': 'swi3T', 'swi001_pha.nii.gz': 'swi3T', 'angio001.nii.gz': 'angiography7T'}
    rawfsublist = ['anatomy', 'anatomy/other']
    softlinkstruct(path_source, 'phase1', 'sub001', rawfsub, modality, newrootdir=path_target, newfsub=newfsublist[modality])

