document.addEventListener("DOMContentLoaded", function () {
        // Get all images
        const images = document.querySelectorAll("#imageSlider img");

        if (images === undefined) {
            return;
        }

        let currentIndex = 0;

        // Show the first image
        images[currentIndex].style.display = "block";

        // Function to hide all images
        function hideImages() {
            images.forEach(image => {
                image.style.display = "none";
            });
        }

        // Function to show the next image
        function showNextImage() {
            hideImages();

            currentIndex = (currentIndex + 1) % images.length;

            images[currentIndex].style.display = "block";
        }

        // Set an interval to change the image every 3 seconds (adjust as needed)
        setInterval(showNextImage, 2000);
    });