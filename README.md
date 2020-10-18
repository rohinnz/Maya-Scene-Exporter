# Maya Scene Exporter

![Alt text](doc/images/tool_ui.png?raw=true "Maya Scene Exporter")

The Maya Scene Exporter handles exporting multiple objects to a game engine (e.g. Unity) as FBX and JSON files.

The aim of this tool is to give artists the freedom to build scenes for game engines inside of Maya instead of having to manually export each object and then build the scene in a seperate tool.

Features
1. Object transforms stored in JSON file and objects exportd as FBX with identiy transform.
2. When multiple objects share the same shape, only one object is exported as an FBX.

## Example

In this example scene we export a bookshelf full of books. There are multiple copies of the book model that all share the same shape node. The tool identifies this during export and only exports one FBX model for the book while storing the transform information for each instance in a JSON file called Bookshelf.SceneExport.json.

![Alt text](doc/images/example_maya.png?raw=true "Exporting in Maya")

The Unity import tool imports the 2 fbx models and creates instances of each model according to the JSOS file.
![Alt text](doc/images/example_unity.png?raw=true "Importing in Unity")

## Install

Copy SceneExporter folder into your Maya app dir.

- Windows: \Users\<username>\Documents\maya
- Mac: ~<username>/Library/Preferences/Autodesk/maya
