# -*- coding: utf-8 -*-
"""
Created on 31/08/2023

@authors: 
    Lukas B. Nordentoft, lbn@mpe.au.dk
    Anders L. Andreasen, ala@mpe.au.dk
"""

def set_options():
    '''
    Configures and sets custom plotting options using Matplotlib.
    
    This function adjusts various Matplotlib settings such as background color,
    grid color, style, resolution, font size, and font family for improved visualizations.
    '''
    import matplotlib.pyplot as plt
    import matplotlib
    color_bg      = "0.99"          #Choose background color
    color_gridaxe = "0.85"          #Choose grid and spine color
    rc = {"axes.edgecolor":color_gridaxe} 
    plt.style.use(('ggplot', rc))           #Set style with extra spines
    plt.rcParams['figure.dpi'] = 300        #Set resolution
    plt.rcParams['figure.figsize'] = [10, 5]
    matplotlib.rc('font', size=15)
    matplotlib.rc('axes', titlesize=20)
    matplotlib.rcParams['font.family'] = ['DejaVu Sans']     #Change font to Computer Modern Sans Serif
    plt.rcParams['axes.unicode_minus'] = False          #Re-enable minus signs on axes))
    plt.rcParams['axes.facecolor']= color_bg             #Set plot background color
    plt.rcParams.update({"axes.grid" : True, "grid.color": color_gridaxe}) #Set grid color
    plt.rcParams['axes.grid'] = True
    # plt.fontname = "Computer Modern Serif"
    
def cmap_alpha(cmap_name):
    '''
    Takes a matplotlib colormap and makes lower values increasingly transparent
    until fully transparent.

    Parameters:
    - cmap_name (string): The name of the base colormap

    Returns:
    - cmap_alpha (colormap): Matplotlib colormap object with transparency
    '''
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap

    cmap_alpha = plt.get_cmap(cmap_name)(range(256))
    cmap_alpha[:,-1] = np.linspace(0.0, 1.0,256)
    cmap_alpha = LinearSegmentedColormap.from_list(name = cmap_name + '_alpha',
                                                   colors = cmap_alpha)
    
    return cmap_alpha

