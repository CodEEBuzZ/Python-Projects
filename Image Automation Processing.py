# In this project this code can create more than 100+ certificates automatically. Here all the font type, size are give. Also given the size and location also. It can access the csv file of the Certificate and can do the changes.
# Template access or create from canva and edit or insertion done from the python code.
import pandas as pd
from PIL import Image, ImageDraw, ImageFont, ImageOps
import os

# Load CSVs
data_df = pd.read_csv(r"C:\Users\Saikat Munshib\Documents\Information 1.csv")     # Name, Topic, Roll Number
details_df = pd.read_csv(r"C:\Users\Saikat Munshib\Documents\Information 2.csv")    # Subject, Date, Semester

# Use the first row of details.csv for fixed data
subject = details_df.loc[0, 'Subject']
date = details_df.loc[0, 'Date']
semester = details_df.loc[0, 'Semester']

# Set up font
font_path = 'times.ttf'
font_size = 47
font = ImageFont.truetype(font_path, font_size)

# Output directory
output_dir = 'certificates'
os.makedirs(output_dir, exist_ok=True)

# Generate certificates
for index, row in data_df.iterrows():
    name = row['Name']
    topic = row['Topic']
    roll = row['Roll No.']

    # Load template
    cert = Image.open(r"C:\Users\Saikat Munshib\Downloads\Final Certificate.png")
    draw = ImageDraw.Draw(cert)

    # Adjust positions (x, y) as per your template
    text_color = '#380d0a'
    draw.text((410, 543), name, font=font, fill=text_color)
    draw.text((410, 596), str(roll), font=font, fill=text_color)
    draw.text((410, 753), topic, font=font, fill=text_color)
    draw.text((410, 700), subject, font=font, fill=text_color)
    draw.text((410, 649), semester, font=font, fill=text_color)
    draw.text((910, 650), date, font=font, fill=text_color)
    
    #Signature
    signature_1 = Image.open(r"C:\Users\Saikat Munshib\Pictures\Screenshots\Screenshot 2025-04-10 173242.png").convert("RGBA")
    signature_2 = Image.open(r"C:\Users\Saikat Munshib\Pictures\Screenshots\Screenshot 2025-04-10 173242.png").convert("RGBA")
    
    signature_1 = signature_1.resize((300,91))
    signature_2 = signature_2.resize((300,91))
    
    cert.paste(signature_1, (267,1060) ,signature_1)
    cert.paste(signature_2, (1407,1059) ,signature_2)
    
    try:
        image_path = os.path.join(r"C:\Users\Saikat Munshib\Desktop\images", f"{name}.jpg")  # You can use roll instead if safer
        photo = Image.open(image_path).convert("RGBA")
        photo = photo.resize((297, 297))

        # Create circular mask
        mask = Image.new('L', (297, 297), 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.ellipse((0, 0, 297, 297), fill=255)

        # Apply mask to photo
        circular_photo = ImageOps.fit(photo, (297, 297))
        circular_photo.putalpha(mask)

        # Paste circular photo (adjust position)
        cert.paste(circular_photo, (1560, 524), circular_photo)

    except FileNotFoundError:
        print(f"Photo not found for: {name}")



    # Save certificate
    output_path = os.path.join(output_dir, f"{name}_{roll}.png")
    cert.show()

    cert.save(output_path)

    print(f"Generated: {output_path}")
