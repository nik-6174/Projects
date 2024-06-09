import pandas as pd
from sklearn import model_selection
import os


class CrossValidation:
    def __init__(
            self,
            df, 
            target_cols,
            shuffle,
            problem_type="binary_classification",
            num_folds=5,
            random_state=42
        ):
        self.dataframe = df
        self.target_cols = target_cols
        self.num_targets = len(target_cols)
        self.problem_type = problem_type
        self.num_folds = num_folds
        self.shuffle = shuffle
        self.random_state = random_state

        if self.shuffle:
            self.dataframe = self.dataframe.sample(frac=1).reset_index(drop=True)
        
        self.dataframe['kfold'] = -1

    def split(self):
        if self.problem_type in ("binary_classification", "multi_classification"):
            if self.num_targets > 1:
                raise Exception("Invalid number of targets for this problem type")
            target = self.target_cols[0]
            if self.dataframe[target].nunique() == 1:
                raise Exception("Only one unique target value found!")
            
            kf = model_selection.StratifiedKFold(n_splits=self.num_folds)
        
            for fold, (train_idx, val_idx) in enumerate(kf.split(X=self.dataframe, y=self.dataframe[target].values)):
                self.dataframe.loc[val_idx, "kfold"] = fold
        
        elif self.problem_type == ("single_col_regression", "multi_col_regression"):
            if self.num_targets > 1 and self.problem_type == "single_col_regression":
                raise Exception("Invalid number of targets for this problem type")
            if self.num_targets < 2 and self.problem_type == "multi_col_regression":
                raise Exception("Invalid number of targets for this problem type")
            kf = model_selection.KFold(n_splits=self.num_folds)
            for fold, (train_idx, val_idx) in enumerate(kf.split(X=self.dataframe)):
                self.dataframe.loc[val_idx, "kfold"] = fold
        
        elif self.problem_type.startswith("holdout_"):
            holdout_percentage = int(self.problem_type.split("_")[1])
            num_holdout_samples = int(len(self.dataframe) * holdout_percentage / 100)
            self.dataframe.loc[:len(self.dataframe) - num_holdout_samples, 'kfold'] = 0
            self.dataframe.loc[len(self.dataframe) - num_holdout_samples:, 'kfold'] = 1

        else:
            raise Exception("Problem type not defined!")



        return self.dataframe
    
if __name__ == "__main__":
    df = pd.read_csv(os.path.join("input", "train.csv"), )
    cv = CrossValidation(df, target_cols=["target"], shuffle=False, problem_type="holdout_20")
    df_split = cv.split()
    print(df_split.head())
    print(df_split.kfold.value_counts())
