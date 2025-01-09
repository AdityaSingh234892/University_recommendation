import openai
from django.shortcuts import render
from django.http import JsonResponse
from .forms import UserForm
from .models import User
from django.conf import settings
import logging

# Set OpenAI API key from settings
openai.api_key = settings.OPENAI_API_KEY

# Configure logging
logger = logging.getLogger(__name__)

def get_recommendations(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # Save the form data to the database
            user_instance = form.save()

            # Extract cleaned data
            user_data = form.cleaned_data
            logger.info(f"Form data received: {user_data}")

            # Prepare the OpenAI prompt
            prompt = f"""
            Based on the following information, suggest universities:
            Name: {user_data['name']}
            My Country: {user_data['Your_country']} 
            the Country for Study: {user_data['country']}
            Degree: {user_data['degree']}
            GPA: {user_data['gpa_score']}
            12th Percentage: {user_data['twelveth_percentage']}
            TOEFL/IELTS: {user_data['toefl_score']}
            Preferred Course: {user_data['preferred_course']}
            Provide the recommendation in a table format with columns: 
            University Name, Fees, Ranking, Location. The value of header should be:
            'University Name','Fees','Ranking','Location'. 
            Provide exactly 10 universities with the best fit for the user's preferences, 
            and include information about their Global Ranking.
            """

            try:
                # Call OpenAI API
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "system", "content": prompt}],
                    max_tokens=500
                )

                # Extract recommendation content
                recommendation = response.choices[0].message['content']
                logger.info(f"OpenAI Response: {recommendation}")

                # Return the recommendation as JSON
                return JsonResponse({"status": "success", "recommendation": recommendation})
            except Exception as e:
                # Log and return error
                logger.error(f"Error generating recommendation: {e}")
                return JsonResponse({"status": "error", "message": str(e)})

        else:
            # Log and return form errors
            logger.error(f"Form validation failed: {form.errors}")
            return JsonResponse({"status": "error", "message": "Invalid form data", "errors": form.errors})

    # For GET requests, render the form
    form = UserForm()
    return render(request, 'index.html', {'form': form})
