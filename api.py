import falcon
import mimetypes
import os
import io
import base64
import json
from falcon_cors import CORS
from waitress import serve


# class Depth:
#     def on_post(self, req, resp):
#         alg = req.media["alg"]
#         if int(alg) in algs:
#             base64_image = req.media["image"]
#             try:
#                 image = Image.open(io.BytesIO(base64.b64decode(base64_image)))
#                 depth = predict_depth(alg, image)["depth"]
#                 output = io.BytesIO()
#                 depth.save(output, format="PNG")
#                 im_data = output.getvalue()
#                 depth_map = "data:image/png;base64," + base64.b64encode(im_data).decode("utf-8")
#                 resp.status = falcon.HTTP_200
#                 resp.body = json.dumps({"image": depth_map})
#             except:
#                 resp.status = falcon.HTTP_400
#                 resp.body = json.dumps({"error": "invalid image data"})
#         else:
#             resp.status = falcon.HTTP_400
#             resp.body = json.dumps({"error": "invalid algorithm"})


# class DepthInfo:
#     def on_post(self, req, resp):
#         alg = req.media["alg"]
#         if int(alg) in algs:
#             base64_image = req.media["image"]
#             try:
#                 image = Image.open(io.BytesIO(base64.b64decode(base64_image)))
#                 result = predict_depth_info(alg, image)
#                 depth = result["depth"]
#                 resp.body = json.dumps({"image": depth.tolist(), "time": result["time"]})
#             except:
#                 resp.status = falcon.HTTP_400
#                 resp.body = json.dumps({"error": "invalid image data"})
#         else:
#             resp.status = falcon.HTTP_400
#             resp.body = json.dumps({"error": "invalid algorithm"})

class Index(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        with open("static/index.html", 'r') as f:
            resp.body = f.read()

class StaticResource(object):
    def on_get(self, req, resp, type, filename):
        # do some sanity check on the filename
        resp.status = falcon.HTTP_200
        
        resp.content_type = ""
        with open("static/" + filename, 'r') as f:
            resp.body = f.read()

class Remix(object):
    def on_post(self, req, resp, type):
        resp.status = falcon.HTTP_200
        resp.body = json.dumps({"filename": "bensound-summer.mp3"})


# allow_origins_list=['http://localhost:5000']
cors = CORS(allow_all_origins=True, allow_all_headers=True, allow_all_methods=True)

api = application = falcon.API(middleware=[cors.middleware])

api.add_route('/', Index())
api.add_route('/{filename}', StaticResource())
api.add_route('/remix/{type}', Remix())

serve(api, host="127.0.0.1", port=8000)