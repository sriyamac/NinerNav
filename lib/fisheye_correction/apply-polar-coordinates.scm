; Convert a single-hemispherical (assume upper hemisphere) image into an equirectangular image and
; pad the lower hemisphere with black
; Written with a large amount of ChatGPT

; GIMP uses Scheme, which is similar to Perl, so it is totally unlike C-style languages
; This defines a function with inputs image and drawable
(define (apply-polar-coordinates image drawable)
    ; This declars the variables for the function
    (let* (
        ; This uses the GIMP function gimp-image-width to get the width of the image
        ; and then get the head of the returned list (function of car) and assign it to the variable
        ; 'width'
        (width (car (gimp-image-width image)))
        (height (car (gimp-image-height image)))

        ; Create a new layer, which will later be made fully black to finish processing the image
        (black-layer (car (gimp-layer-new image
            (* (car (gimp-image-width image)) 2)
            (car (gimp-image-height image))
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
    (gimp-image-resize image (* width 2) (* height 2) 0 0)

    ; Do this with a pure black rectangle along the bottom
    (gimp-image-insert-layer image black-layer 0 0)
    (gimp-context-set-foreground '(0 0 0))
    (gimp-edit-fill black-layer 0)
    (gimp-drawable-set-name black-layer "Black Layer")
    (gimp-layer-set-offsets black-layer 0 height)

    ; Make GIMP update its window based on the above functions
    (gimp-displays-flush)
    )
)

; Register the script in a menu
(script-fu-register
  "apply-polar-coordinates"
  "Reverse Polar Coordinates..."
  "Applies the Polar Coordinates filter with the 'To polar' option unchecked."
  "Paul Warner"
  "No rights reserved. Even if AI generated works are copyrightable, do whatever you want with this."
  "2023"
  ""
  SF-IMAGE "Image" 0
  SF-DRAWABLE "Drawable" 0
)

(script-fu-menu-register "apply-polar-coordinates" "<Image>/Filters/Distort")

