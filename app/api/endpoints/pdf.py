from fastapi import APIRouter
from fastapi.responses import FileResponse
from app.services.pdf_generator import PDFGenerator

pdf_generator = PDFGenerator()

router = APIRouter()


@router.get("/pdf/{set_id}", response_class=FileResponse)
async def generate_pdf(set_id: str, image: str = "pins"):
    return pdf_generator.generate_pdf(set_id, image_type=image)
