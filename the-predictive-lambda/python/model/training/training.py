import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import joblib

def load_chipotle_data():
    return pd.read_csv("chipotle_stores.csv")

#clean our data
stores = load_chipotle_data()
stripped_stores = stores[["address", "latitude", "longitude"]].copy()
stripped_stores = stripped_stores.drop_duplicates(keep="first")

#split our data into training and test set
train_set, test_set = train_test_split(stripped_stores, test_size=0.2, random_state=42)

#split data from labels
train_set_no_labels = train_set.drop("address", axis=1)
train_set_labels = train_set["address"].copy()

#train model
model = KNeighborsClassifier(n_neighbors=2, weights="distance", algorithm="auto")
model.fit(train_set_no_labels, train_set_labels)

#export model
joblib.dump(model, 'chipotle.pkl')