def near_optimal_space_matrix(vertices, 
                              samples = None,
                              bins = 50, 
                              title = 'Near-optimal space matrix', 
                              cmap = 'Blues',
                              xlim = [None, None], ylim = [None, None],
                              xlabel = None, ylabel = None,
                              opt_solution = None, cheb_center = None,
                              plot_vertices = False, plot_boundary = True,
                              filename = None, 
                              ):
    '''
    Creates a matrix plot of 2D projections of polytope vertices. If samples 
    are provided, plots the sample distributions within each projection.

    Parameters:
    - vertices (pd.DataFrame): DataFrame containing vertices of the space.
    - samples (pd.DataFrame, optional): DataFrame containing samples from the 
            space. If provided, plot distribution on each projection.
    - bins (int, optional): Number of bins for 2D histograms. Default is 50.
    - title (str, optional): Title of the plot.
    - cmap (str, optional): Colormap for correlations. Default is 'Blues'.
    - xlim (list, optional): Optional limits for x-axis. 
    - ylim (list, optional): Optional limits for y-axis.
    - xlabel (str, optional): Label for x-axis. 
    - ylabel (str, optional): Label for y-axis. 
    - opt_solution (pd.DataFrame, optional): DataFrame containing optimal solution.
    - cheb_center (pd.DataFrame, optional): DataFrame containing Chebyshev center. 
    - plot_vertices (bool, optional): Whether to plot vertices. 
    - plot_boundary (bool, optional): Whether to plot the convex hull boundary.
    - filename (str, optional): If provided, saves the plot to a PDF file. 
    
    Returns:
    - axs (numpy.ndarray): Array of subplots.
    - fig (matplotlib.figure.Figure): The Figure object.
    
    '''
    
    import pandas as pd
    import matplotlib.pyplot as plt
    from scipy.spatial import ConvexHull
    import numpy as np
    import matplotlib.colors as mcolors
    import matplotlib.patches as mpatches
    from matplotlib.lines import Line2D
    import seaborn as sns
    
    variables = list(vertices.columns)
    var_titles = variables
    
    # -------- Set up plot ----------------------------------------
    set_options()
    
    # Initialize and adjust figure 
    fig, axs = plt.subplots(len(variables), len(variables), 
                            figsize=(20/3 * len(variables), 5 * len(variables)))
    
    fig.suptitle(title, fontsize = 28, y = 0.95)
    fig.subplots_adjust(wspace = 0.25, hspace = 0.35, top = 0.85)
    
    # Set top titles
    for ax, col in zip(axs[0], var_titles):
        ax.set_title(col + '\n')
    
    # Set side titles
    for ax, row in zip(axs[:,0], var_titles):
        ax.annotate(row, xy=(0, 0.5), xytext=(-ax.yaxis.labelpad - 5, 0),
                    xycoords = ax.yaxis.label, textcoords='offset points',
                    size = 24, ha = 'right', va = 'center', rotation = 90)

    
    # -------- Plotting -------------------------------
    
    # Upper triangle of subplots ----------------------------------------------
    for i in range(0, len(variables)):
        for j in range(0, i):
            
            # Get axis
            ax = axs[j][i]
            
            # Set ax options. Remove ticks and set title.
            ax.patch.set_facecolor('white')
            ax.set_xticks([])
            ax.set_yticks([])
            ax.text(0.5, 1.075, 'Correlation', ha='center', va='top',
                    transform=ax.transAxes, fontsize = 16, color = 'gray')
            
            # If samples are provided, calculate and plot correlations
            if samples is not None:
                
                # Create colormap for correlations
                red    = (1.0, 0.7, 0.6)  # light red
                yellow = (1.0, 1.0, 0.8)  # light yellow
                green  = (0.6, 1.0, 0.6)  # light green
                cmap = mcolors.LinearSegmentedColormap.from_list('my_colormap',
                                                                 [red, yellow, green])
                
                # Create dataframe from samples
                samples_df = pd.DataFrame(samples, columns = variables)
                
                # Calculate correlation and normalize
                samples_corr = samples_df.corr()
                
                # Calculate normalized correlation, used to color heatmap.
                samples_temp = samples_corr + abs(samples_corr.min().min())
                samples_norm = samples_temp / samples_temp.max().max()
                
                # Write correlation
                corr_text = str(round(samples_corr[variables[i]][variables[j]],2))
                ax.text(0.5, 0.5, corr_text, ha='center', va='center', fontsize=20)
                
                # Change bg color according to correlation
                ax.patch.set_facecolor(cmap(samples_norm[variables[i]][variables[j]]))
                
    
    # Diagonal plotting -------------------------------------------------------
    for j in range(0, len(variables)):

        ax = axs[j][j]
        
        # # Set ax options. Remove ticks and set title.
        ax.text(0.5, 1.075, 'Histogram', ha='center', va='top', 
                transform=ax.transAxes, fontsize = 16, color = 'gray')

        # Set x and y labels
        if not xlabel == None or ylabel == None:
            ax.set_xlabel(xlabel, color = 'gray', size = 16)
            ax.set_ylabel(ylabel, color = 'gray', size = 16)
        else:
            ax.set_ylabel('Proportion', color = 'gray', size = 16)
            ax.set_xlabel('Value', color = 'gray', size = 16)
        
        # If samples are provided, calculate and plot histogram
        if samples is not None:
            sns.histplot(samples_df[variables[j]].values,
                          bins = bins,
                          line_kws = {'linewidth':3},
                          element = 'bars',
                          stat = 'probability',
                          kde = True,
                          ax = ax, label = '_nolegend_',)
            
        # Show optimum if provided
        if opt_solution is not None:
            ax.axvline(x = opt_solution.iloc[0,j], color = 'gold', linestyle = '--',
                       linewidth = 4, gapcolor = 'darkorange',)
            
        # Show chebyshev center if provided
        if cheb_center is not None:
            ax.axvline(x = cheb_center.iloc[0,j], color = 'red', linestyle = '--',
                       linewidth = 2,)
    
    # lower traingle of subplots ----------------------------------------------
    for j in range(0, len(variables)):
        for i in range(0, j):
            
            ax = axs[j][i]
            
            if not xlabel == None or ylabel == None:
                ax.set_xlabel(xlabel, color = 'gray', size = 16)
                ax.set_ylabel(ylabel, color = 'gray', size = 16)
            else:
                ax.set_xlabel('Capacity [GW]', color = 'gray', size = 16)
                ax.set_ylabel('Capacity [GW]', color = 'gray', size = 16)
            
            ax.text(0.5, 1.075, 'Near-optimal space', ha='center', va='top',
                    transform=ax.transAxes, fontsize=16, color = 'gray')
            
            ax.grid('on')
            
            # -------- Create 2D histogram ------------------------------------
            
            if samples is not None:
                # Calculate 2D histogram data from samples for this dimension
                hist, xedges, yedges = np.histogram2d(samples.values[:,i],
                                                      samples.values[:,j],
                                                      bins = bins)
        
                # Create meshgrid and plot pcolormesh with 2D hist data
                X, Y = np.meshgrid(xedges, yedges)
                ax.pcolormesh(X, Y, hist.T, cmap = 'Blues', zorder = 0)
                
                # Create patch to serve as handle for legend
                hist_handle = mpatches.Patch(color = 'tab:blue')
            
            # -------- Plot hull ----------------------------------------------
            if plot_boundary:
                # Get 2D hull for dimension [i,j]
                hull = ConvexHull(vertices.values[:,[i,j]])
                
                # Plot simplexes (edges)
                for simplex in hull.simplices:
                    face_handle = ax.plot(vertices.values[simplex, i], 
                                          vertices.values[simplex, j],
                                           '-', color = 'silver', 
                                           label = 'faces', zorder = 0)
        
            # -------- Plot vertices ------------------------------------------
            if plot_vertices:
                # Vertices for this dimension
                x, y = vertices.values[:,i],   vertices.values[:,j]
                
                # Plot vertices
                vertices_handle, = ax.plot(x, y, 'o', label = "Near-optimal",
                                           color = 'lightcoral', zorder = 2)
                
            # --------- Plot optimal system -----------------------------------
            if opt_solution is not None:
                # Plot optimal solutions for this dimension
                ax.scatter(opt_solution.iloc[0,i], opt_solution.iloc[0,j],
                            marker = '*', s = 1000, zorder = 4,
                            linewidth = 2, alpha = 0.85,
                            facecolor = 'gold', edgecolor = 'darkorange',)
                
                opt_handle = Line2D([0], [0], marker = '*', color = 'gold',
                            markeredgecolor = 'darkorange', markeredgewidth = 2,
                            markersize = 25, label = 'Optimal Solutions',
                            linestyle = '',)
                
                opt_line_handle = Line2D([0], [0], linestyle = '--', color = 'gold',
                              gapcolor = 'darkorange', linewidth = 4,)
                
            # --------- Plot chebyshev center ---------------------------------
            if cheb_center is not None:
                cheb_handle, = ax.plot(cheb_center.iloc[0,i], cheb_center.iloc[0,j],
                              marker = 'o', linestyle = '',
                              ms = 15, zorder = 3, color = 'red',)
                
                cheb_line_handle = Line2D([0], [0], linestyle = '--', 
                                          color = 'red', linewidth = 2,)
                
            # --------- Set limits --------------------------------------------
            ax.set_xlim(xlim)
            ax.set_ylim(ylim)
            
    # Construct legend --------------------------------------------------------
    legend_handles, legend_labels = [], []
    
    if plot_boundary:
        legend_handles += [face_handle]
        legend_labels  += ['Polytope face']
    
    if samples is not None:
        legend_handles += [hist_handle]
        legend_labels  += ['Sample density']
    
    if opt_solution is not None:
        legend_handles += [opt_handle, opt_line_handle]
        legend_labels  += ['Optimal solution', 'Optimal line']
    
    if plot_vertices:
        legend_handles += [vertices_handle]
        legend_labels  += ['Vertices']
        
    if cheb_center is not None:
        legend_handles += [cheb_handle, cheb_line_handle]
        legend_labels  += ['Chebyshev center', 'Chebyshev line']
    
    # get central axis
    ax = axs[len(variables)-1,
             int(np.median(np.linspace(0, len(variables), len(variables)+1)))] # Get center axis
      
    # Place legend centrally below all plots
    ax.legend(legend_handles, legend_labels, 
              loc = 'center', ncol = 3,
              bbox_to_anchor=(0.5, -0.1*len(variables)), fancybox=False, shadow=False,)
    
    # Save to pdf if filename is given ----------------------------------------
    if not filename == None:
        fig.savefig(filename, format = 'pdf', bbox_inches='tight')
        
    plt.show()
        
    return axs, fig

