def mksublist(prefix, numlist):
    sublist = numlist
    for i, subid in enumerate(numlist):
        sublist[i] = str(subid)
        while len(sublist[i]) < 3:
            sublist[i] = "0" + sublist[i]
        sublist[i] = prefix + sublist[i]
    return sublist

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

