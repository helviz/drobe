from PIL import Image

# Open the original image
img = Image.open('media/sw.jpg')  # Adjust the path if needed

# Resize the image (change the size as needed)
resized_img = img.resize((300, 300))  # Example size: 300x300 pixels

# Save the resized image
resized_img.save('media/sw_resized.jpg')

print('Image resized and saved as media/sw_resized.jpg')
