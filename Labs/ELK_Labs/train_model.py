import logging
import time
import numpy as np
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, confusion_matrix, mean_squared_error
from datetime import datetime, timedelta

# Configure the logging module
logging.basicConfig(filename='logstash/training.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the Diabetes dataset once
data = load_diabetes()
X, y = data.data, data.target

# Track start time
start_time = datetime.now()
end_time = start_time + timedelta(minutes=20)

# Loop to retrain the model every 2 minutes with added randomness, stopping after 20 minutes
while datetime.now() < end_time:
    # Split the data into training and testing sets with a different random state each time
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=np.random.randint(1000))

    # Add random noise to the training data to increase randomness
    feature_noise = np.random.normal(0, 0.1, X_train.shape)
    X_train_noisy = X_train + feature_noise

    # Randomly add noise to the target
    label_noise = np.random.normal(0, 0.1, y_train.shape)  # 10% label noise
    y_train_noisy = y_train + label_noise

    # Initialize the Linear Regression model
    model = LinearRegression()

    # Logging important information
    logging.info("Starting model training...")
    logging.info(f"Number of training samples: {len(X_train)}")
    logging.info(f"Number of testing samples: {len(X_test)}")

    # Train the model with noisy data and log progress
    try:
        model.fit(X_train_noisy, y_train_noisy)
        logging.info("Model training completed.")
    except Exception as e:
        logging.error(f"Model training failed: {e}")
        continue

    # Evaluate the model
    #GIve me code for metrics of linear regression



    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    logging.info(f"Model Mean Squared Error: {mse:.2f}")
    logging.info(f"Model R^2 Score: {r2:.2f}")

    score = model.score(X_test, y_test)
    logging.info(f"Model accuracy on test data: {score:.2f}")

    # Log model parameters
    logging.info(f"Model coefficients: {model.coef_}")
    logging.info(f"Model intercept: {model.intercept_}")

    # Wait 2 minutes before retraining
    logging.info("Waiting 2 minutes before next training run...\n")
    time.sleep(120)

logging.info("Training loop finished after 20 minutes.")
