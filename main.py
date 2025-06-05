from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
import httpx
import json
from typing import Optional, Dict, Any
import asyncio
from urllib.parse import urlencode

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Entab Enquiry ChatBOT API", description="A chatbot for querying student application data")

# Configure CORS for MERN stack integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:8000"],  # Adjust for your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="templates")

# External API configuration
EXTERNAL_API_URL = "https://test-api.entab.info/api/form/leads"
API_KEY = os.getenv("ENTAB_API_KEY")  # Store your API key in .env file

# Configure Gemini model via LangChain
try:
    model = ChatGoogleGenerativeAI(
        model="gemini-pro",
        google_api_key=os.getenv("GOOGLE_API_KEY"),  # Store in .env file instead of hardcoding
        temperature=0.7
    )
except Exception as e:
    print(f"Warning: Failed to initialize Gemini model: {str(e)}")
    model = None


# Function to fetch data from external API
async def fetch_student_data(filters: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Fetch student data from the external API with optional filters
    """
    try:
        # Prepare query parameters
        params = {}
        if filters:
            for key, value in filters.items():
                if value is not None and value != "":
                    params[key] = value

        # Set default limit if not specified
        if 'limit' not in params:
            params['limit'] = 50

        # Add API key if available
        headers = {}
        if API_KEY:
            headers['Authorization'] = f'Bearer {API_KEY}'

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                EXTERNAL_API_URL,
                params=params,
                headers=headers
            )

            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "error": f"API request failed with status {response.status_code}",
                    "message": response.text
                }

    except httpx.TimeoutException:
        return {"error": "API request timed out"}
    except Exception as e:
        return {"error": f"Failed to fetch data: {str(e)}"}


# Function to analyze data and generate insights
def generate_data_insights(data: Dict[str, Any], user_query: str) -> str:
    """
    Generate insights about the student data based on user query
    """
    if "error" in data:
        return f"Sorry, I couldn't fetch the data: {data['error']}"

    # Extract relevant information from the data
    try:
        # Assuming the API returns data in a specific format
        # Adjust this based on the actual API response structure
        students = data.get('data', []) if isinstance(data.get('data'), list) else []
        total_count = data.get('total', len(students))

        # Generate basic statistics
        insights = []
        insights.append(f"Found {total_count} student records.")

        if students:
            # Gender distribution
            gender_counts = {}
            school_counts = {}
            class_counts = {}
            location_counts = {}
            year_counts = {}

            for student in students:
                # Gender analysis
                gender = student.get('gender', 'Unknown')
                gender_counts[gender] = gender_counts.get(gender, 0) + 1

                # School analysis
                school = student.get('schoolCode', 'Unknown')
                school_counts[school] = school_counts.get(school, 0) + 1

                # Class analysis
                class_name = student.get('class', 'Unknown')
                class_counts[class_name] = class_counts.get(class_name, 0) + 1

                # Location analysis
                location = student.get('location', 'Unknown')
                location_counts[location] = location_counts.get(location, 0) + 1

                # Year analysis
                year = student.get('appliedYear', 'Unknown')
                year_counts[year] = year_counts.get(year, 0) + 1

            # Add gender insights
            if len(gender_counts) > 1:
                gender_info = ", ".join([f"{k}: {v}" for k, v in gender_counts.items()])
                insights.append(f"Gender distribution: {gender_info}")

            # Add school insights
            if len(school_counts) > 1:
                top_schools = sorted(school_counts.items(), key=lambda x: x[1], reverse=True)[:3]
                school_info = ", ".join([f"{k}: {v}" for k, v in top_schools])
                insights.append(f"Top schools: {school_info}")

            # Add location insights
            if len(location_counts) > 1:
                top_locations = sorted(location_counts.items(), key=lambda x: x[1], reverse=True)[:3]
                location_info = ", ".join([f"{k}: {v}" for k, v in top_locations])
                insights.append(f"Top locations: {location_info}")

        # Combine insights
        result = "\n".join(insights)

        # Add context-specific response based on user query
        query_lower = user_query.lower()
        if "male" in query_lower or "female" in query_lower:
            gender_filter = "male" if "male" in query_lower else "female"
            gender_count = gender_counts.get(gender_filter.title(), 0)
            result += f"\n\nSpecifically for {gender_filter} students: {gender_count} records found."

        return result

    except Exception as e:
        return f"Error analyzing data: {str(e)}"


# Root endpoint for serving the HTML interface
@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Chat endpoint that integrates external API with AI
@app.post("/chat")
async def chat(
        user_input: str = Form(...),
        filters: str = Form(default="{}")
):
    try:
        if not user_input.strip():
            raise HTTPException(status_code=400, detail="Input cannot be empty")

        # Parse filters
        try:
            filter_dict = json.loads(filters) if filters else {}
        except json.JSONDecodeError:
            filter_dict = {}

        # Fetch data from external API
        student_data = await fetch_student_data(filter_dict)

        # Generate insights about the data
        data_insights = generate_data_insights(student_data, user_input)

        # If Gemini model is available, enhance the response
        if model:
            try:
                # Create a context-aware prompt for the AI
                context_prompt = f"""
                You are a helpful assistant analyzing student application data. 

                User Query: {user_input}

                Current Data Insights: {data_insights}

                Applied Filters: {json.dumps(filter_dict, indent=2) if filter_dict else "None"}

                Please provide a helpful, conversational response about the student data. 
                Keep it concise and relevant to the user's question. If they're asking for 
                specific information that's not in the insights, acknowledge what data is 
                available and suggest how they might refine their query or filters.
                """

                ai_response = model.invoke(context_prompt)
                response_text = ai_response.content

            except Exception as e:
                # Fallback to data insights if AI fails
                response_text = f"{data_insights}\n\n(Note: AI enhancement unavailable: {str(e)})"
        else:
            # Use just the data insights if no AI model
            response_text = data_insights

        return {"response": response_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "external_api": EXTERNAL_API_URL,
        "ai_model": "available" if model else "unavailable"
    }


# Endpoint to test external API connection
@app.get("/test-api")
async def test_external_api():
    try:
        test_data = await fetch_student_data({"limit": 5})
        return {
            "status": "success",
            "sample_data": test_data
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


# Run the application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)