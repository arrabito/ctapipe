"""
Container structures for data that should be read or written to disk
"""

from astropy import units as u
from astropy.time import Time
from numpy import ndarray, nan

from ..core import Container, Field, Map
from ..instrument import SubarrayDescription

__all__ = ['InstrumentContainer',
           'R0Container',
           'R0CameraContainer',
           'R1Container',
           'R1CameraContainer',
           'DL0Container',
           'DL0CameraContainer',
           'DL1Container',
           'DL1CameraContainer',
           'MCEventContainer',
           'MCHeaderContainer',
           'MCCameraEventContainer',
           'CameraCalibrationContainer',
           'CentralTriggerContainer',
           'ReconstructedContainer',
           'ReconstructedShowerContainer',
           'ReconstructedEnergyContainer',
           'ParticleClassificationContainer',
           'DataContainer',
           'HillasParametersContainer']

# todo: change some of these Maps to be just 3D NDarrays?


class InstrumentContainer(Container):
    """Storage of header info that does not change with event. This is a
    temporary hack until the Instrument module and database is fully
    implemented.  Eventually static information like this will not be
    part of the data stream, but be loaded and accessed from
    functions.

    """

    subarray = Field(SubarrayDescription("MonteCarloArray"),
                     "SubarrayDescription from the instrument module")

    telescope_ids = Field([], "list of IDs of telescopes used in the run")
    pixel_pos = Field(Map(ndarray), "map of tel_id to pixel positions")
    optical_foclen = Field(Map(ndarray), "map of tel_id to focal length")
    mirror_dish_area = Field(Map(float), "map of tel_id to the area of the mirror dish", unit=u.m**2)
    mirror_numtiles = Field(Map(int), "map of tel_id to the number of tiles for the mirror")
    tel_pos = Field(Map(ndarray), "map of tel_id to telescope position")
    num_pixels = Field(Map(int), "map of tel_id to number of pixels in camera")
    num_channels = Field(Map(int), "map of tel_id to number of channels")




class DL1CameraContainer(Container):
    """Storage of output of camera calibration e.g the final calibrated
    image in intensity units and other per-event calculated
    calibration information.
    """
    image = Field(None, "np array of camera image", unit=u.electron)
    extracted_samples = Field(None, (
        "numpy array of bools indicating which samples were included in the "
        "charge extraction as a result of the charge extractor chosen. "
        "Shape=(nchan, npix, nsamples)."
    ))
    peakpos = Field(None, (
        "numpy array containing position of the peak as determined by the "
        "peak-finding algorithm for each pixel and channel"
    ))
    cleaned = Field(
        None, "numpy array containing the waveform after cleaning"
    )


class CameraCalibrationContainer(Container):
    """
    Storage of externally calculated calibration parameters (not per-event)
    """
    dc_to_pe = Field(None, "DC/PE calibration arrays from MC file")
    pedestal = Field(None, "pedestal calibration arrays from MC file")


class DL1Container(Container):
    """ DL1 Calibrated Camera Images and associated data"""
    tel = Field(Map(DL1CameraContainer), "map of tel_id to DL1CameraContainer")


class R0CameraContainer(Container):
    """
    Storage of raw data from a single telescope
    """
    adc_sums = Field(None, (
        "numpy array containing integrated ADC data "
        "(n_channels x n_pixels)"
    ))
    adc_samples = Field(None, (
        "numpy array containing ADC samples"
        "(n_channels x n_pixels, n_samples)"
    ))
    num_samples = Field(None, "number of time samples for telescope")



class R0Container(Container):
    """
    Storage of a Merged Raw Data Event
    """

    run_id = Field(-1, "run id number")
    event_id = Field(-1, "event id number")
    tels_with_data = Field([], "list of telescopes with data")
    tel = Field(Map(R0CameraContainer), "map of tel_id to R0CameraContainer")


class R1CameraContainer(Container):
    """
    Storage of r1 calibrated data from a single telescope
    """
    pe_samples = Field(None, (
        "numpy array containing p.e. samples"
        "(n_channels x n_pixels, n_samples)"
    ))


