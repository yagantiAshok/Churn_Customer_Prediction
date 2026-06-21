
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline 
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler,OneHotEncoder,OrdinalEncoder
from sklearn.metrics import accuracy_score,confusion_matrix,precision_score,recall_score,f1_score,classification_report
from imblearn.pipeline import Pipeline as imblearn_pipeline
from imblearn.over_sampling import SMOTE




def preprocessor(numeric_features,categorical_features):

    

    numerical_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("std",StandardScaler())
    ])

    categorical_pipeline = Pipeline(steps=[
        ("imputer",SimpleImputer(strategy="most_frequent")),
        ("scaler",OneHotEncoder(handle_unknown="ignore",drop="first"))


    ])



    preprocessing= ColumnTransformer([
        ("num",numerical_pipeline,numeric_features),
        ("cat",categorical_pipeline,categorical_features),

    ])

    return preprocessing




def evaluate(actual,predict):

    accuracy = accuracy_score(actual,predict)

    confusion = confusion_matrix(actual,predict)

    precision = precision_score(actual,predict)

    f1 = f1_score(actual,predict)

    recall = recall_score(actual,predict)

    return accuracy,confusion,precision,f1,recall

 


# Evaluate models

def evaluate_model(x,y,models,numeric_features,categorical_features):

    # separate dataset into train and test

    x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.25,random_state=42,shuffle=True)

    preprocessing = preprocessor(numeric_features=numeric_features,categorical_features=categorical_features)

    models_list = []

    accuracy_list_train = []

    accuracy_list_test = []

    for i in range(len(models)):

        model = list(models.values())[i]
        
        training_pipeline = imblearn_pipeline([

           ("preprocessing",preprocessing),

           ("smote",SMOTE(random_state=42)),

            ("model",model)])
        

        training_pipeline.fit(x_train,y_train)

        # making predictions 

        y_train_pred = training_pipeline.predict(x_train)
        y_test_pred = training_pipeline.predict(x_test)

        # y_test_proba = training_pipeline.predict_proba(x_test)[:,1]

        # training set performances

        model_train_accuracy,modle_train_confusion,model_train_precision,\
        model_train_f1,model_train_recall=evaluate(y_train,y_train_pred)


        # test set performances
        
        model_test_accuracy,modle_test_confusion,model_test_precision,\
        model_test_f1,model_test_recall=evaluate(y_test,y_test_pred) 

        
        print(list(models.keys())[i])
        models_list.append(list(models.keys())[i])

        # print("model performance for training Data ")
        # print("- Accuracy {:.4f}".format(model_train_accuracy))
        accuracy_list_train.append(model_train_accuracy)
        # print("- Confusion_matrix",modle_train_confusion)
        # print("- precision{:.4f}".format(model_train_precision))
        # print("- f1 {:.4f}".format(model_train_f1))
        # print("- Recall{:.4f}".format(model_train_recall))

        # print("----------------------------")


        print("model performance for test Data ",end="\t")
        print("- Accuracy {:.4f}".format(model_test_accuracy))
        print("- Confusion_matrix",modle_test_confusion)
        print("- precision{:.4f}".format(model_test_precision))
        print("- f1 {:.4f}".format(model_test_f1))
        print("- Recall{:.4f}".format(model_test_recall))
        print("Classfication_report")
        print(classification_report(y_test,y_test_pred))

        accuracy_list_test.append(model_test_accuracy)


        # model_object = training_pipeline.named_steps["model"]

        # preprocess_obj = training_pipeline.named_steps["preprocessing"]

        # feature_names = preprocess_obj.get_feature_names_out()

        # coefficients = model_object.coef_.flatten()

        # print("Feature Names:", list(feature_names))

        # print("Coefficients:", list(coefficients))

        # coef_df = pd.DataFrame(data= {"Coefficients":coefficients},index=feature_names)


    report = pd.DataFrame(list(zip(models_list,accuracy_list_test,accuracy_list_train)),columns=["Model","Test_Accuracy","Train_Accuracy"])

    return report #coef_df,x_test,y_test_pred,y_test_proba,y_test
