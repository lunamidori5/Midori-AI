+++
disableToc = false
title = "Subsystem Update Log"
weight = 5
+++

## 4/2/2024
- Update: Added a menu to fork into nonsubsystem images for installing models
- Update: Added a way to install Huggingface based models into LocalAI using Midori AI's model repo
- Bug Fix: Fixed some type o and bad text in a few places that was confusing users
- Bug Fix: Fixed a bug when some links were used with Huggingface 
- Update: Server upgrades to our model repo api

## 4/1/2024
- Update 1: Added a new safety check to make sure the subsystem manager is not in the Windows folder or in system32
- Update 2: Added more prompting for the baked in Carly model for if you are asking about GPU or not with cuda

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