+++
disableToc = false
title = "Subsystem Update Log"
weight = 1
+++

![Midori AI photo](https://tea-cup.midori-ai.xyz/download/logosubsystem.png)

## 4/13/2024
- Update: Added InvokeAI Backend Program (Host installer)
- Update: Added InvokeAI Backend Program (Subsystem installer)
- Update: Site wide updates, added Big-AGI
- Update: Updated LocalAI Page
- Update: Updated InvokeAI Page
- Update: Fixed Port on Big-AGI (server side, was `3000` now `33000`)
- Update: Removed Home Assistant links
- Update: Removed Oobabooga links
- Update: Removed Ollama link
- Update: Full remake of the Subsystem index page to have better working links

## 4/12/2024
- Bug Fix: Fixed the GPU question to only show up if you have a gpu installed
- Update: Getting ready for InvokeAI backend program to install on host

## 4/10/2024
- Bug Fix: Fixed a bug that was making the user hit enter 3 times after a update
- Bug Fix: Fixed the system message on the 14b ai that helps in the program (she can now help uninstall the subsystem if needed)
- Update: Added new functions to the server for new function based commands for the helper ai
- Update: Updated Invoke AI installer (if its bugged let [Luna](https://io.midori-ai.xyz/about-us/about-luna/) or [Carly](https://io.midori-ai.xyz/about-us/carly-api/) know)

## 4/9/2024
- Bug Fix: Fixed a loop in the help context
- Bug Fix: Fixed the Huggingface downloader (Now runs as root and is its own program)
- Bug Fix: Fixed LocalAI image being out of date
- Bug Fix: Fixed LocalAI AIO image looping endlessly
- Update: [Added LocalAI x Midori AI AIO images to github actions](https://github.com/lunamidori5/Midori-AI/actions/workflows/Make_Subsystem_Dockers.yml)
- Update: Added more context to the 14B model used for the help menu

## 4/7/2024
- Bug Fix: AnythingLLM docker image is now fixed server side. Thank you for your help testers!

## 4/6/2024
- Bug Fix: Removed alot of old text
- Bug Fix: Fixed alot of outdated text
- Bug Fix: Removed Github heartbeat check ||(why were we checking if github was up??)||
- **Known Bug Update**: Huggingface Downloader seems be bugged on LocalAI master... will be working on a fix
- **Known Bug Update**: AnythingLLM docker image seems to be bugged, will be remaking its download / setup from scratch

## 4/3/2024
- New Backend: Added Big-AGI to the subsystem! 
- Update: Added better huggingface downloader commands server side
- Update: Redid how the server sends models to the subsystem
- Bug Fix: Fixed a bug with ollama not starting with the subsystem
- Bug Fix: Fixed a bug with endlessly installing backends 

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