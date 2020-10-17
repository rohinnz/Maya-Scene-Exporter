// Example editor tool for setting up instances of prefabs
// in scenes accoring to *.SceneExport.json files.

using UnityEngine;
using UnityEditor;
using System.IO;
using System.Collections.Generic;

// --------------------------------------------------------------------------------------------------------------------

public class SceneImporterTool : EditorWindow
{
    [MenuItem("Tools/Scene Importer")]
    static void Init()
    {
        SceneImporterTool window = (SceneImporterTool)EditorWindow.GetWindow(typeof(SceneImporterTool));
    }

    void OnGUI()
    {
        if (GUILayout.Button("Import all objects"))
        {
            ImportObjects();
        }
    }

    private void ImportObjects()
    {
        DirectoryInfo dir = new DirectoryInfo("Assets/Editor/SceneExportJSON");
        FileInfo[] info = dir.GetFiles("*.SceneExport.json");
        foreach (FileInfo f in info)
        {
            ImportGroup(f.FullName);
        }
    }

    private void ImportGroup(string jsonFilepath)
    {
        //
        // Read json file
        //
        Debug.Log("Attempting to read file at " + jsonFilepath);
        ItemGroup itemGroup = null;
        using (StreamReader reader = new StreamReader(jsonFilepath))
        {
            string json = reader.ReadToEnd();
            ItemGroup.CreateFromJSON(json);
        }

        //
        // Remove existing group
        //
        GameObject groupObj = GameObject.Find("/" + itemGroup.name);
        if (groupObj != null)
        {
            DestroyImmediate(groupObj);
        }

        //
        // Create group and instantiate instances
        //
        groupObj = new GameObject(itemGroup.name);

        // Simple cache to save loading prefab multiple times for each instance.
        var prefabCache = new Dictionary<string, Object>();
        
        foreach (var item in itemGroup.items)
        {
            Debug.Log(string.Format("fbx: {0} - name: {1}", item.fbx, item.name));

            Matrix4x4 matrix = new Matrix4x4();
            for (int i = 0; i < item.transform.Length; ++i)
            {
                matrix[i] = item.transform[i];
            }

            if (!prefabCache.TryGetValue(item.fbx, out Object prefab))
            {
                prefab = Resources.Load(item.fbx, typeof(GameObject)) as GameObject;
                if (prefab == null)
                {
                    throw new FileNotFoundException(string.Format("Unable to prefab {0}. Please make sure the file exists.", item.fbx));
                }

                prefabCache.Add(item.fbx, prefab);
            }

            GameObject instance = (GameObject)Instantiate(prefab, matrix.ExtractPosition(), matrix.ExtractRotation(), groupObj.transform);
            instance.transform.localScale = matrix.ExtractScale();
            instance.name = item.name;
        }
    }
}

// --------------------------------------------------------------------------------------------------------------------
// Temp classes used while reading JSON data.

[System.Serializable]
public class Item
{
    public string fbx;
    public string name;
    public float[] transform;

}

[System.Serializable]
public class ItemGroup
{
    public string name;
    public List<Item> items;

    public static ItemGroup CreateFromJSON(string jsonString)
    {
        return JsonUtility.FromJson<ItemGroup>(jsonString);
    }
}

// --------------------------------------------------------------------------------------------------------------------
// Matrix extensions for fetching position, rotation and scale

public static class MatrixExtensions
{
    public static Quaternion ExtractRotation(this Matrix4x4 matrix)
    {
        Vector3 forward;
        forward.x = matrix.m02;
        forward.y = matrix.m12;
        forward.z = matrix.m22;

        Vector3 upwards;
        upwards.x = matrix.m01;
        upwards.y = matrix.m11;
        upwards.z = matrix.m21;

        return Quaternion.LookRotation(forward, upwards);
    }

    public static Vector3 ExtractPosition(this Matrix4x4 matrix)
    {
        Vector3 position;
        position.x = matrix.m03;
        position.y = matrix.m13;
        position.z = matrix.m23;
        return position;
    }

    public static Vector3 ExtractScale(this Matrix4x4 matrix)
    {
        Vector3 scale;
        scale.x = new Vector4(matrix.m00, matrix.m10, matrix.m20, matrix.m30).magnitude;
        scale.y = new Vector4(matrix.m01, matrix.m11, matrix.m21, matrix.m31).magnitude;
        scale.z = new Vector4(matrix.m02, matrix.m12, matrix.m22, matrix.m32).magnitude;
        return scale;
    }
}