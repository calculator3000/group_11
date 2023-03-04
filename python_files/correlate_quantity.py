def correlate_quantity():
    """Provides a correlation heatmap of the quantity columns"""

    correlation = self.data_df.iloc[:, 13:].corr()
    mask = np.zeros_like(correlation, dtype=bool)
    mask[np.triu_indices_from(mask)] = True

    heatmap = sns.heatmap(correlation, vmin=-1, vmax=1, annot=True, mask=mask)
    heatmap.set_title("Correlation Heatmap", fontdict={"fontsize": 12}, pad=12)
    ax_figure = heatmap.axes
    ax_figure.text(
        0,
        -0.35,
        "Source: Agricultural total factor productivity (USDA), Our World in Data 2021",
        fontsize=12,
        ha="left",
        transform=heatmap.figure.transFigure,
    )