class R1Container(Container):
    """
    Storage of a r1 calibrated Data Event
    """

    run_id = Field(-1, "run id number")
    event_id = Field(-1, "event id number")
    tels_with_data = Field([], "list of telescopes with data")
    tel = Field(Map(R1CameraContainer), "map of tel_id to R1CameraContainer")


class DL0CameraContainer(Container):
    """
    Storage of data volume reduced dl0 data from a single telescope
    """
    pe_samples = Field(None, (
        "numpy array containing data volume reduced "
        "p.e. samples"
        "(n_channels x n_pixels, n_samples)"
    ))


class DL0Container(Container):
    """
    Storage of a data volume reduced Event
    """

    run_id = Field(-1, "run id number")
    event_id = Field(-1, "event id number")
    tels_with_data = Field([], "list of telescopes with data")
    tel = Field(Map(DL0CameraContainer), "map of tel_id to DL0CameraContainer")


class MCCameraEventContainer(Container):
    """
    Storage of mc data for a single telescope that change per event
    """
    photo_electron_image = Field(
        Map(), "reference image in pure photoelectrons, with no noise"
    )
    # todo: move to instrument (doesn't change per event)
    reference_pulse_shape = Field(
        None, "reference pulse shape for each channel"
    )
    # todo: move to instrument or a static MC container (don't change per
    # event)
    time_slice = Field(0, "width of time slice", unit=u.ns)
    dc_to_pe = Field(None, "DC/PE calibration arrays from MC file")
    pedestal = Field(None, "pedestal calibration arrays from MC file")
    azimuth_raw = Field(
        0, "Raw azimuth angle [radians from N->E] for the telescope"
    )
    altitude_raw = Field(0, "Raw altitude angle [radians] for the telescope")
    azimuth_cor = Field(
        0, "the tracking Azimuth corrected for pointing errors for the telescope"
    )
    altitude_cor = Field(
        0, "the tracking Altitude corrected for pointing errors for the telescope"
    )


class MCEventContainer(Container):
    """
    Monte-Carlo
    """
    energy = Field(0.0, "Monte-Carlo Energy", unit=u.TeV)
    alt = Field(0.0, "Monte-carlo altitude", unit=u.deg)
    az = Field(0.0, "Monte-Carlo azimuth", unit=u.deg)
    core_x = Field(0.0, "MC core position", unit=u.m)
    core_y = Field(0.0, "MC core position", unit=u.m)
    h_first_int = Field(0.0, "Height of first interaction")
    tel = Field(
        Map(MCCameraEventContainer), "map of tel_id to MCCameraEventContainer"
    )


class MCHeaderContainer(Container):
    """
    Monte-Carlo information that doesn't change per event
    """
    run_array_direction = Field([], (
        "the tracking/pointing direction in "
        "[radians]. Depending on 'tracking_mode' "
        "this either contains: "
        "[0]=Azimuth, [1]=Altitude in mode 0, "
        "OR "
        "[0]=R.A., [1]=Declination in mode 1."
    ))


class CentralTriggerContainer(Container):

    gps_time = Field(Time, "central average time stamp")
    tels_with_trigger = Field([], "list of telescopes with data")


class ReconstructedShowerContainer(Container):
    """
    Standard output of algorithms reconstructing shower geometry
    """

    alt = Field(0.0, "reconstructed altitude", unit=u.deg)
    alt_uncert = Field(0.0, "reconstructed altitude uncertainty", unit=u.deg)
    az = Field(0.0, "reconstructed azimuth", unit=u.deg)
    az_uncert = Field(0.0, 'reconstructed azimuth uncertainty', unit=u.deg)
    core_x = Field(
        0.0, 'reconstructed x coordinate of the core position', unit=u.m
    )
    core_y = Field(
        0.0, 'reconstructed y coordinate of the core position', unit=u.m
    )
    core_uncert = Field(
        0.0, 'uncertainty of the reconstructed core position', unit=u.m
    )
    h_max = Field(0.0, 'reconstructed height of the shower maximum')
    h_max_uncert = Field(0.0, 'uncertainty of h_max')
    is_valid = Field(False, (
        'direction validity flag. True if the shower direction'
        'was properly reconstructed by the algorithm'
    ))
    tel_ids = Field([], (
        'list of the telescope ids used in the'
        ' reconstruction of the shower'
    ))
    average_size = Field(0.0, 'average size of used')
    goodness_of_fit = Field(0.0, 'measure of algorithm success (if fit)')


