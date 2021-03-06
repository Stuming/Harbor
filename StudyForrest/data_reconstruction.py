# Create session folder and make soft link of fmri data into run dir
import os
import re


def mkfreesurferdir(subid):
    """
    Make soft link of subs from studyforrest/rawdata/freesurfer to studyforrest/anat.

    Parameters
    ----------
        subid: the id of subjects that want to build dir for, determined by subid in rawdata/freesurfer/
                or studyforrest/subid, sub001 or sub-01 is acceptable.

    Examples
    --------
        >>softlinkdir('sub001')
        softlink: '/nfs/s1/studyforrest/rawdata/freesurfer/sub-01/' >>> '/nfs/s1/studyforrest/anat/sub001'
    """
    rawsubid = mksubid('sub-', subid)
    newsubid = mksubid('sub0', subid)
    srcdir = '/nfs/s1/studyforrest/rawdata/freesurfer/'
    dstdir = '/nfs/s1/studyforrest/anat/'

    if not os.path.exists(dstdir):
        os.makedirs(dstdir)

    src = os.path.join(srcdir, rawsubid)
    dst = os.path.join(dstdir, newsubid)

    print("Soft link from {0} to {1}".format(src, dst))
    os.symlink(src, dst)


def mkphase2dir(subid, scan):
    """
    Make soft link of subid in phase2 from studyforrest/rawdata/ to studyforrest/.
    This function prepare the dir info based on `subid` and `scan`, make dir is doing by softlinkphase2().

    Parameters
    ----------
        subid: the id of subjects that want to build dir for, determined by subid in rawdata/freesurfer/
                or studyforrest/subid, sub001 or sub-01 is acceptable.
        scan: the name behind studyforrest/subid/, for phase2 data, scan name should be one of
                ['audiovisual3T', 'retinotopy3T', 'localizer3T'].

    Examples
    --------
        >>mkphase2dir('sub001, ')
        softlink: '/nfs/s1/studyforrest/rawdata/phase2/sub-01/ses-movie/func/files'
                    >>> '/nfs/s1/studyforrest/sub001/audiovisual3T/runid/files'
    """
    # different dst scan has different tasks, specify them by scanlist.
    scanlist = dict(audiovisual3T=None, retinotopy3T=None, localizer3T=None)
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

    # specify the src scan by dst scan
    if scan == 'audiovisual3T':
        rawscan = 'ses-movie'
    else:
        rawscan = 'ses-localizer'

    # doing soft link
    softlinkphase2(rawrootdir, newrootdir, rawsubid, newsubid, rawscan, scan, tasks)


def softlinkphase2(rawrootdir, newrootdir, rawsubid, newsubid, rawscan, scan, tasks):
    """
    Make soft link of every chosen file in phase2 from studyforrest/rawdata/ to studyforrest/.

    Parameters
    ----------
        rawrootdir: the rawdata dir path, also the parent dir of phase2.
        newrootdir: the newdata dir path, also the parent dir of newsubid.
        rawsubid: subid in raw data.
        newsubid: subid in newrootdir.
        rawscan: 'ses-movie' or 'ses-localizer' in raw data.
        scan: new scan name.
        tasks: the task list that could specify files under scan.
    """
    for task in tasks:
        rawmodalitys, newfilenames = split_task(task)  # split task to get more info.

        if not rawmodalitys or not newfilenames:
            raise ValueError("Please check input task name.")

        srcdir = os.path.join(rawrootdir, 'phase2', rawsubid, rawscan, 'func')
        dstdir = os.path.join(newrootdir, newsubid, scan)

        for rawmodality, newfilename in zip(rawmodalitys, newfilenames):
            """soft link each rawmodality file into newfilename."""

            # Get runid from files.
            rawrunidlist = []
            for files in os.listdir(srcdir):
                rawrunids = re.search(r'_run-[0-9]_{0}'.format(rawmodality), files)
                if rawrunids:
                    rawrunidlist.append(re.search(r'[0-9]', rawrunids.group(0)).group(0))
            rawrunidlist = list(set(rawrunidlist))  # remove duplicate runid

            for rawrunid in rawrunidlist:
                rawfilename = rawsubid + '_' + rawscan + '_task-' + task + '_run-' + rawrunid + '_' + rawmodality
                newrunid = mkrunid(rawrunid)
                src = os.path.join(srcdir, rawfilename)
                dst = os.path.join(dstdir, newrunid, newfilename)

                if not os.path.exists(os.path.join(dstdir, newrunid)):
                    os.makedirs(os.path.join(dstdir, newrunid))

                print("Soft link from {0} to {1}".format(src, dst))
                os.symlink(src, dst)


def mksubid(prefix, subid, idlength=2):
    """
    Use 'prefix' and the last two number of 'subid' to make new subid.

    Parameters
    ----------
        prefix: prefix before new format of subid.
        subid: id number.
        idlength: determine the length of id number.

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
    """
    Build new format of runid by given idlength.

    Parameters
    ----------
        runid: id number.
        idlength: determine the length of id number.

    Examples
    --------
        >>>mkrunid(1)
            001
        >>>mkrunid('5', idlength=2)
            05
    """
    runid_str = str(runid)
    while len(runid_str) < idlength:
        runid_str = '0' + runid_str
    return runid_str


def split_task(task):
    """
    Get raw modalitys and the corresponding newfilename by the raw task.
    If task is not specified, return None.

    Parameters
    ----------
        task: task name of raw data, should be one of
                ['movie', 'objectcategories', 'retmapccw', 'retmapclw', 'retmapcon', 'retmapexp']

    Return
    ------
        rawmodalitys: unified post part of raw data filename.
        newfilenames: new filename of dst file.
    """
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

