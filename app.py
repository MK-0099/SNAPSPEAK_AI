import gradio as gr
from transformers import VisionEncoderDecoderModel, ViTFeatureExtractor, AutoTokenizer
import torch
from PIL import Image

# Load the pre-trained model and tokenizer
model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
feature_extractor = ViTFeatureExtractor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

max_length = 100
num_beams = 4
gen_kwargs = {"max_length": max_length, "num_beams": num_beams}

def generate_description(image):
    try:
        pixel_values = feature_extractor(images=image, return_tensors="pt").pixel_values
        pixel_values = pixel_values.to(device)

        output_ids = model.generate(pixel_values, **gen_kwargs)

        preds = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
        preds = [pred.strip() for pred in preds]

        return preds[0]
    except Exception as e:
        return f"An error occurred: {e}"

# Create the Gradio interface
interface = gr.Interface(
    fn=generate_description,
    inputs=gr.Image(type="numpy"),
    outputs=gr.Textbox(label="Image Description"),
    title="Image Upload and Description Generator",
    description="Upload an image to get a description generated by a pre-trained model.",
)

if __name__ == "__main__":
    interface.launch()
import gradio as gr  # Import Gradio for creating the interface
from transformers import BlipForConditionalGeneration, BlipProcessor  # Import BLIP model and processor
from PIL import Image  # Import PIL for image processing
import torch  # Import PyTorch

# Load the larger pre-trained model and processor
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")

device = "cuda" if torch.cuda.is_available() else "cpu"  # Check if CUDA is available, else use CPU
model.to(device)  # Move the model to the selected device

max_length = 150  # Increase the maximum length for longer descriptions
num_beams = 8  # Increase the number of beams for more diverse outputs
gen_kwargs = {"max_length": max_length, "num_beams": num_beams}  # Generation arguments for the model

def generate_description(image):
    try:
        # Preprocess the image
        pixel_values = processor(images=image, return_tensors="pt").pixel_values
        pixel_values = pixel_values.to(device)  # Move pixel values to the selected device

        # Generate the caption
        output_ids = model.generate(pixel_values, **gen_kwargs)
        caption = processor.decode(output_ids[0], skip_special_tokens=True)

        return caption
    except Exception as e:
        return f"An error occurred: {e}"

# Create the Gradio interface
interface = gr.Interface(
    fn=generate_description,
    inputs=gr.Image(type="numpy", label=""),
    outputs=gr.Textbox(label="The first look description of the image"),
    title="SnapSpeak: The Picture Translator",
    description="Upload an image to get a description generated by the BLIP model",
   
)

if __name__ == "__main__":
    interface.launch(share=True)