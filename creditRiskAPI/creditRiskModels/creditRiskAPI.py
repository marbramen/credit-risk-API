from joblib import dump, load
from utils.helpers import *
import os
import pandas as pd

class CreditRiskAPI(object):
    def __init__(self):
        # pathModel = os.getenv('MODEL_LOCATION')
        # nameModel = os.getenv('NAME_MODEL')
        # pathFeatures = os.getenv('FEATURES_LOCATION')
        # nameFeatures = os.getenv('NAME_FEATURES')

        pathModel = os.path.dirname(__file__) + "/trained-model"
        nameModel = 'model_risk_RandomForestClassifier_withDataSet01.joblib'
        pathFeatures = os.path.dirname(__file__) + "/feature-set"
        nameFeatures = 'feature_set.csv'

        self.numberFeatures = 5
        self.featuresL = ['nb_previous_loans',
                          'avg_amount_loans_previous',
                          'age',
                          'years_on_the_job',
                          'flag_own_car']
        self.CREDIT_RISK_MODEL_LOCATION = os.path.join(pathModel, nameModel)
        self.DATASET_FEATURE_FILE = os.path.join(pathFeatures, nameFeatures)

    def predict(self, request):
        message, response =  '', None

        # validation request feature vector
        codeList = self.validationFeautureVector(request)
        if len(codeList) == 1 and codeList[0] == CODE_OK:
            code = CODE_OK
            requestList = []
            for it in self.featuresL:
                requestList.append(request[it])

            modelCreditRisk = load(self.CREDIT_RISK_MODEL_LOCATION)
            resultModel = modelCreditRisk.predict([requestList])
            response = {}
            response['prediction'] = resultModel.tolist()[0]
        elif len(codeList) == 1 and codeList[0] != CODE_OK:
            code = codeList[0]
            print(f'codigo de error: {code}')
            message = dict_code_message[codeList[0]]
        else:
            code = CODE_ERROR_LOT_ERRORS
            message = dict_code_message[CODE_ERROR_LOT_ERRORS]
            for it in codeList:
                message = message + dict_code_message[it] + " \n "

        return code, message, response

    def getFeaturesByUserId(self,request):
        message, response = '', None

        ## Validation userId(id)
        code = self.validationUserId(request['id'])
        if code  == CODE_OK:
            response = {
                'nb_previous_loans': None,
                'avg_amount_loans_previous': None,
                'age': None,
                'years_on_the_job': None,
                'flag_own_car': None
            }
            print(self.DATASET_FEATURE_FILE)
            print('valor de impresion  ' + request['id'])
            df = pd.read_csv(os.path.join(self.DATASET_FEATURE_FILE),sep=';', dtype={'id':'string'})
            dfTemp = df[df['id']== request['id']]
            values = dfTemp.values

            if len(values) != 0:
                response['nb_previous_loans'] = values[0][1]
                response['avg_amount_loans_previous'] = values[0][2]
                response['age'] = values[0][3]
                response['years_on_the_job'] = values[0][4]
                response['flag_own_car'] = values[0][5]
            else:
                code = CODE_ERROR_NON_EXISTENT_ID_USER
                message = dict_code_message[code]
        else:
            message = dict_code_message[code]

        return code, message, response

    def validationFeautureVector(self, dictFeatureVec):
        if len(dictFeatureVec) != 5:
            print(str(dictFeatureVec))
            return [CODE_ERROR_INVALID_NUMBER_FEATURES]

        # all features are numeric
        # validation for correct features
        flagInvalidFeatures = False
        for it in self.featuresL:
            flagInvalidFeatures = flagInvalidFeatures or (it not in dictFeatureVec)
        if flagInvalidFeatures:
            return [CODE_ERROR_INVALID_FEATURES]

        listCodeResult = []
        if not isinstance(dictFeatureVec['nb_previous_loans'], int):
            listCodeResult.append(CODE_ERROR_INVALID_FEATURE_NB_PREVIOUS_LOAN)
        elif dictFeatureVec['nb_previous_loans'] < 0:
            listCodeResult.append(CODE_ERROR_INVALID_FEATURE_NB_PREVIOUS_LOAN)

        if (not isinstance(dictFeatureVec['avg_amount_loans_previous'], float)) and (not isinstance(dictFeatureVec['avg_amount_loans_previous'], int)):
            listCodeResult.append(CODE_ERROR_INVALID_FEATURE_AVG_AMOUNT_LOANS_PREVIOUS)
        elif dictFeatureVec['avg_amount_loans_previous'] <= 0:
            print("entro aca")
            listCodeResult.append(CODE_ERROR_INVALID_FEATURE_AVG_AMOUNT_LOANS_PREVIOUS)

        if not isinstance(dictFeatureVec['age'], int):
            listCodeResult.append(CODE_ERROR_INVALID_FEATURE_AGE)
        elif dictFeatureVec['age'] <= 0:
            listCodeResult.append(CODE_ERROR_INVALID_FEATURE_AGE)

        if not isinstance(dictFeatureVec['years_on_the_job'], int):
            listCodeResult.append(CODE_ERROR_INVALID_FEATURE_YEARS_ON_THE_JOB)
        elif dictFeatureVec['years_on_the_job'] < 0:
            listCodeResult.append(CODE_ERROR_INVALID_FEATURE_YEARS_ON_THE_JOB)

        if not isinstance(dictFeatureVec['flag_own_car'], int):
            listCodeResult.append(CODE_ERROR_INVALID_FEATURE_FLAG_OWN_CAR)
        elif dictFeatureVec['flag_own_car'] not in [0,1] :
            listCodeResult.append(CODE_ERROR_INVALID_FEATURE_FLAG_OWN_CAR)

        if len(listCodeResult) == 0:
            listCodeResult.append(CODE_OK)

        return listCodeResult

    def validationUserId(self, id):
        # check if 'id' is a string
        if not isinstance(id, str):
            return CODE_ERROR_INVALID_ID_USER
        # check if 'id' a numeric string
        if not id.isnumeric():
            return CODE_ERROR_INVALID_ID_USER
        return CODE_OK