def near_optimal_space_slice(chosen_variables,
                             vertices, samples,
                             hist_bins = 50, density_bins = 50,
                             title = 'Near-optimal space slice', cmap = 'Blues',
                             xlabel = None, ylabel = None,
                             opt_solution = None, cheb_center = None,
                             filename = None,
                             ):
    """
    Plots the 2D projection and histograms of two specific dimensions of a 
    n-dimensional polytope.

    Parameters:
    - chosen_variables (list): List of two variables to be plotted.
    - vertices (pd.DataFrame): DataFrame containing vertices of the space.
    - samples (pd.DataFrame): DataFrame containing samples from the space.
    - hist_bins (int, optional): Number of bins for histograms. Default is 50.
    - density_bins (int, optional): Number of bins for sample density. Default is 50.
    - title (str, optional): Title of the plot. 
    - cmap (str, optional): Colormap for sample density. Default is 'Blues'.
    - xlabel (str, optional): Optional label for x-axis. 
    - ylabel (str, optional): Optional label for y-axis. 
    - opt_solution (pd.DataFrame, optional): DataFrame containing optimal solutions. 
    - cheb_center (pd.DataFrame, optional): DataFrame containing Chebyshev center. 
    - filename (str, optional): If provided, saves the plot to a file. 

    Returns:
    - axs (numpy.ndarray): Array of subplots.
    """
    import pandas as pd
    import matplotlib.pyplot as plt
    from scipy.spatial import ConvexHull
    import numpy as np
    import matplotlib.patches as mpatches
    from matplotlib.lines import Line2D
    import seaborn as sns
    
    all_variables = list(samples.columns)
    
