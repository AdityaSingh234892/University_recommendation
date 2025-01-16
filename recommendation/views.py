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
            Based on the provided user details, recommend universities and programs:

            User Information:
            - Name: {user_data['name']}
            - Home Country: {user_data['Your_country']}
            - Preferred Study Country: {user_data['country']}
            - Program Level: {user_data['degree']}
            - GPA: {user_data['gpa_score']}
            - 12th Grade Percentage: {user_data['twelveth_percentage']}
            - TOEFL/IELTS Score: {user_data['toefl_score']}
            - DUOLINGO/PTE Score: {user_data['Duolingo_PTE']}
            - Preferred Course/Field of Study: {user_data['preferred_course']}
            for Postgratuate studies Requirment According to the user details.
             -Bachelor’s course: {user_data['bachelors_course']}

          Recommendation Requirements:
          1. Provide a list of **10 universities** that are the best fit for the user’s preferences, displayed in a table format with the following headers:
          | University Name | Fees | Global Ranking | Location |
          2. Ensure the universities:
          - Offer programs relevant to the user’s preferred field of study.
          - Include their global ranking, tuition fees, and location in the table.

          3. Tailor recommendations based on:
           - The user's academic qualifications (GPA, 12th percentage).
           - The TOEFL/IELTS score for language proficiency requirements.
           - The preferred program level and course of study.
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
