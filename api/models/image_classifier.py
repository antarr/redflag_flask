import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns


def load_and_train():
    toys_path = Path('images/toys')
    foods_path = Path('images/foods')
    toys = [str(path) for path in toys_path.glob('*.jpg')]
    foods = [str(path) for path in foods_path.glob('*.jpg')]
    training_data = []
    training_labels = []
    for img in toys:
        training_data.append(img)
        training_labels.append('toy')
    for img in foods:
        training_data.append(img)
        training_labels.append('food')
    df = pd.DataFrame(training_data, columns=['image'])
    df['labels'] = training_labels
    df = df.sample(frac=1).reset_index(drop=True)
    return df


if __name__ == '__main__':
    trained_model = load_and_train()

    # Save trained model as csv and hdf files
    trained_model.to_csv('examples/trained_model.csv', index=False)
    trained_model.to_hdf('examples/trained_model.h5', key='df', mode='w')

    # Create a countplot of labels in the trained model and save it as a png file
    sns.countplot(x='labels', data=trained_model)
    plt.savefig('examples/plot.png')
