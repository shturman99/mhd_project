import matplotlib.pyplot as plt
from scipy import constants
from scipy.special import zeta
import numpy as np
import math

def plot_simulation(tsall, labels=None, figsize=(30, 160), exclude_params=['t', 'keys'], max_rows=None):
    """
    Plot all parameters from a list of time series objects.
    
    Parameters:
    -----------
    tsall : list
        List of time series objects with attributes to plot
    labels : list, optional
        Names for each time series in tsall. If None, indices will be used
    figsize : tuple, optional
        Size of the figure (width, height)
    exclude_params : list, optional
        Parameters to exclude from plotting
    max_rows : int, optional
        Maximum number of parameter rows to display. If None, display all parameters.
        
    Returns:
    --------
    fig, axes : matplotlib figure and axes objects
    """
    
    # Set default labels if none provided
    if labels is None:
        labels = [f'Series {i}' for i in range(len(tsall))]
    
    # Verify labels match the number of time series
    if len(labels) != len(tsall):
        raise ValueError(f"Number of labels ({len(labels)}) doesn't match number of time series ({len(tsall)})")
    
    # Get valid parameters (excluding specified ones)
    valid_params = [param for param in tsall[0].__dict__.keys() if param not in exclude_params]
    
    # Apply row limit if specified
    if max_rows is not None and max_rows > 0:
        valid_params = valid_params[:max_rows]
    
    num_params = len(valid_params)
    
    # Create the figure with proper dimensions
    fig, axes = plt.subplots(nrows=num_params, ncols=len(tsall), figsize=figsize)
    
    # Handle the case of a single row or column subplot
    if num_params == 1 and len(tsall) == 1:
        axes = np.array([[axes]])
    elif num_params == 1:
        axes = axes.reshape(1, -1)
    elif len(tsall) == 1:
        axes = axes.reshape(-1, 1)
    
    # Loop through all time series
    for ts_id, ts in enumerate(tsall):
        # Loop through each valid parameter
        for plot_row, param in enumerate(valid_params):
            # Select the correct axis
            ax = axes[plot_row, ts_id]
            
            # Plot the parameter data
            # Assuming ts.t exists and starts from 1, adjust as needed
            ax.plot(ts.t-1, getattr(ts, param), "o", linewidth=2)
            
            # Set labels and title
            ax.set_title(f'{labels[ts_id]}: {param}', fontsize=16)
            ax.set_xlabel(r'$t$', fontsize=14)
            ax.set_ylabel(param, fontsize=14)
            ax.tick_params(axis='both', which='major', labelsize=12)
    
    # Adjust layout
    plt.tight_layout()
    plt.subplots_adjust(hspace=0.4, wspace=0.4)  # Add more space between subplots
    
    return fig, axes


# =========================== 
# === PHYSICAL CONSTANTS ===
# ===========================

# Create a dictionary to store all constants and conversions
convert = {}

# Exact physical constants
convert['c'] = 299792458  # m/s (exact)
convert['h'] = 6.62607015e-34  # J/Hz (exact)
convert['hbar'] = convert['h']/(2 * math.pi)  # exact
convert['hbar_c'] = convert['hbar'] * convert['c']  # exact

# Empirical masses
convert['me'] = 0.51099895000  # MeV/c^2
convert['mp'] = 938.27208816  # MeV/c^2
convert['mn'] = 939.56542052  # MeV/c^2
convert['md'] = 1875.61294257  # MeV/c^2
convert['u'] = 931.49410242  # MeV/c^2

# Electromagnetic constants
convert['mu0'] = 4 * math.pi * 1.00000000055e-7  # N/A^2
convert['epsilon0'] = 1/(convert['mu0'] * convert['c']**2)  # empirical

# Fine structure constant (approximately 1/137)
convert['alpha'] = 1/137.0

# Classical electron radius
convert['re'] = convert['hbar_c'] * convert['alpha'] / (convert['me'] * convert['c']**2)

