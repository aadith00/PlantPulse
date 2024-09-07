from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

# Create your views here
def modpage(request):
    return render(request, 'model.html')

# Load the trained model 
model = load_model(r'C:\Users\IDZ\Desktop\Trimester 4\Project\model.h5')

# Define class names 
CLASS_NAMES = ['Tomato___bacterial_spot', 'Tomato___early_blight', 'Tomato___healthy', 'Tomato___late_blight', 'Tomato___leaf_curl', 'Tomato___leaf_mold', 'Tomato___mosaic_virus', 'Tomato___septoria_leaf_spot', 'Tomato___spider_mites', 'Tomato___target_spot']

def model_prediction_view(request):
    if request.method == 'POST' and request.FILES['image']:
        # Handle file upload
        image_file = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image_file.name, image_file)
        img_path = fs.path(filename)

        try:
            # Load and preprocess the image
            img = image.load_img(img_path, target_size=(150, 150))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array /= 255.0

            # Make predictions
            predictions = model.predict(img_array)
            predicted_class_index = np.argmax(predictions, axis=1)[0]
            confidence = np.max(predictions) * 100

            # Get the predicted class name
            predicted_class_name = CLASS_NAMES[predicted_class_index]

            # Return the result to the template
            return render(request, 'model.html', {
                'prediction': predicted_class_name,
                'confidence': round(confidence, 2)
            })

        except Exception as e:
            # Handle errors
            return render(request, 'model.html', {
                'error': f"An error occurred: {str(e)}"
            })
    # If GET request, just render the page with the form
    return render(request, 'model.html')
