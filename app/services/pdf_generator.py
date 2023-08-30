import os
import requests
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from PIL import Image, ImageDraw, ImageFont
from app.db.crud import get_data, get_specific_field_by_foreign_key


class PDFGenerator:
    def generate_pdf(self, set_id, image_type):
        pdf_file = f"generated_route_{set_id}.pdf"

        places = self.get_details_for_generation(set_id)
        image_path = self.generate_route_image(set_id, image_type)

        c = canvas.Canvas(pdf_file, pagesize=A4)

        # Title
        c.setFont("Helvetica", 16)
        title = "Proposed Journey"
        title_width = c.stringWidth(title, "Helvetica", 16)
        title_height = 30  # Reduced title height
        c.drawString((A4[0] - title_width) / 2, A4[1] - title_height, title)

        # Add a little space between title and image
        image_top_spacing = 10

        # Route Image
        img = Image.open(image_path)
        img_width, img_height = img.size
        image_scale = 480 / max(img_width, img_height)
        c.drawImage(
            image_path,
            (A4[0] - img_width * image_scale) / 2,
            A4[1] - title_height - img_height * image_scale - image_top_spacing,
            width=img_width * image_scale,
            height=img_height * image_scale,
        )

        # Places Details
        c.setFont("Helvetica", 14)
        places_header = "Places"
        places_header_width = c.stringWidth(places_header, "Helvetica", 14)
        places_header_height = 30
        c.drawString(
            (A4[0] - places_header_width) / 2,
            A4[1] - title_height - img_height * image_scale - places_header_height,
            places_header,
        )
        y_position = (
            A4[1] - title_height - img_height * image_scale - places_header_height - 20
        )  # Starting position for details

        details_line_height = 12
        for place in places:
            details = f"Name: {place['name']}\n"
            details += f"Rating: {place['rating']}\n"
            details += f"User Ratings Total: {place['user_ratings_total']}\n"
            details += f"Place Types: {', '.join(place['place_type'])}"

            # Calculate required height for the background
            details_lines = details.count("\n") + 1
            background_height = details_lines * details_line_height

            if (
                y_position - background_height < 50
            ):  # Start new page if content doesn't fit
                c.showPage()
                y_position = (
                    A4[1] - background_height - 20
                )  # Reset starting position for details on the next page

            # Draw pale grey background for each place
            c.setFillColor(colors.lightgrey)
            c.rect(
                50,
                y_position - background_height,
                A4[0] - 100,
                background_height,
                fill=True,
            )
            c.setFillColor(colors.black)

            c.setFont("Helvetica", 10)
            text_object = c.beginText(
                70, y_position - background_height + details_line_height + 26
            )
            text_object.setFont("Helvetica", 10)
            text_object.textLines(details)
            c.drawText(text_object)
            y_position -= background_height  # No additional spacing needed here

        c.save()

        return pdf_file

    @staticmethod
    def generate_route_image(set_id, image_type):
        image_path = os.path.join("storage", f"route_image_{set_id}.png")
        if image_type == "directions":
            data = get_specific_field_by_foreign_key(
                foreign_key=set_id,
                field_name="overview_polyline",
                collection="directions",
            )
            try:
                polygon = data[0]["overview_polyline"]
            except IndexError as e:
                # TODO: create function that will handle this
                image = Image.new("RGB", (640, 480), color=(255, 255, 255))
                draw = ImageDraw.Draw(image)
                font = ImageFont.load_default()
                text = "IMAGE NOT GENERATED"
                draw.text((320, 240), text, fill=(0, 0, 0), font=font)
                image.save(image_path)
                return image_path
            response = requests.get(
                f"https://maps.googleapis.com/maps/api/staticmap?size=640x480&path=enc:{polygon}&key={os.environ.get('GOOGLE_MAPS_API_KEY')}",
                timeout=10,
            )
        elif image_type == "pins":
            data = get_data(set_id, "places")
            markers = []
            for location in data["locations"]:
                lat = location["lat"]
                lng = location["lng"]
                markers.append(f"markers=color:red|{lat},{lng}")
            markers_query = "&".join(markers)
            response = requests.get(
                f"https://maps.googleapis.com/maps/api/staticmap?size=640x480&{markers_query}&key={os.environ.get('GOOGLE_MAPS_API_KEY')}",
                timeout=10,
            )
        else:
            # TODO: create function that will handle this
            image = Image.new("RGB", (640, 480), color=(255, 255, 255))
            draw = ImageDraw.Draw(image)
            font = ImageFont.load_default()
            text = "IMAGE NOT GENERATED"
            draw.text((320, 240), text, fill=(0, 0, 0), font=font)
            image.save(image_path)
            return image_path
        with open(image_path, "wb") as img_file:
            img_file.write(response.content)
        return image_path

    @staticmethod
    def get_details_for_generation(set_id):
        data = get_data(data_id=set_id, collection="places")
        return data["locations"]