# Compton wavelength
convert['lambda_e'] = convert['hbar'] / (convert['me'] * convert['c'])

# Bohr radius
convert['a_infinity'] = convert['re'] / convert['alpha']**2

# Rydberg constant
convert['R_infinity'] = convert['me'] * convert['c']**2 * convert['alpha']**2 / (2 * convert['h'] * convert['c'])

# Thomson cross section
convert['sigma_T'] = 8 * math.pi * convert['re']**2 / 3

# Gravitational constants
convert['GN'] = 6.67430e-11  # m^3 kg^-1 s^-2
convert['gN'] = 9.80665  # m/s^2 (exact)

# Thermodynamic constants
convert['kB'] = 1.380649e-23  # J/K (exact)
convert['b'] = 2.897771955e-3  # m·K (Wien's displacement constant)
convert['sigma_SB'] = (math.pi**2 * convert['kB']**4) / (60 * convert['hbar']**3 * convert['c']**2)  # Stefan-Boltzmann constant

# Electroweak and strong interaction
convert['GF'] = 1.1663787e-5  # GeV^-2 ħc^3
convert['sin_sq_theta'] = 0.23122  # Weak mixing angle
convert['mW'] = 80.379  # W boson mass in GeV/c^2
convert['mZ'] = 91.1876  # Z boson mass in GeV/c^2
convert['alpha_s'] = 0.1179  # Strong coupling constant

# Unit conversions
convert['inch'] = 0.0254  # m
convert['Angstrom'] = 0.1e-9  # m
convert['barn'] = 1e-28  # m^2
convert['dyne'] = 1e-5  # N
convert['erg'] = 1e-7  # J
convert['kg'] = 5.609588603e35  # eV/c^2
convert['Coulomb'] = 2.99792458e9  # esu

# Mass units
convert['gram'] = 1e-3  # kg
convert['MP'] = np.sqrt(convert['hbar_c']/convert['GN'])  # Planck mass
convert['Mpl'] = convert['MP']/np.sqrt(8 * math.pi)  # reduced Planck mass

# Energy units
convert['PeV'] = 1e15  # eV
convert['TeV'] = 1e12  # eV
convert['GeV'] = 1e9  # eV
convert['MeV'] = 1e6  # eV
convert['keV'] = 1e3  # eV
convert['meV'] = 1e-3  # eV
convert['ueV'] = 1e-6  # eV
convert['Joule'] = convert['kg'] * convert['c']**2  # J

# Chemistry
convert['N0'] = 6.02214076e23  # Avogadro's constant (exact)
convert['NA'] = convert['N0']  # Avogadro's number

# Force
convert['Newton'] = convert['kg'] * convert['c'] * convert['c'] / convert['c']  # N

# Power
convert['Watt'] = convert['Joule'] / 1  # W

# Length units
convert['km'] = 1e3  # m
convert['cm'] = 1e-2  # m
convert['nm'] = 1e-9  # m
convert['fm'] = 1e-15  # m
convert['ly'] = convert['c'] * 365.25 * 24 * 3600  # light-year in m
convert['Gly'] = 1e9 * convert['ly']  # giga light-year
convert['AU'] = 149597870700  # m
convert['pc'] = (648000/math.pi) * convert['AU']  # parsec
convert['kpc'] = 1e3 * convert['pc']  # kiloparsec
convert['Mpc'] = 1e6 * convert['pc']  # megaparsec
convert['Gpc'] = 1e9 * convert['pc']  # gigaparsec
convert['mbarn'] = 1e-3 * convert['barn']  # millibarn
convert['lP'] = 1/(convert['MP'] * convert['c']**2 / convert['hbar_c'])  # Planck length

# Time units
convert['sec'] = 1  # s
convert['hr'] = 3600 * convert['sec']  # hour
convert['day'] = 24 * convert['hr']  # day
convert['yr'] = 365.25 * convert['day']  # Julian year
convert['yrGreg'] = 365.2425 * convert['day']  # Gregorian year
convert['tU'] = 13.7e9 * convert['yr']  # age of the universe
convert['tP'] = 1/(convert['MP'] * convert['c']**2 / convert['hbar'])  # Planck time

