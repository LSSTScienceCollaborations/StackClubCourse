import numpy as np
import pandas as pd

from lsst.daf.persistence import Butler

############################################################

REPO = '/datasets/hsc/repo/rerun/RC/w_2020_19/DM-24822'
TRACT = 9615
FILTERS = ['HSC-G', 'HSC-R', 'HSC-I']
PATCHES = ['0,0', '0,1', '0,2', 
           '1,0', '1,1', '1,2',
           '2,0', '2,1', '2,2']
SELECTED_COLUMNS = ['id',
                    'coord_ra', 
                    'coord_dec',
                    'modelfit_CModel_instFlux',
                    'modelfit_CModel_instFluxErr',
                    'base_PsfFlux_instFlux',
                    'base_PsfFlux_instFluxErr',
                    'base_ClassificationExtendedness_flag',
                    'base_ClassificationExtendedness_value',
                    'base_SdssCentroid_flag',
                    'base_PixelFlags_flag_interpolated',
                    'base_PixelFlags_flag_saturated',
                    'base_PsfFlux_flag',
                    'modelfit_CModel_flag']

# SHORTCUT = True for quick evaluation but lower statistics, 
# SHORTCUT = False to get all the objects from all the patches in the tract (~10 mins)
SHORTCUT = True

############################################################

def getData():
    """
    Assemble a catalog of forced source measurements for a 
    set of coadd objects observed in multiple bands.
    
    Returns
    -------
    data : dict
        dict of Pandas DataFrames containing catalog for
        each band
    """
        
    butler = Butler(REPO)

    skymap = butler.get('deepCoadd_skyMap')
    patch_array = []
    for ii in range(skymap.generateTract(TRACT).getNumPatches()[0]):
        for jj in range(skymap.generateTract(TRACT).getNumPatches()[1]):
            patch_array.append('%s,%s'%(ii, jj))
    tract_array = np.tile(TRACT, len(patch_array))

    if SHORTCUT:
        # Only get a few patches
        df_tract_patch = pd.DataFrame({'tract': len(PATCHES) * [TRACT],
                                       'patch': PATCHES})
    else:
        # Get all the object catalogs from one tract
        df_tract_patch = pd.DataFrame({'tract': tract_array,
                                       'patch': patch_array})
    
    data = {}
    for band in FILTERS:
        coadd_array = []
        selection_array = []
        for ii in range(0, len(df_tract_patch)):
            tract, patch = df_tract_patch['tract'][ii], df_tract_patch['patch'][ii] 
            print(band, tract, patch)
            dataid = {'filter':band, 'tract':tract, 'patch':patch}
            coadd_ref = butler.get('deepCoadd_ref', dataId=dataid)
            coadd_forced_src = butler.get('deepCoadd_forced_src', dataId=dataid)
            coadd_calib = butler.get('deepCoadd_calexp_photoCalib', dataId=dataid)
    
            selected_rows = coadd_ref['detect_isPrimary']
    
            print(np.sum(selected_rows))
            coadd_array.append(coadd_forced_src.asAstropy().to_pandas().loc[selected_rows, SELECTED_COLUMNS])
            coadd_array[-1]['psf_mag'] = coadd_calib.instFluxToMagnitude(coadd_forced_src[selected_rows], 'base_PsfFlux')[:,0]
            coadd_array[-1]['cm_mag'] = coadd_calib.instFluxToMagnitude(coadd_forced_src[selected_rows], 'modelfit_CModel')[:,0]
    
        data[band] = pd.concat(coadd_array)
    
    # Require good quality measurements in all bands
    selected_rows = []
    for band in FILTERS:
        # Signal-to-noise ratio
        snr = data[band]['modelfit_CModel_instFlux'] / data[band]['modelfit_CModel_instFluxErr']
        
        selected_rows.append(~data[band]['base_SdssCentroid_flag'] 
                             & ~data[band]['base_PixelFlags_flag_interpolated']
                             & ~data[band]['base_PixelFlags_flag_saturated']
                             & ~data[band]['base_PsfFlux_flag']
                             & ~data[band]['modelfit_CModel_flag']
                             & (snr > 10.))
    selected_rows = np.all(selected_rows, axis=0)

    for band in FILTERS:
        data[band] = data[band].loc[selected_rows]
        
    return data

############################################################