from flask import Flask
from flask_restful import Resource, Api, reqparse
import werkzeug
import os

Cars_FOLDER = os.path.join('static', 'cars_images')

application = Flask(__name__)
application.config['UPLOAD_FOLDER'] = Cars_FOLDER
application.config["IMAGE_UPLOADS"] = "./static/cars_images"

api = Api(application,)

class Cars(Resource):
    def get(self):
        f = open('cars.csv', 'r')
        data = f.readlines()
        f.close()

        i = 0
        del data[0]
        while i < len(data):
            data[i] = data[i].replace('\n', '')
            data[i] = data[i].split(',')
            data[i] = {
                        'nom':       data[i][0],
                        'prix':  data[i][1],
                        'disponibilite':    data[i][2],
                        'image':    data[i][3],
                    }
            i+= 1

        return {'cars': data}, 200
    
    def post(self):
        # parse arguments to dictionary
        parser = reqparse.RequestParser()
        parser.add_argument('nom', required=True)
        parser.add_argument('prix', required=True)
        parser.add_argument('disponibilite', required=True)
        parser.add_argument('image', type=werkzeug.datastructures.FileStorage, location='files')
        args = parser.parse_args()
        image_file = args['image']
        image_file.save("./static/cars_images/" + image_file.filename)

        f = open('cars.csv', 'a')
        f.write(args['nom'])
        f.write(',')
        f.write(args['prix'])
        f.write(',')
        f.write(args['disponibilite'])
        f.write(',')
        f.write(image_file.filename)
        f.write('\n')
        f.close()                       

        return {'Error': False}, 200

api.add_resource(Cars, '/cars')

if __name__ == '__main__':
    application.run()