# Frequency units
convert['mHz'] = 1e-3  # Hz
convert['Hz'] = 1  # Hz
convert['kHz'] = 1e3  # Hz
convert['MHz'] = 1e6  # Hz
convert['GHz'] = 1e9  # Hz

# Angle units
convert['rad'] = 1  # radian
convert['deg'] = math.pi/180 * convert['rad']  # degree
convert['arcmin'] = convert['deg']/60  # arcminute
convert['arcsec'] = convert['deg']/3600  # arcsecond
convert['sr'] = 1  # steradian
convert['sqdeg'] = math.pi**2/180**2 * convert['sr']  # square degree

# Electromagnetic units in SI
convert['Volt'] = convert['Joule'] / convert['Coulomb']  # V
convert['Henry'] = convert['Joule'] / convert['Coulomb']**2  # H
convert['Tesla'] = convert['Joule'] / (convert['Coulomb'] * convert['c'] * convert['c'])  # T
convert['Ampere'] = convert['Coulomb'] / convert['sec']  # A
convert['Farad'] = convert['Coulomb'] / convert['Volt']  # F
convert['eSI'] = 1.602176634e-19  # C (exact)
convert['alpha_SI'] = convert['eSI']**2 / (4 * math.pi * convert['epsilon0'] * convert['hbar_c'])
convert['Gauss_SI'] = 1e-4 * convert['Tesla']  # G
convert['mu_B_SI'] = convert['eSI'] * convert['hbar'] / (2 * convert['me'])  # Bohr magneton
convert['mu_N_SI'] = convert['eSI'] * convert['hbar'] / (2 * convert['mp'])  # Nuclear magneton

# Electromagnetism in HL units
convert['eHL'] = np.sqrt(4 * math.pi * convert['hbar_c'] * 0.00729735256931876)
convert['alpha_HL'] = convert['eHL']**2 / (4 * math.pi * convert['hbar_c'])
convert['Gauss_HL'] = (4 * math.pi)**(-1/2) * convert['gram']**(1/2) * convert['cm']**(-1/2) / convert['sec']
convert['mu_B_HL'] = convert['eHL'] * convert['hbar'] / (2 * convert['me'])
convert['mu_N_HL'] = convert['eHL'] * convert['hbar'] / (2 * convert['mp'])

# Electromagnetism in CGS units
convert['eCGS'] = np.sqrt(convert['hbar_c'] * 0.00729735256931876)
convert['alpha_CGS'] = convert['eCGS']**2 / convert['hbar_c']
convert['Gauss_CGS'] = convert['gram']**(1/2) * convert['cm']**(-1/2) / convert['sec']
convert['mu_B_CGS'] = convert['eCGS'] * convert['hbar'] / (2 * convert['me'] * convert['c'])
convert['mu_N_CGS'] = convert['eCGS'] * convert['hbar'] / (2 * convert['mp'] * convert['c'])

# Astrophysics
convert['Jy'] = 1e-26 * convert['Watt'] / (convert['c']**2)  # Jansky
convert['Msun'] = 1.989e30 * convert['kg']  # Solar mass
convert['Rsun'] = 6.957e5 * convert['km']  # Solar radius
convert['Lsun'] = 3.828e26 * convert['Joule'] / convert['sec']  # Solar luminosity
convert['Mearth'] = 5.972e24 * convert['kg']  # Earth mass
convert['Rearth'] = 6.371e3 * convert['km']  # Earth radius
convert['Mmoon'] = 7.348e22 * convert['kg']  # Moon mass

