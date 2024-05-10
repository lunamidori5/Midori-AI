+++
disableToc = false
title = "Subsystem Update Log"
weight = 1
+++

![Midori AI photo](https://tea-cup.midori-ai.xyz/download/logosubsystem.png)

## 5/10/2024
- Update: Planned changes for LocalAi's Gallery API
- Bug Fix: Fixed a loading bug with how we get carly loaded
- Update: Moved Carly's loading to the carly help file
- Update: Updated the news page
- Update: added invokeAI model support
- Update: added docker to invokeai install
- Update: Few more text changes and a action rename
- Update: Cleans up after itself and deletes the installer / old files
- Update: more text clean up for the backends menu
- Update: added better error code for invoke.ai system runner
- Update: added support for running InvokeAI on the system
- Bug Fix: Fixed the news menu
- Update: Added a new "run InvokeAI" menu for running the InvokeAI program
- Bug Fix: Did some bug fixes

## 5/7/2024
- Update: Added a way for "other os" type to auto-update
- Update: Added a yay or nay to purging the venv at the end of other os
- Update: Added a new UI/UX menu
- Bug Fix: Fixed the news menu
- Bug Fix: Fixed naming on the GitHub actions
- Update: Added a way to get the local IP address
- Update: Fully redid some actions that make the docker images
- Update: Reworked the subsystem docker files and the new news post

## 5/5/2024
- Update: Fixed some of Ollama's support 
- Update: Action updates
- Bug Fix: Fixed some server ver bugs
- Bug Fix: Fixed a few more bugs
- Update: Removed verlocking 
- Update: More fixes
- Update: Added a new way to deal with python env
- Update: Code clean up and fixed a socket error 

## 4/22/2024
- Update: Fully reworked how we pack the exec for all os
- Update: Fully redid our linting actions on github to run better
- Update: Mac OS Support should be "working"
- Bug Fix: Fixed a odd bug with VER
- Bug Fix: Fixed a bug with WSL purging docker for no reason

## 4/20/2024
- Update: Added new "WSL Docker Data" backend program (in testing)
- Update: Added more GPU checks to make sure we know for sure if you have a GPU
- Update: Better logging for debugging
- Bug Fix: Fixed a few bugs and made the subsystem docker 200mbs smaller
- Update: Removed some outdated code
- Update: Added new git actions thanks to - [Cryptk](https://github.com/cryptk)
- Update: Subsystem Manager builds are now on github actions, check them out - [Actions](https://github.com/lunamidori5/Midori-AI/actions)

## 4/13/2024
- Known Bug: Upstream changes to LocalAI is making API Keys not work, I am working on a temp fix, please use a outdated image for now.

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