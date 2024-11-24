from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.cluster import KMeans
import numpy as np

def calculate_mse(y_true, y_pred):
    return np.mean((y_true - y_pred) ** 2)

def train_model(data):
    X = data[['Capacidad_litros', 'Tipo_Plastico']]
    y = data['ventas']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    predictions = model.predict(X_test)
    mse = calculate_mse(y_test, predictions)
    return model, mse

def train_clustering(data):
    X = data[['Capacidad_litros', 'Tipo_Plastico']]
    kmeans = KMeans(n_clusters=3)
    labels = kmeans.fit_predict(X)
    return labels

def train_logistic_regression(data):
    X = data[['Capacidad_litros', 'Tipo_Plastico']]
    y = data['ventas'] > 100

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = LogisticRegression()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    return model, accuracy