# Cosmology
convert['gast0'] = 3.36  # Relativistic degrees of freedom (energy density)
convert['gastE0'] = convert['gast0']  # Relativistic degrees of freedom (energy density)
convert['gastS0'] = 3.91  # Relativistic degrees of freedom (entropy density)
convert['H100'] = 100 * convert['km'] / convert['sec'] / convert['Mpc']  # Hubble parameter
convert['h100'] = 0.7  # Hubble constant in units of H100
convert['H0'] = convert['h100'] * convert['H100']  # Hubble constant
convert['T0'] = 0.234 * convert['meV'] / convert['kB']  # CMB temperature

# =========================== 
# === CODE UNITS CALCULATION ===
# ===========================

def calculate_code_units(T100=1.0, g30=1.0, alpha=1/137.0):
    """
    Calculate code units based on temperature and other parameters
    
    Parameters:
    -----------
    T100 : float
        Temperature in units of 100 GeV
    g30 : float
        Relativistic degrees of freedom divided by 30
    alpha : float
        Fine structure constant
        
    Returns:
    --------
    Dictionary with calculated values
    """
    # Additional constants needed for calculations
    me = 511e-6  # electron mass in GeV/c^2
    v = 246  # Higgs vev in GeV
    gP = 0.35  # some coupling constant
    ye = np.sqrt(2) * me / v  # Yukawa coupling
    kB = convert['kB']
    hbar = convert['hbar']
    c = convert['c']
    T = T100 * 100 * convert['GeV'] / kB  # Temperature
    Mpl = convert['Mpl']  # reduced Planck mass
    
    # Calculate radiation energy density
    gE = g30 * 30  # Relativistic degrees of freedom
    Erad = (math.pi**2 / 30) * gE * (kB**4 * T**4) / (hbar**3 * c**3)
    
    # Solve for Hubble parameter
    H = np.sqrt(Erad * hbar / (3 * c * Mpl**2))
    
    # Calculate other quantities
    t = 1 / H  # time
    l = c * t  # length
    EE = Erad * l**3  # energy
    
    # Print the results in the same format as the Mathematica code
    t_star = (8.83758e-11 / (np.sqrt(g30) * T100**2))
    l_star = (2.64944 / (np.sqrt(g30) * T100**2))
    E_star = (2.38892e60 / (np.sqrt(g30) * T100**2))
    
    print(f"t_* = {t_star} sec")
    print(f"l_* = {l_star} cm")
    print(f"E_* = {E_star} eV")
    
    return {'t': t, 'l': l, 'EE': EE, 'H': H, 'Erad': Erad, 
            't_star': t_star, 'l_star': l_star, 'E_star': E_star}

# =========================== 
# === MHD PARAMETERS ===
# ===========================

