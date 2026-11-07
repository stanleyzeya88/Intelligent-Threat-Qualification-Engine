import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split

class ThreatClassifier:
    def __init__(self, dataset_path: str = 'data/KDDTrain+.csv'):
        self.dataset_path = dataset_path
        self.model = None
        self.preprocessor = None
        self.threshold = 0.85

    def train(self):
        cols = [
            "duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes",
            "land", "wrong_fragment", "urgent", "hot", "num_failed_logins", "logged_in",
            "num_compromised", "root_shell", "su_attempted", "num_root",
            "num_file_creations", "num_shells", "num_access_files", "num_outbound_cmds",
            "is_host_login", "is_guest_login", "count", "srv_count", "serror_rate",
            "srv_serror_rate", "rerror_rate", "srv_rerror_rate", "same_srv_rate",
            "diff_srv_rate", "srv_diff_host_rate", "dst_host_count",
            "dst_host_srv_count", "dst_host_same_srv_rate", "dst_host_diff_srv_rate",
            "dst_host_same_src_port_rate", "dst_host_srv_diff_host_rate",
            "dst_host_serror_rate", "dst_host_srv_serror_rate",
            "dst_host_rerror_rate", "dst_host_srv_rerror_rate", "target", "difficulty_level"
        ]
        df = pd.read_csv(self.dataset_path, names=cols)
        df['label'] = df['target'].apply(lambda x: 0 if x == 'normal' else 1)

        X = df.drop(columns=['target', 'difficulty_level', 'label'])
        y = df['label']

        cat_cols = X.select_dtypes(include=['object']).columns.tolist()
        num_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()

        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), num_cols),
                ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_cols),
            ]
        )
        X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        X_train_prep = self.preprocessor.fit_transform(X_train)

        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train_prep, y_train)
        print(f"✅ Classifier trained on {len(X_train):,} records.")

    def predict(self, telemetry_dict: dict) -> dict:
        df = pd.DataFrame([telemetry_dict])
        cat_categories = self.preprocessor.transformers_[1][1].categories_
        cat_features = self.preprocessor.transformers_[1][2]
        for col, cats in zip(cat_features, cat_categories):
            if col not in df.columns:
                df[col] = 'unknown'
        for col in self.preprocessor.transformers_[0][2]:
            if col not in df.columns:
                df[col] = 0.0

        X_prep = self.preprocessor.transform(df)
        prob = float(self.model.predict_proba(X_prep)[0][1])
        return {"is_attack": bool(prob >= self.threshold), "confidence": prob, "prediction": "ATTACK" if prob >= self.threshold else "BENIGN"}
