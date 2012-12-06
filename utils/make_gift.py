from pyPdf import PdfFileWriter, PdfFileReader
import StringIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def make_Cert(code, redeem_for):
	packet = StringIO.StringIO()
	# create a new PDF with Reportlab

	can = canvas.Canvas(packet, pagesize=letter)
	can.setFont('Helvetica', 32)
	can.drawString(280,540, code)
	can.setFont('Helvetica', 32)
	can.drawString(220,300, redeem_for)
	can.save()

	#move to the beginning of the StringIO buffer
	packet.seek(0)
	new_pdf = PdfFileReader(packet)
	# read your existing PDF
	existing_pdf = PdfFileReader(file("cert.pdf", "rb"))
	output = PdfFileWriter()
	# add the "watermark" (which is the new pdf) on the existing page
	page = existing_pdf.getPage(0)
	page.mergePage(new_pdf.getPage(0))
	output.addPage(page)
	# finally, write "output" to a real file
	outputStream = file(redeem_for.replace(" ", "_") + "_cert.pdf", "wb")
	output.write(outputStream)
	outputStream.close()