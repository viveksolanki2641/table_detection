import json
from PIL import Image, ImageDraw
from unstructured.partition.image import partition_image
from unstructured.documents.elements import Table
from pdf2image import convert_from_path
import os

def process_image_or_pdf(file_path: str, file_type: str, base_name: str):
    tables_data = {"tables": []}

    if file_type == "pdf":
        # Convert PDF pages to images
        pages = convert_from_path(file_path)
        page_count = len(pages)
        
        # Process each page
        for i, page in enumerate(pages):
            page_path = f"img/{base_name}_page_{i+1}.jpg"
            page.save(page_path, "JPEG")
            print(f"Processing page {i+1} of {page_count}...")
            process_image(page_path, tables_data, page_num=i+1,base_name=base_name)

        # Return the results for all pages
        output_image_path = f"img/{base_name}_processed_pages.jpg"
        output_json_path = f"img/{base_name}.json"

    else:
        # If the input is a single image
        output_image_path, output_json_path = process_image(file_path, tables_data, base_name=base_name)

    return output_image_path, output_json_path

def process_image(image_path: str, tables_data: dict, page_num=None,base_name=None):
    # Detect tables in the image
    elements = partition_image(
        filename=image_path,
        include_page_breaks=True,
        infer_table_structure=True,
        extract_images_in_pdf=False,
        extract_image_block_types=["Table"],
        extract_image_block_to_payload=False,
        starting_page_number=page_num or 1,
        extract_forms=False,
        form_extraction_skip_tables=True
    )

    # Open the image for drawing
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    # Loop through the elements and process tables
    for element in elements:
        if isinstance(element, Table):
            if hasattr(element.metadata, 'coordinates') and element.metadata.coordinates:
                coordinates = element.metadata.coordinates.points
                draw.polygon(coordinates, outline="red", width=3)

                # Add table data to the output dictionary
                tables_data["tables"].append({
                    "page": page_num or 1,
                    "coordinates": {
                        "x1": int(min(coordinates[0][0], coordinates[1][0])),
                        "y1": int(min(coordinates[0][1], coordinates[2][1])),
                        "x2": int(max(coordinates[0][0], coordinates[1][0])),
                        "y2": int(max(coordinates[0][1], coordinates[2][1]))
                    },
                    "rows": "rows",  # Placeholder for rows
                    "columns": "columns"  # Placeholder for columns
                })

    # Save the modified image using the base name
    output_image_path = f"img/{base_name}_processed.jpg"
    image.save(output_image_path)

    # Save the extracted table data to a JSON file using the base name
    output_json_path = f"img/{base_name}.json"
    with open(output_json_path, 'w') as json_file:
        json.dump(tables_data, json_file, indent=4)

    return output_image_path, output_json_path