def calculate_mhd_parameters(code_units, T100=1.0, g30=1.0, alpha=1/137.0):
    """
    Calculate MHD parameters
    
    Parameters:
    -----------
    code_units : dict
        Dictionary with code units from calculate_code_units
    T100 : float
        Temperature in units of 100 GeV
    g30 : float
        Relativistic degrees of freedom divided by 30
    alpha : float
        Fine structure constant
        
    Returns:
    --------
    Dictionary with calculated MHD parameters
    """
    # Additional constants needed for calculations
    me = 511e-6  # electron mass in GeV/c^2
    v = 246  # Higgs vev in GeV
    gP = 0.35  # some coupling constant
    ye = np.sqrt(2) * me / v  # Yukawa coupling
    kB = convert['kB']
    hbar = convert['hbar']
    c = convert['c']
    T = T100 * 100 * convert['GeV'] / kB  # Temperature
    gE = g30 * 30  # Relativistic degrees of freedom
    
    # Get code units
    t = code_units['t']
    l = code_units['l']
    EE = code_units['EE']
    
    # Calculate MHD parameters
    sigma = (6**4 * zeta(3)**2) / math.pi**3 * (math.pi**2/8 + 22/3)**(-1) * \
            1 / (gP**2 * np.log(1/gP)) * (kB * T) / hbar
    
    eta = c**2 / sigma
    nu = 1e-2 * (hbar * c**2) / (kB * T)
    lambda_param = (12 * alpha**2) / math.pi**2 * (hbar * c) / (kB**2 * T**2)
    D5 = 1e-2 * (hbar * c**2) / (kB * T)
    Gamma_f = (1.3e-2) * ye**2 * (kB * T) / hbar
    S5 = 1e-10 * math.pi**2 / 30 * gE * (kB**4 * T**4) / (hbar**4 * c**3)
    scaled_S5 = (hbar**2 * c**2) / kB**2 * alpha / (3 * math.pi * T**2) * S5
    
    # Calculate scaled parameters and print
    sigma_scaled = 7.36022e17 / (np.sqrt(g30) * T100)
    eta_scaled = 1.35866e-18 * np.sqrt(g30) * T100
    nu_scaled = 7.44788e-19 * np.sqrt(g30) * T100
    lambda_scaled = 1.15259e29 / T100**2
    D5_scaled = 7.44788e-19 * np.sqrt(g30) * T100
    Gamma_f_scaled = 1506.3 / (np.sqrt(g30) * T100)
    S5_scaled = 3.20752e55 / (g30 * T100**4)
    scaled_S5_scaled = 1.37798e20 / T100**2
    
    print(f"σ = {sigma_scaled} t_*^(-1)")
    print(f"η = {eta_scaled} l_*^2 t_*^(-1)")
    print(f"ν = {nu_scaled} l_*^2 t_*^(-1)")
    print(f"λ = {lambda_scaled} l_* E_*^(-1)")
    print(f"D_5 = {D5_scaled} l_*^2 t_*^(-1)")
    print(f"Γ_flip = {Gamma_f_scaled} t_*^(-1)")
    print(f"S_5 = {S5_scaled} l_*^(-3) t_*^(-1)")
    print(f"(ħ^2 c^2)/(k_B^2) α/(3π T^2) S_5 = {scaled_S5_scaled} l_*^(-1) t_*^(-1)")
    
    return {
        'sigma': sigma, 'eta': eta, 'nu': nu, 'lambda': lambda_param,
        'D5': D5, 'Gamma_f': Gamma_f, 'S5': S5, 'scaled_S5': scaled_S5,
        'sigma_scaled': sigma_scaled, 'eta_scaled': eta_scaled,
        'nu_scaled': nu_scaled, 'lambda_scaled': lambda_scaled,
        'D5_scaled': D5_scaled, 'Gamma_f_scaled': Gamma_f_scaled,
        'S5_scaled': S5_scaled, 'scaled_S5_scaled': scaled_S5_scaled
    }

# Calculate equilibrium μ5
def calculate_equilibrium_mu5(code_units, mhd_params, T100=1.0, g30=1.0, alpha=1/137.0):
    """Calculate equilibrium μ5"""
    kB = convert['kB']
    hbar = convert['hbar']
    c = convert['c']
    T = T100 * 100 * convert['GeV'] / kB  # Temperature
    
    result = hbar * c / (kB * T) * (hbar**2 * c**2) / kB**2 * \
             alpha / (3 * math.pi * T**2) * mhd_params['S5'] / mhd_params['Gamma_f']
    
    equilibrium_mu5 = 6.81342 * g30
    print(f"Equilibrium μ5 = {equilibrium_mu5}")
    return equilibrium_mu5

# Main execution
if __name__ == "__main__":
    # Default parameters
    T100 = 1.0  # Temperature in units of 100 GeV
    g30 = 1.0   # Relativistic degrees of freedom / 30
    alpha = 1/137.0  # Fine structure constant
    
    # Run calculations
    print("\n=== Code Units ===")
    code_units = calculate_code_units(T100, g30, alpha)
    
    print("\n=== MHD Parameters ===")
    mhd_params = calculate_mhd_parameters(code_units, T100, g30, alpha)
    
    print("\n=== Equilibrium μ5 ===")
    equilibrium_mu5 = calculate_equilibrium_mu5(code_units, mhd_params, T100, g30, alpha)