# - # -------- Set up plot ----------------------------------------
    set_options()
    plt.figure()
    fig, axs = plt.subplots(1, 2, figsize = (20,5),
                           gridspec_kw={'width_ratios': [1, 2]}, )
    fig.subplots_adjust(wspace = 0.2, hspace = 0.2)
    fig.suptitle(title, fontsize = 24, y = 1.05)
    
    axs[1].set_title('Histograms', color = 'gray')
    axs[1].set_xlabel('Variable value', color = 'gray')
    
    axs[0].set_title('Near-optimal space', color = 'gray')
    axs[0].set(xlabel = chosen_variables[0], 
               ylabel = chosen_variables[1])
    
# - # Histograms - right axis --------------------------
    
    ax = axs[1]
    for variable in chosen_variables:
        sns.histplot(samples[variable].values, 
                     line_kws = {'linewidth': 3},
                     element  = 'step',
                     stat     = 'probability',
                     alpha    = 1/3,
                     bins     = hist_bins,
                     kde      = True,
                     ax       = ax,
                     label    = variable,)
        
    ax.legend()
    
# - ### Near-optimal space plot - left axis --------------------------

    handles, labels = [], []
    
    # Set x and y as samples for this dimension
    x_samples = samples[chosen_variables[0]]
    y_samples = samples[chosen_variables[1]]
    
    # --------  Create 2D histogram --------------------
    hist, xedges, yedges = np.histogram2d(x_samples, y_samples,
                                          bins = density_bins)

    # Create grid for pcolormesh and plot
    X, Y = np.meshgrid(xedges, yedges)
    axs[0].pcolormesh(X, Y, hist.T, cmap = 'Blues', zorder = 0)
    
    # Create patch to serve as hexbin label
    hb = mpatches.Patch(color = 'tab:blue')
    
    handles.append(hb)
    labels.append('Sample density')
    
    axs[0].grid('on')
    
    # --------  Plot hull --------------------
    hull = ConvexHull(vertices[[chosen_variables[0], chosen_variables[1]]].values)
    
    # plot simplexes
    for simplex in hull.simplices:
        l0, = axs[0].plot(vertices[chosen_variables[0]][simplex],
                          vertices[chosen_variables[1]][simplex], '-', 
                          color = 'silver', label = 'faces', zorder = 0)
        
    handles.append(l0)
    labels.append('Polytope boundary')
    
    # -------- opt system --------------------
    #optimal solutions
    if opt_solution is not None:
        x_opt = opt_solution[chosen_variables[0]].values
        y_opt = opt_solution[chosen_variables[1]].values
        
        # Plot optimal solutions
        axs[0].scatter(x_opt, y_opt,
                    marker = '*', 
                    s = 1000, zorder = 4,
                    linewidth = 2, alpha = 0.85,
                    facecolor = 'gold', edgecolor = 'darkorange',)
        
        l2 = Line2D([0], [0], marker = '*', color = 'gold',
                    markeredgecolor = 'darkorange', markeredgewidth = 2,
                    markersize = 25, label = 'Optimal Solutions',
                    linestyle = '',)
        
        handles.append(l2)
        labels.append('Optimal solution')
        
    if cheb_center is not None:
        cheb_df = pd.DataFrame(np.array([cheb_center]), columns = all_variables)
        cheb_handle, = axs[0].plot(cheb_df[chosen_variables[0]], cheb_df[chosen_variables[1]],
                      marker = 'o', linestyle = '',
                      ms = 15, zorder = 3, color = 'red',)
        
        cheb_line_handle = Line2D([0], [0], linestyle = '--', 
                                  color = 'red', linewidth = 2,)
                
    if cheb_center is not None:
        handles += [cheb_handle, cheb_line_handle]
        labels  += ['Chebyshev center', 'Chebyshev line']    
    
    axs[0].legend(handles, labels, loc = 'lower center',
                  ncols = 2,
                  bbox_to_anchor=(0.5, -0.2 - 0.05*len(handles)),)
    axs[1].legend(loc = 'lower center',  ncols = 2,
                  bbox_to_anchor=(0.5, -0.2 - 0.05*len(chosen_variables)))
        
    return axs

