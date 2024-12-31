import google.generativeai as genai
import PIL.Image

image_path_1 = (
    "path/to/your/image1.jpeg"  # Replace with the actual path to your first image
)
image_path_2 = (
    "path/to/your/image2.jpeg"  # Replace with the actual path to your second image
)

sample_file_1 = PIL.Image.open(image_path_1)
sample_file_2 = PIL.Image.open(image_path_2)

# Choose a Gemini model.
model = genai.GenerativeModel(model_name="gemini-1.5-pro")

prompt = "Write an advertising jingle based on the items in both images."

response = model.generate_content([prompt, sample_file_1, sample_file_2])

print(response.text)