class ReconstructedEnergyContainer(Container):
    """
    Standard output of algorithms estimating energy
    """
    energy = Field(-1.0, 'reconstructed energy', unit=u.TeV)
    energy_uncert = Field(-1.0, 'reconstructed energy uncertainty', unit=u.TeV)
    is_valid = Field(False, (
        'energy reconstruction validity flag. True if '
        'the energy was properly reconstructed by the '
        'algorithm'
    ))
    tel_ids = Field([], (
        'array containing the telescope ids used in the'
        ' reconstruction of the shower'
    ))
    goodness_of_fit = Field(0.0, 'goodness of the algorithm fit')


class ParticleClassificationContainer(Container):
    """
    Standard output of gamma/hadron classification algorithms
    """
    # TODO: Do people agree on this? This is very MAGIC-like.
    # TODO: Perhaps an integer classification to support different classes?
    # TODO: include an error on the prediction?
    prediction = Field(0.0, (
        'prediction of the classifier, defined between '
        '[0,1], where values close to 0 are more '
        'gamma-like, and values close to 1 more '
        'hadron-like'
    ))
    is_valid = Field(False, (
        'classificator validity flag. True if the '
        'predition was successful within the algorithm '
        'validity range')
    )

    # TODO: KPK: is this different than the list in the reco
    # container? Why repeat?
    tel_ids = Field([], (
        'array containing the telescope ids used '
        'in the reconstruction of the shower'
    ))
    goodness_of_fit = Field(0.0, 'goodness of the algorithm fit')


class ReconstructedContainer(Container):
    """ collect reconstructed shower info from multiple algorithms """

    shower = Field(
        Map(ReconstructedShowerContainer),
        "Map of algorithm name to shower info"
    )
    energy = Field(
        Map(ReconstructedEnergyContainer),
        "Map of algorithm name to energy info"
    )
    classification = Field(
        Map(ParticleClassificationContainer),
        "Map of algorithm name to classification info"
    )


class TelescopePointingContainer(Container):
    '''
    Container holding pointing information for a single telescope
    after all necessary correction and calibration steps.
    These values should be used in the reconstruction to transform
    between camera and sky coordinates.
    '''
    azimuth = Field(nan * u.rad, 'Azimuth, measured N->E', unit=u.rad)
    altitude = Field(nan * u.rad, 'Altitude', unit=u.rad)


class DataContainer(Container):
    """ Top-level container for all event information """

    r0 = Field(R0Container(), "Raw Data")
    r1 = Field(R1Container(), "R1 Calibrated Data")
    dl0 = Field(DL0Container(), "DL0 Data Volume Reduced Data")
    dl1 = Field(DL1Container(), "DL1 Calibrated image")
    dl2 = Field(ReconstructedContainer(), "Reconstructed Shower Information")
    mc = Field(MCEventContainer(), "Monte-Carlo data")
    mcheader = Field(MCHeaderContainer(), "Monte-Carlo run header data")
    trig = Field(CentralTriggerContainer(), "central trigger information")
    count = Field(0, "number of events processed")
    inst = Field(InstrumentContainer(), "instrumental information (deprecated")
    pointing = Field(Map(TelescopePointingContainer), 'Telescope pointing positions')


