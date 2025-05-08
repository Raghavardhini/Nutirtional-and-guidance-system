from django.shortcuts import render
from .forms import FitnessForm
from .utils import predict_age, get_exercise_and_food_recommendations, handle_uploaded_image
import os

def upload_fitness_record(request):
    """
    Handle the fitness form submission and display results.
    """
    if request.method == 'POST':
        form = FitnessForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            image = form.cleaned_data['image']
            height = form.cleaned_data['height']
            weight = form.cleaned_data['weight']

            # Save uploaded image and get temp file path
            temp_file_path = handle_uploaded_image(image)

            try:
                # Predict age and get recommendations
                predicted_age_group = predict_age(temp_file_path)
                recommendations = get_exercise_and_food_recommendations(predicted_age_group, height, weight)

                # Clean up temp file
                os.remove(temp_file_path)

                # Calculate BMI
                height_in_meters = height / 100  # Convert cm to meters
                bmi = round(weight / (height_in_meters ** 2), 2)

                # Example sugar level calculation (can be customized)
                sugar_level = round((bmi / weight) * 100, 2)

                return render(request, 'result.html', {
                    'name': name,
                    'age_group': predicted_age_group,
                    'bmi': bmi,
                    'sugar_level': sugar_level,
                    'recommendations': recommendations,
                })
            except ValueError as e:
                # Clean up temp file in case of error
                os.remove(temp_file_path)
                return render(request, 'error.html', {'error': str(e)})
    else:
        form = FitnessForm()

    return render(request, 'upload.html', {'form': form})
