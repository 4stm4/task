import xmltodict, json
from flask import Flask, request, Response
from flask_restful import Resource, Api

from app import Normalizer, PostProcessor

app = Flask(__name__)
api = Api(app)

class Extractor(Resource):

    @staticmethod
    def _request_to_data(content_type: str, data):
        if content_type == 'application/json':
            data = json.loads(data)
        elif content_type == 'application/xml':
            data = xmltodict.parse(data)
            data = data.get('data')
        return data

    def post(self):
        request_data = self._request_to_data(
            content_type=request.headers.get('Content-Type'),
            data=request.get_data(),
        )
        normalizer = Normalizer()
        post_processor = PostProcessor(
            normalizer=normalizer,
        )
        request_data = post_processor.find_lists(request_data)
        result_dict = post_processor.process_node(request_data)
        response = Response(response=json.dumps(result_dict, ensure_ascii=False), status=200, mimetype="application/json")
        return response

api.add_resource(Extractor, '/extract')
