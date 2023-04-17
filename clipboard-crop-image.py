from PIL import ImageGrab
from PIL import Image, ImageChops

from io import BytesIO
import win32clipboard


def send_to_clipboard(clip_type, data):
	win32clipboard.OpenClipboard()
	win32clipboard.EmptyClipboard()
	win32clipboard.SetClipboardData(clip_type, data)
	win32clipboard.CloseClipboard()

def grab_image_crop():

	im = ImageGrab.grabclipboard()
	if not im:
		print ( "No image in clipboard?" )
		return False
		
	bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
	diff = ImageChops.difference(im, bg)
	diff = ImageChops.add(diff, diff, 2.0, -100)
	bbox = diff.getbbox()
	
	if bbox:
		im2 = im.crop(bbox)
		
		# Save this to PNG?
		# im2.save( 'cropped.png','PNG' )
		
		
		output = BytesIO()
		im2.convert("RGB").save(output, "BMP")
		im_data = output.getvalue()[14:]
		output.close()
		
		send_to_clipboard(win32clipboard.CF_DIB, im_data )

		print ( "Cropping OK. Sent new to clipboard" )
		
		

def main():
	grab_image_crop()

main()
