"""
Plot density map for the spectra in a particular fits file.

author: R. Garcia-Dias rafaelagd@gmail.com
date: Aug. 17, 2017
"""
from numpy import squeeze, ones, where
from astropy.io import fits
from matplotlib.pyplot import hist2d, figure, ylabel, tight_layout, colorbar, show, xlabel, cm

# getting the data
filename_field = 'https://dr14.sdss.org/sas/dr14/apogee/spectro/redux/r8/stars/l31c/l31c.2/2001/aspcapField-2001.fits'
fits_spectra = fits.open(filename_field)
spectra = fits_spectra[2].data['SPEC']
wavelength = squeeze(10 ** fits_spectra[3].data['WAVE'])

# define wavelenght coverage
MIN_WAVE, MAX_WAVE = 16178, 16222
wave_filter = where((wavelength >= MIN_WAVE) & (wavelength <= MAX_WAVE))[0]

# replicate the wavelength
wave_arr = ones((spectra.shape[0], len(wave_filter))) * wavelength[wave_filter]

# reshape arrays to a single line
wave_arr = wave_arr.flatten()
spectra = spectra[:, wave_filter].flatten()

# define plot limits
MIN_FLUX, MAX_FLUX = 0.65, 1.05
lim_plot = [(MIN_WAVE, MAX_WAVE), (MIN_FLUX, MAX_FLUX)]

# plot
fig = figure(figsize=(16, 4.5))
ax = fig.add_subplot(111)
ax.tick_params(labelsize=18, axis='both')
hist2d(wave_arr, spectra,
       bins=[len(wave_filter), 80],  # number of bins
           range=lim_plot,  # limits where the density map is defined
           cmap=cm.gnuplot2_r,  # color map
           vmin=1)  # saturation to the lighter color in the cmap
cbar = colorbar()
xlabel('wavelength ($\AA$)', fontsize=18)
ylabel('Norm. Flux', fontsize=18)
tight_layout()
show()
