from flask import Flask, jsonify, request
import os
import logging
import traceback
import json
from utils.helpers import *
from utils.version import *
from creditRiskModels.creditRiskAPI import CreditRiskAPI
from dotenv import load_dotenv

app = Flask(__name__)

def main_configuration():
    load_dotenv(dotenv_path='./profiles/local.env')

def logging_configuration():
    fileName = os.path.join(os.getenv('PATH_LOG'),'credit-risk-API.log')
    logging.basicConfig(format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        filename=fileName,
                        level=logging.DEBUG)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    app.logger.addHandler(console)

## Servicios para consultar estado del componente

@app.route('/version-check', methods=['GET'])
def version_check():
    return f'current Version: {__current_version__} \n old version: {__old_version__}'

@app.route('/health-check', methods=['GET'])
def health_check():
    return 'OK'

## Servicios para consumir el componente

@app.route("/getFeaturesByUserId", methods=['POST','GET'])
def getFeaturesByUserId():
    if request.method == 'GET':
        try:
            userId = request.args.get('id', type=str)
            body = {'id': userId}
            creditRiskAPI = CreditRiskAPI()
            code, message, response = creditRiskAPI.getFeaturesByUserId(body)
            result = ''
            if code == CODE_OK:
                result = f'UserId= {userId} has the following features: <br>' + \
                        f'{"=="*10}<br>' + \
                        f'nb_previous_loans= {response["nb_previous_loans"]}<br>' + \
                        f'avg_amount_loans_previous= {response["avg_amount_loans_previous"]}<br>' + \
                        f'age= {response["age"]}<br>' + \
                        f'years_on_the_job= {response["years_on_the_job"]}<br>' + \
                        f'flag_own_car= {response["flag_own_car"]}<br>'
            else:
                result = f'ERROR in the consult <br>' + \
                        f'{"=="*10}<br>' + \
                        f'Code= {code}<br>' + \
                        f'message= \"{message}\"'
            return result
        except Exception as ex:
            error_string= traceback.format_exc()
            logging.info(f'Error getFeaturesByUserId: {str(ex)}')
            logging.info(f'Error getFeaturesByUserId: {error_string}')
            errorHtml = f'Error al procesar + {error_string}'

            return f'{errorHtml}'
    elif request.method == 'POST':
        try:
            body = request.get_json()

            creditRiskAPI = CreditRiskAPI()
            code, message, response = creditRiskAPI.getFeaturesByUserId(body)
            result = {
                'code': code,
                'message': message,
                'data': None
            }
            if code == CODE_OK:
                result['data'] = {}
                result['data'] = response

            return result
        except Exception as ex:
            error_string= traceback.format_exc()
            logging.info(f'Error getFeaturesByUserId POST: {str(ex)}')
            logging.info(f'Error getFeaturesByUserId POST: {error_string}')
            return {'code': CODE_ERROR_COMPILE,
                    'message': dict_code_message[CODE_ERROR_COMPILE] + error_string}

@app.route("/prediction", methods=['POST'])
def prediction():
    try:
        body = request.get_json()
        creditRiskAPI = CreditRiskAPI()
        code,message,response = creditRiskAPI.predict(body)
        result = { 'code':code, 'message': message,'data':None}
        if code == CODE_OK:
            result['data'] = {'prediction':response['prediction']}

        return result
    except Exception as ex:
        error_string= traceback.format_exc()
        logging.info(f'Error Visualize POST: {str(ex)}')
        logging.info(f'Error Visualize POST: {error_string}')
        return {'code': CODE_ERROR_COMPILE,
                'message': dict_code_message[CODE_ERROR_COMPILE] + error_string}

if __name__ == '__main__':
    logging.info("esta es una prueba ")
    main_configuration()
    logging_configuration()
    logging.info("Starting web server.....")
    # local setup
    # app.run(host='0.0.0.0', port=6924, debug=False)

    # heroku setup
    port = int(os.environ.get("PORT", 6924)) 
    app.run(host='0.0.0.0', port=port) 

# servicio getFeaturesByUserId/GET -> http://0.0.0.0:6924/getFeaturesByUserId?id=1231
# servicio version-check -> http://0.0.0.0:6924/version-check
# servicio health-check -> http://0.0.0.0:6924/health-check