class MuonRingParameter(Container):
    """
    Storage of muon ring fit output

    Parameters
    ----------

    run_id : int
        run number
    event_id : int
        event number
    tel_id : int
        telescope ID
    ring_center_x, ring_center_y, ring_radius:
        center position and radius of the fitted ring
    ring_chi2_fit:
        chi squared of the ring fit
    ring_cov_matrix:
        covariance matrix of ring parameters
    """

    run_id = Field(0, "run identification number")
    event_id = Field(0, "event identification number")
    tel_id = Field(0, 'telescope identification number')
    ring_center_x = Field(0.0, 'centre (x) of the fitted muon ring')
    ring_center_y = Field(0.0, 'centre (y) of the fitted muon ring')
    ring_radius = Field(0.0, 'radius of the fitted muon ring')
    ring_chi2_fit = Field(0.0, 'chisquare of the muon ring fit')
    ring_cov_matrix = Field(0.0, 'covariance matrix of the muon ring fit')
    ring_fit_method = Field("", 'fitting method used for the muon ring')
    inputfile = Field("", 'input file')


class MuonIntensityParameter(Container):
    """
    Storage of muon intensity fit output

    Parameters
    ----------

    run_id : int
        run number
    event_id : int
        event number
    tel_id : int
        telescope ID
    impact_parameter: float
        reconstructed impact parameter
    impact_parameter_chi2:
        chi squared impact parameter
    intensity_cov_matrix:
        Covariance matrix of impact parameters or alternatively:
        full 5x5 covariance matrix for the complete fit (ring + impact)
    impact_parameter_pos_x, impact_parameter_pos_y:
        position on the mirror of the muon impact
    COG_x, COG_y:
        center of gravity
    optical_efficiency_muon:
        optical muon efficiency from intensity fit
    ring_completeness:
        completeness of the ring
    ring_num_pixel: int
        Number of pixels composing the ring
    ring_size:
        ring size
    off_ring_size:
        size outside of the ring
    ring_width:
        ring width
    ring_time_width:
        standard deviation of the photons time arrival

    prediction: dict
        ndarray of the predicted charge in all pixels
    mask:
        ndarray of the mask used on the image for fitting

    """
    run_id = Field(0, 'run identification number')
    event_id = Field(0, 'event identification number')
    tel_id = Field(0, 'telescope identification number')
    ring_completeness = Field(0., 'fraction of ring present')
    ring_num_pixel = Field(0, 'number of pixels in the ring image')
    ring_size = Field(0., 'size of the ring in pe')
    off_ring_size = Field(0., 'image size outside of ring in pe')
    ring_width = Field(0., 'width of the muon ring in degrees')
    ring_time_width = Field(0., 'duration of the ring image sequence')
    impact_parameter = Field(0., 'distance of muon impact position from centre of mirror')
    impact_parameter_chi2 = Field(0., 'impact parameter chi squared')
    intensity_cov_matrix = Field(0., 'covariance matrix of intensity')
    impact_parameter_pos_x = Field(0., 'impact parameter x position')
    impact_parameter_pos_y = Field(0., 'impact parameter y position')
    COG_x = Field(0.0, 'Centre of Gravity x')
    COG_y = Field(0.0, 'Centre of Gravity y')
    prediction = Field([], 'image prediction')
    mask = Field([], 'image pixel mask')
    optical_efficiency_muon = Field(0., 'optical efficiency muon')
    intensity_fit_method = Field("", 'intensity fit method')
    inputfile = Field("", 'input file')


class HillasParametersContainer(Container):

    intensity = Field(0.0, 'total intensity (size)')

    x = Field(0.0, 'centroid x coordinate')
    y = Field(0.0, 'centroid x coordinate')
    r = Field(0.0, 'radial coordinate of centroid')
    phi = Field(0.0, 'polar coordinate of centroid', unit=u.deg)

    length = Field(0.0, 'RMS spread along the major-axis')
    width = Field(0.0, 'RMS spread along the minor-axis')
    psi = Field(0.0, 'rotation angle of ellipse', unit=u.deg)

    skewness = Field(0.0, 'measure of the asymmetry')
    kurtosis = Field(0.0, 'measure of the tailedness')
