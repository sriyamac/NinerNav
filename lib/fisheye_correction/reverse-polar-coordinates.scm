; Partially written using ChatGPT
; Place this script in %appdata%/GIMP/<version>/scripts/
; Then reload scripts in GIMP via Filters > Script-Fu > Refresh Scripts
; Use either via the command line or via Filters > Distors > Reverse Polar Coordinates...

; This defines a function with inputs image and drawable
(define (reverse-polar-coordinates in-file out-file percent-pad)
    ; This declars the variables for the function
    (let* (
		; Open image from in-file and get its drawable
		(image (car (gimp-file-load 1 in-file in-file)))
		(drawable (car (gimp-image-get-active-drawable image)))

        ; This uses the GIMP function gimp-image-width to get the width of the image
        ; and then get the head of the returned list (function of car) and assign it to the variable
        ; 'width'
        (width (car (gimp-image-width image)))
        (height (car (gimp-image-height image)))
		(float-percent-pad (/ percent-pad 100))

        ; Create a new layer, which will later be made fully black to finish processing the image
        (black-layer (car (gimp-layer-new image
            (* width 2)
            (* height float-percent-pad)
            RGBA-IMAGE "Black Layer" 100 NORMAL-MODE)))
    )

    ; Select the entire image and remove other selections
    (gimp-selection-all image)
    (gimp-rect-select image 0 0 width height 0 FALSE 0)

    ; Apply a reverse polar transformation to the image
    (plug-in-polar-coords 1 image drawable 100 0 FALSE TRUE FALSE)

    ; Scheme uses prefix notation, so this is the same as 'width * 2' in other languages
    ; Scale the image to be double wide, fully converts it to equirectangular
    (gimp-image-scale image (* width 2) height)

    ; The camera is only single-hemispherical, so need to pad the "southern hemisphere"
	(gimp-image-resize image (* width 2) (* height (+ 1 float-percent-pad)) 0 0)

    ; Do this with a pure black rectangle along the bottom
    (gimp-image-insert-layer image black-layer 0 0)
    (gimp-context-set-foreground '(0 0 0))
    (gimp-edit-fill black-layer 0)
    (gimp-drawable-set-name black-layer "Black Layer")
    (gimp-layer-set-offsets black-layer 0 height)

	; Flatten the image, resizing the layers to fit everything if needed
	(gimp-image-merge-visible-layers image 0)

	; Grab the new drawable for saving the image
	;(define merged-layer (gimp-image-get-active-drawable image))	; Theoretically a drawable
	;(define merged-layer (gimp-image-merge-visible-layers image 0))
	(define merged-layer (car (gimp-image-get-active-drawable image)))

    ; Make GIMP update its window based on the above functions
    (gimp-displays-flush)

	; Save the image
	(file-jpeg-save
		1				; Run non-interactively
		image			; The image that is being saved
		merged-layer	; The new merged layer
		out-file		; The name of the file to save
		out-file		; A "raw-filename", appears redundant
		1				; Quality, set to max
		0				; Disable smoothing
		1				; Optimize image
		1				; Generate a progressive JPEG image, may cause issues
		""				; Comment for the image
		2				; Subsampling quality, set to max
		0				; Do not force creation of baseline JPEG, may cause issues
		0				; Insert no restart markers, images can't recover from errors
		0				; DCT method. Maybe compression and/or FFT related?
	)
    )
)

; Register the script in a menu
(script-fu-register
	;"apply-polar-coordinates"
	"reverse-polar-coordinates"
	"Reverse Polar Coordinates..."
	"Applies the Polar Coordinates filter with the 'To polar' option unchecked."
	"Paul Warner"
	"No rights reserved."
	"2023"
	""

	SF-STRING "Input file name" "C:\\Users\\Paul\\Desktop\\School\\UNCC\\Sophomore\\S1\\ITSC3155\\ITSC-3155-Final-Project\\lib\\fisheye_correction\\img\\10th_floor_library.jpeg"
	SF-STRING "Output file name" "C:\\Users\\Paul\\Desktop\\School\\UNCC\\Sophomore\\S1\\ITSC3155\\ITSC-3155-Final-Project\\lib\\fisheye_correction\\out\\out.jpeg"
	SF-ADJUSTMENT "Percent fill" '(33 0 100 1 10 0 1)
)

(script-fu-menu-register "reverse-polar-coordinates" "<Image>/Filters/Distorts")

