import os

CODE_OK = 1
CODE_ERROR_INVALID_NUMBER_FEATURES = -11
CODE_ERROR_INVALID_FEATURES = -20
CODE_ERROR_INVALID_FEATURE_NB_PREVIOUS_LOAN = -12
CODE_ERROR_INVALID_FEATURE_AVG_AMOUNT_LOANS_PREVIOUS = -13
CODE_ERROR_INVALID_FEATURE_AGE = -14
CODE_ERROR_INVALID_FEATURE_YEARS_ON_THE_JOB = -15
CODE_ERROR_INVALID_FEATURE_FLAG_OWN_CAR = -16
CODE_ERROR_INVALID_ID_USER = -17
CODE_ERROR_NON_EXISTENT_ID_USER = -18
CODE_ERROR_COMPILE = -19
CODE_ERROR_LOT_ERRORS = -21

dict_code_message = {}
dict_code_message[CODE_OK] = 'Success Consult'
dict_code_message[CODE_ERROR_INVALID_NUMBER_FEATURES] = 'Invalid number of features.'
dict_code_message[CODE_ERROR_INVALID_FEATURE_NB_PREVIOUS_LOAN] = 'Invalid type and value for nb_previous_loan feature'
dict_code_message[CODE_ERROR_INVALID_FEATURE_AVG_AMOUNT_LOANS_PREVIOUS] = 'Invalid type and value for avg_amount_loans_previous feature'
dict_code_message[CODE_ERROR_INVALID_FEATURE_AGE] = 'Invalid type and value for age feature'
dict_code_message[CODE_ERROR_INVALID_FEATURE_YEARS_ON_THE_JOB] = 'Invalid type and value for year_on_the_job feature'
dict_code_message[CODE_ERROR_INVALID_FEATURE_FLAG_OWN_CAR] = 'Invalid type and value for flag_own_car feature'
dict_code_message[CODE_ERROR_INVALID_ID_USER] = 'Invalid type and value for userId'
dict_code_message[CODE_ERROR_NON_EXISTENT_ID_USER] = 'Non existent userId'
dict_code_message[CODE_ERROR_COMPILE] = 'Compile error.'
dict_code_message[CODE_ERROR_INVALID_FEATURES] = 'Invalid features.'
dict_code_message[CODE_ERROR_LOT_ERRORS] = 'Many errors found:'


MODEL_DEFAULT = 'model_risk_RandomForestClassifier_withDataSet01.joblib'