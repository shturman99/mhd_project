import matplotlib.pyplot as plt
import numpy as np

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

# Example usage:
# labels = ['no_source', 'ramp_decay', 'step_decay', 'step_no_decay']
# fig, axes = plot_simulation_parameters(tsall, labels=labels, max_rows=5)  # Only show first 5 parameters
# plt.show()