import pandas as pd
import matplotlib.pyplot as plt


def csv_to_single_table_image(csv_path, image_path):
    # Read the CSV file
    df = pd.read_csv(csv_path)

    # Set up the matplotlib figure
    fig, ax = plt.subplots(
        figsize=(15, len(df) * 0.5)
    )  # Adjust the size for visibility
    ax.axis("off")  # Hide axes

    # Create the table
    table = ax.table(
        cellText=df.values, colLabels=df.columns, cellLoc="center", loc="center"
    )

    # Adjust the table's properties for better fit
    table.auto_set_font_size(False)
    table.set_fontsize(15)  # Adjust font size as needed
    table.scale(1.2, 1.2)  # Adjust scale to make the table fit in the image

    # Adjust column widths to fit content
    for key, cell in table.get_celld().items():

        row_idx, col_idx = key  # Extract row and column indices

        if col_idx == 0:
            cell.set_width(0.16)
        elif col_idx == 1:
            cell.set_width(0.08)
        elif col_idx == 2:
            cell.set_width(0.25)
        elif col_idx == 3:
            cell.set_width(0.25)
        elif col_idx == 4:
            cell.set_width(0.55)
        elif col_idx == 5:
            cell.set_width(0.06)

        elif col_idx > 5:
            cell.set_width(0.08)
        else:
            cell.set_width(0.25)  # Set a fixed width for all cells
        cell.set_height(0.04)  # Set a fixed height for all cells

    # Save the table as an image
    plt.savefig(image_path, bbox_inches="tight", dpi=400, format="pdf")


# Example usage:
csv_to_single_table_image("final-cenario5-sem1.csv", "tabela_completa.pdf")
