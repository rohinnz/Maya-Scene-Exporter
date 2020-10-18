# Maya Scene Exporter

![Alt text](doc/images/tool_ui.png?raw=true "Maya Scene Exporter")

The Maya Scene Exporter handles exporting multiple objects to a game engine (e.g. Unity) as FBX and JSON files.

Features
1. All objects have there transform set to identify before export, while scene transform information is stored in a seperate JSON file.
2. If multiple objects share the same shape, only one object will be exported.

The aim of this tool is to give artists the freedom to build scenes for game engines inside of Maya instead of having to manually export each object and then build the scene in a seperate tool.

## Example

In this example scene we export a bookshelf full of books. There are multiple copies of the book model that all share the same shape node. The tool identifies this during export and only exports one FBX model for the book while storing the transform information for each instance in a JSON file called Bookshelf.SceneExport.json.

![Alt text](doc/images/example_maya.png?raw=true "Exporting in Maya")

![Alt text](doc/images/example_unity.png?raw=true "Importing in Unity")
This Unity scene is made up of only 2 models.
