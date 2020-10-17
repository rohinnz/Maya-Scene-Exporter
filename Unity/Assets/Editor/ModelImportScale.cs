// Ensure we have a 1-1 scale on import for our models
using UnityEngine;
using UnityEditor;

class MeshPostprocessor : AssetPostprocessor
{
    void OnPreprocessModel()
    {
        ModelImporter modelImporter = assetImporter as ModelImporter;
        Debug.Log(string.Format("Setting scale on model {0} to global scale 1.0", modelImporter.name));

        // There was an issue with 1cm not converting to 0.01m on import. 
        // So force global scale of 1.0 and ignore file scale.
        modelImporter.useFileUnits = false;
        modelImporter.useFileScale = false;
        modelImporter.globalScale = 1.0f;
    }
}
