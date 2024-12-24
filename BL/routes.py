
from io import BytesIO

from flask import Flask, Response, request, json, jsonify,send_file
from flask_cors import CORS
from BL.modules import GeminiModule, SentimentModule, MemeImageModule
from PIL import Image
from DAL.mongo_module import MongoModule
import matplotlib.pyplot as plt
import io


app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://localhost:5173"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    },
    r"/memes/*": {
        "origins": ["http://localhost:3000", "http://localhost:5173"],
        "methods": ["GET", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
connection_string = "mongodb://localhost:5000"
sentiment_module = SentimentModule(positive_threshold=0.3)
gemini_module = GeminiModule(api_key='private')
mongo_config = {
            'database': 'meme_db',
            'collection': 'memes'
        }
mongo_module = MongoModule(mongo_config, connection_string)
image_path = 'https://picsum.photos/200'
mem_module = MemeImageModule()

def create_meme(
        meme_type: str = "custom_image"  # Default to "gradient"
):
    # Get an affirmation text
    affirmation = gemini_module.get_affirmation_text()

    while affirmation and not sentiment_module.is_positive(affirmation):
        affirmation = gemini_module.get_affirmation_text()

    # Generate meme based on the selected type
    if meme_type == "custom_image":
        meme_image = MemeImageModule.create_meme_with_downloaded_image(mem_module,affirmation, image_path)
    elif meme_type == "solid_background":
        meme_image = MemeImageModule.create_meme_with_solid_background(mem_module,affirmation)
    elif meme_type == "gradient":
        meme_image = MemeImageModule.create_meme_with_gradient(mem_module,affirmation)
    else:
        raise ValueError("Invalid meme type. Choose 'custom_image', 'gradient', or 'solid_background'.")

    # Convert image to binary format
    img_byte_arr = BytesIO()
    meme_image.save(img_byte_arr, format="PNG")
    image_binary = img_byte_arr.getvalue()

    # Save the meme to MongoDB
    return mongo_module.save_meme(image_binary)


@app.route('/')
def base():
    return Response(
        response=json.dumps({"Status": "UP"}),
        status=200,
        mimetype='application/json'
    )

@app.route('/memes', methods=['GET'])
def get_memes():
    data = request.json
    if data is None or data == {}:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    mongo_api = MongoModule(data, connection_string)
    response = mongo_api.get_all_memes()
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')


@app.route('/memes/<meme_id>', methods=['GET'])
def get_meme_by_id(meme_id):
    # Remove the requirement for JSON data in GET request
    response = mongo_module.get_meme(meme_id)

    if response and 'binary_data' in response:
        # Return the binary data directly as an image
        return send_file(
            io.BytesIO(response['binary_data']),
            mimetype='image/jpeg'
        )

    return Response(
        response=json.dumps({"Error": "Meme not found"}),
        status=404,
        mimetype='application/json'
    )
@app.route('/mongodb', methods=['POST'])
def mongo_write():
    data = request.json
    if data is None or data == {} or 'Document' not in data:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    mongo_api = MongoModule(data, connection_string)
    response = mongo_api.save_meme(data)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')


@app.route('/api/meme', methods=['GET', 'OPTIONS'])
def get_new_meme():
    if request.method == 'OPTIONS':
        # Handle preflight request
        return '', 204

    try:
        data = create_meme()
        return jsonify(data)
    except Exception as e:
        print(f"Meme Generation Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/mongodb', methods=['DELETE'])
def mongo_delete():
    data = request.json
    if data is None or data == {} or 'Delete' not in data:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    mongo_api = MongoModule(data, connection_string)
    response = mongo_api.delete_meme(data)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

#for debugging
def display_meme(meme_id):
    # Retrieve the image binary from MongoDB
    meme = mongo_module.get_meme(meme_id)

    # Create an image from the binary data
    image = Image.open(io.BytesIO(meme['binary_data']))

    # Display the image
    plt.figure(figsize=(10, 10))
    plt.imshow(image)
    plt.axis('off')  # Hide axes
    plt.title('Generated Meme')
    plt.show()


if __name__ == "__main__":
    app.run(debug=True, port=5173, host='0.0.0.0')
    #meme_image = create_meme(meme_type="gradient")
    #meme_id = meme_image['meme_id']
    #display_meme(meme_id)
