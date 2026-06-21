
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from xgboost import XGBClassifier


models = {
    "LogisticRegression":LogisticRegression,
    "SVC":SVC,
    "DecisionTreeClassifier":DecisionTreeClassifier,
    "randomforestclassifier":RandomForestClassifier,
    "adaboostclassifier":AdaBoostClassifier,
    "xgboostclassifier":XGBClassifier

}


