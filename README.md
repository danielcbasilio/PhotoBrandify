# PhotoBrandify
## Description
Stamps the ieee up sb logo on a photo album automatically
## Instructions
1. Check if you have all the dependencies installed. 
1. Place all the photos you want to stamp the logo on the photos_to_brandify directory.
1. Run the command `python3 .` in the PhotoBrandify directory.
1. Choose the stamping mode and folder with the photos you want to stamp the logo in.
1. Press start in the app window.
1. Wait.
1. Your brandified photos will be in the brandified_photos directory.
## Stamping Mode Algorithms
### Standard (standard.py)
Stamps the logo on the bottom-right corner of the image and decides whether it should stamp black or white.
### Tomada de Posse (tdp.py)
Chooses between upper-left, upper-right and bottom-center position to stamp the logo and whether it should be black or white.
### Everything (everything.py)
White, black, blue or dark blue logo. Bottom-center, upper-left, upper-right, bottom-left, bottom-right and a powerful algorithm to determine the optimal combination. You'll just have to wait though.
