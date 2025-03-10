from fastapi import FastAPI, UploadFile, File
import easyocr
from PIL import Image
import io
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware



reader = easyocr.Reader(["en"])
handler = Mangum(app)  # This allows Vercel to run the FastAPI app

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (be cautious in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

templates = Jinja2Templates(directory="templates")


def extract_text_from_image(image_bytes):
    """  """
    image = Image.open(io.BytesIO(image_bytes))
    # Convert the image to a format EasyOCR can read
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format="PNG")
    img_byte_arr = img_byte_arr.getvalue()
    result = reader.readtext(img_byte_arr)
    # Extract and return the text
    extracted_text_1= " ".join([text[1] for text in result])
   
   
    return extracted_text_1


@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/ocr/")

async def perform_ocr(file: UploadFile = File(...)):
    print("Hello, World!")

    try:
        if file.content_type not in ["image/png", "image/jpeg", "image/jpg"]:
            return {"error": "Invalid file type. Please upload a PNG or JPEG image."}

        image_bytes = await file.read()
        extracted_text_1 = extract_text_from_image(image_bytes)
        return {"text_1": extracted_text_1}
    except Exception as e:
        return {"error":f"An error occured: {str(e)}"}


@app.post("/hello")
async def hello_world():
    print("me")
    return {"message": "Hello, World!"}