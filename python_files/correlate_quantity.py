def correlate_quantity():
    """Provides a correlation heatmap of the quantitiy columns"""

    heatmap = sns.heatmap(data_df.iloc[:, 13:].corr(), vmin=-1, vmax=1, annot=True)
    heatmap.set_title("Correlation Heatmap", fontdict={"fontsize": 12}, pad=12)
