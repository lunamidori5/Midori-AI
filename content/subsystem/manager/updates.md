+++
disableToc = false
title = "Subsystem Update Log"
weight = 5
+++

## 3/30/2024
- Update 1: Fixed a bug with the subsystem ver not matching the manager ver and endlessly updating the subsystem

## 3/29/2024
- Update 1: Fixed a big bug if the user put the subsystem manager in a folder not named "midoriai"
- Update 2: Fixed the new LocalAI image to only download the models one time
- Update 3: Added server side checks to make sure models are ready for packing to end user
- Update 4: Better logging added to help debug the manager, thank you all for your help!

## 3/27/2024

- Update 1: Fixed a bug that let the user use the subsystem manager with out installing the subsystem (oops)
- Update 2: LocalAI images are now from the Midori AI repo and are update to date with LocalAI's master images*
- Update 3: Added the start for "auto update of docker images" to the subsystem using hashes

Star: These images have models baked into the images to make it easyer to get setup and get going!