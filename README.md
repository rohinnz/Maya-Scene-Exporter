# Maya Scene Exporter

The Maya Scene Exporter handles exporting multiple objects to a game engine (e.g. Unity) as FBX and JSON files.

Features
1. All objects have there transform set to identify before export, while scene transform information is stored in a seperate JSON file.
2. If multiple objects share the same shape, only one object will be exported.

The aim of this tool is to give artists the freedom to build scenes for game engines inside of Maya instead of having to manually export each object and then build the scene in a seperate tool.

## Bookshelf example

In this example scene, there are multiple copies of the book model that all share the same shape node. The tool identifies this during export and only exports one FBX model for a book while storing the transform information for each instance in a JSON file called Bookshelf.SceneExport.json.

![Alt text](maya_ZWVmxWTqCC.png?raw=true "Exporting in Maya")

![Alt text](Unity_JgoSQkWuNY.png?raw=true "Importing in Unity")
