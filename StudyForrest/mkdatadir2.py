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
        rawmodalitys, newfilenames = split_task(task)

        if not rawmodalitys or not newfilenames:
            raise ValueError("Please check input task name.")

        srcdir = os.path.join(rawrootdir, 'phase2', rawsubid, rawscan, 'func')
        dstdir = os.path.join(newrootdir, newsubid, scan)

        for rawmodality, newfilename in zip(rawmodalitys, newfilenames):
            """Find runid from files."""
            files = os.listdir(srcdir)
            rawrunids = re.search('_run-[0-9]_{0}'.format(rawmodality), files).group()
            rawrunidlist = re.search('[0-9]', rawrunids).group()

            for rawrunid in rawrunidlist:
                rawfilename = rawsubid + '_' + rawscan + '_task-' + task + '_run-' + rawrunid + '_' + rawmodality
                newrunid = mkrunid(rawrunid)
                src = os.path.join(srcdir, rawfilename)
                dst = os.path.join(dstdir, newrunid, newfilename)
                os.symlink(src, dst)
        

def mksubid(prefix, subid, idlength=2):
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
    while len(subnum) < idlength:
        subnum = '0' + subnum
    return prefix + subnum


def mkrunid(runid, idlength=3):
    runid_str = str(runid)
    while len(runid_str) < idlength:
        runid_str = '0' + runid_str
    return runid_str


def split_task(task):
    rawmodalitys = None
    newfilenames = None

    if task == 'movie':
        rawmodalitys = ['bold.nii.gz', 'events.tsv', 'eyelinkraw.asc.gz', 'recording-eyegaze_physio.tsv.gz']
        newfilenames = ['raw.nii.gz', 'events.tsv', 'eyelinkraw.asc.gz', 'eyegaze_physio.tsv.gz']

    if task == 'objectcategories':
        rawmodalitys = ['bold.nii.gz', 'recording-cardresp_physio.tsv.gz', 'events.tsv']
        newfilenames = [task + '_raw.nii.gz', task + '_cardresp_physio.tsv.gz', task + '_events.tsv']

    if task == 'movielocalizer':
        rawmodalitys = ['bold.nii.gz', 'recording-cardresp_physio.tsv.gz']
        newfilenames = ['movieframe_raw.nii.gz', 'movieframe_cardresp_physio.tsv.gz']

    if task in ['retmapccw', 'retmapclw', 'retmapcon', 'retmapexp']:
        rawmodalitys = ['bold.nii.gz', 'recording-cardresp_physio.tsv.gz']
        newfilenames = [task + '_raw.nii.gz', task + '_recording-cardresp_physio.tsv.gz']

    return rawmodalitys, newfilenames

