# **Checkmate Fact-Checker**

A novel, state-of-the-art fact-checker designed to verify the credibility of news and information. The system uses advanced machine learning and natural language processing (NLP) techniques to detect misinformation and provide reliable results.

---

### **Features**
- **Stance Detection**: Identifies the stance of a claim relative to a given context.
- **Fake News Detection**: Analyzes and classifies news articles for authenticity.
- **Data Cleaning and Preparation**: Includes robust preprocessing for text data, such as punctuation removal and tokenization.
- **Visualization Tools**: Generates confusion matrices and performance metrics for model evaluation.

---

### **Technologies Used**
- **Libraries**:
  - NLP: `nltk`, `keras.preprocessing.text`
  - Data Manipulation: `pandas`, `zipfile`, `os`
  - Machine Learning: `xgboost`, `sklearn` (including `tree`, `naive_bayes`, `linear_model`, and `ensemble`)
  - Visualization: `matplotlib`, `seaborn`
  - Serialization: `dill`
- **Models**:
  - Decision Trees
  - Naive Bayes
  - XGBoost
  - Neural Networks (Keras)

---

### **Project Organization**
```
    ├── LICENSE                <- MIT License file
    ├── README.md              <- Project overview and usage documentation
    ├── data                   <- Data storage
    │   ├── raw                <- Raw datasets
    │   ├── processed          <- Processed data for modeling
    ├── notebooks              <- Jupyter notebooks for development
    │   ├── detect_stance.ipynb <- Stance detection implementation
    │   └── FakeNews.ipynb     <- Fake news detection pipeline
    ├── src                    <- Source code for data, features, and modeling
    ├── reports                <- Generated analysis and visualizations
    └── requirements.txt       <- Python dependencies
```

---

### **Setup and Installation**
1. **Clone the Repository**
   ```bash
   git clone https://github.com/username/checkmate-fact-checker.git
   cd checkmate-fact-checker
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Notebooks**
   - Open `detect_stance.ipynb` for stance detection.
   - Open `FakeNews.ipynb` for fake news detection.

---

### **Usage**
1. **Data Loading**:
   - Configure paths to your raw data in the notebooks.
   - Preprocess the data using the provided scripts.

2. **Model Training**:
   - Train models using provided functions for XGBoost, Naive Bayes, and others.

3. **Evaluation**:
   - Evaluate results with performance metrics and confusion matrix visualizations.

4. **Results**:
   - Visualize predictions and model performance for better interpretability.
