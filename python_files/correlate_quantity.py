def correlate_quantity():
    """Provides a correlation heatmap of the quantitiy columns"""

    heatmap = sns.heatmap(data_df.iloc[:, 13:].corr(), vmin=-1, vmax=1, annot=True)
    heatmap.set_title("Correlation Heatmap", fontdict={"fontsize": 12}, pad=12)
    ax = heatmap.axes
    ax.text(
        0,
        -0.35,
        "Source: Agricultural total factor productivity (USDA), Our World in Data 2021",
        fontsize=12,
        ha="left",
        transform=heatmap.figure.transFigure,
    )
