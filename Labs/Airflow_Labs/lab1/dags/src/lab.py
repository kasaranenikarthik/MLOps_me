import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from kneed import KneeLocator
import pickle
import os


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_DIR = os.path.join(BASE_DIR, "model")
TMP_DIR = os.path.join(BASE_DIR, "tmp")

os.makedirs(TMP_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

def load_data():
    """
    Loads CSV data and saves it to a temporary pickle file.
    Returns the file path (string) for downstream use.
    """
    df = pd.read_csv(os.path.join(DATA_DIR, "file.csv"))
    file_path = os.path.join(TMP_DIR, "raw_data.pkl")

    with open(file_path, "wb") as f:
        pickle.dump(df, f)

    return file_path  #This is XCom-safe (a string)

def data_preprocessing(file_path):
    """
    Loads the raw data from a pickle file, preprocesses it,
    and saves the result to another pickle file.
    Returns the preprocessed file path.
    """
    with open(file_path, "rb") as f:
        df = pickle.load(f)

    df = df.dropna()
    clustering_data = df[["BALANCE", "PURCHASES", "CREDIT_LIMIT"]]
    scaler = MinMaxScaler()
    transformed = scaler.fit_transform(clustering_data)

    processed_path = os.path.join(TMP_DIR, "processed_data.pkl")
    with open(processed_path, "wb") as f:
        pickle.dump(transformed, f)

    return processed_path  #XCom-safe

def build_save_model(processed_data_path, filename):
    """
    Loads preprocessed data, builds a KMeans model, saves the model,
    and returns the list of SSE values (JSON-serializable).
    """
    with open(processed_data_path, "rb") as f:
        data = pickle.load(f)

    kmeans_kwargs = {
        "init": "random",
        "n_init": 10,
        "max_iter": 300,
        "random_state": 42,
    }
    sse = []
    for k in range(1, 50):
        kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
        kmeans.fit(data)
        sse.append(kmeans.inertia_)

    model_path = os.path.join(MODEL_DIR, filename)
    with open(model_path, "wb") as f:
        pickle.dump(kmeans, f)

    return sse  #XCom-safe (list of floats)

def load_model_elbow(filename, sse):
    """
    Loads the model from disk, reads test data,
    determines optimal number of clusters, and returns first prediction.
    """
    model_path = os.path.join(MODEL_DIR, filename)
    with open(model_path, "rb") as f:
        model = pickle.load(f)

    test_df = pd.read_csv(os.path.join(DATA_DIR, "test.csv"))

    # Assume test data already has same preprocessing as training
    kl = KneeLocator(range(1, 50), sse, curve="convex", direction="decreasing")

    print(f"Optimal number of clusters: {kl.elbow}")

    prediction = model.predict(test_df)

    return int(prediction[0])  #JSON-safe (int)
