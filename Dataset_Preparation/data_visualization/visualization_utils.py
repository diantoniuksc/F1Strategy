import pandas as pd
import matplotlib.pyplot as plt

def visualize_compound_vs_tyre_life(doc_file, check_validity=False):
    """
    Visualize compound vs tyre life from a CSV file.
    Optionally filter for valid rows if 'is_valid' column is present.
    Assumes columns 'compound' and 'tyre_life' exist.
    """
    df = pd.read_csv(doc_file, header=0)
    if check_validity:
        if 'is_valid' in df.columns:
            df = df[df['is_valid'] == 1]
        else:
            print(f"'is_valid' column not found in {doc_file}")
            return
    compound = df['compound']
    tyre_life = df['tyre_life']
    compound_counts = compound.value_counts()
    print('Tyre count by compound:')
    print(compound_counts)
    plt.scatter(compound, tyre_life)
    plt.xlabel('Compound')
    plt.ylabel('Tyre Life')
    plt.title('Compound vs Tyre Life')
    plt.grid(True)
    plt.show()


