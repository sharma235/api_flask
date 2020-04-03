import os
from flask import Flask, request, abort, jsonify

api = Flask(__name__)
api.config['MAX_CONTENT_LENGTH'] = 100 *1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@api.route("/files/<filename>", methods=["POST"])
def post_file(filename):
	if "/" in filename:
		abort(400, "no subdirectories allowed")
	imagefile = request.files.get('image', '')
	if allowed_file(imagefile.filename):
		imagefile.save('image/%s' %(filename))
		return "upload successful", 201
	else:
		return "not an image file", 401


@api.errorhandler(413)
def error413(e):
    return "Size of file exceeded",401


if __name__ == "__main__":
    api.run(debug=True, port=8000)