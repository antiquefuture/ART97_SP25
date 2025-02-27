import bpy
import mathutils

def get_scene_bounds(objects):
    """Calculate the min and max bounds of all objects in world space."""
    min_x, max_x = float('inf'), float('-inf')
    min_y, max_y = float('inf'), float('-inf')
    min_z, max_z = float('inf'), float('-inf')
    
    for obj in objects:
        if obj.type in {'MESH', 'CURVE', 'SURFACE', 'META', 'FONT'}:
            bbox_corners = [obj.matrix_world @ mathutils.Vector(corner) for corner in obj.bound_box]
            min_x = min(min_x, min(v.x for v in bbox_corners))
            max_x = max(max_x, max(v.x for v in bbox_corners))
            min_y = min(min_y, min(v.y for v in bbox_corners))
            max_y = max(max_y, max(v.y for v in bbox_corners))
            min_z = min(min_z, min(v.z for v in bbox_corners))
            max_z = max(max_z, max(v.z for v in bbox_corners))
    
    return (min_x, max_x), (min_y, max_y), (min_z, max_z)

def rescale_scene(target_height=1.0):
    """Groups all objects, rescales everything uniformly, and repositions the center to (0,0,0). Adjusts lights accordingly."""
    
    # Get all valid objects
    objects = [obj for obj in bpy.context.scene.objects if obj.type in {'MESH', 'CURVE', 'SURFACE', 'META', 'FONT'}]
    lights = [obj for obj in bpy.context.scene.objects if obj.type == 'LIGHT']

    if not objects:
        print("No valid objects found in the scene.")
        return

    # Create a new empty object as the parent
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
    scene_anchor = bpy.context.object

    # Parent all objects to the empty
    for obj in objects + lights:
        obj.select_set(True)
        obj.parent = scene_anchor
    
    bpy.context.view_layer.objects.active = scene_anchor

    # Find the bounding box dimensions
    (min_x, max_x), (min_y, max_y), (min_z, max_z) = get_scene_bounds(objects)
    tallest_height = max_z - min_z

    if tallest_height == 0:
        print("Could not determine object heights.")
        return

    # Compute the uniform scale factor
    scale_factor = target_height / tallest_height

    # Apply scale to the parent empty (scaling everything together)
    scene_anchor.scale *= scale_factor
    
    # Adjust light intensities and radii
    for light in lights:
        if light.data.type in {'POINT', 'SPOT', 'SUN', 'AREA'}:
            light.data.energy *= scale_factor if scale_factor > 1 else scale_factor ** 0.5  # Increase proportionally, reduce gently
            if hasattr(light.data, 'shadow_soft_size'):
                light.data.shadow_soft_size *= scale_factor  # Adjust light radius proportionally
    
    # Apply the transform to freeze the scale
    bpy.ops.object.transform_apply(scale=True)
    
    # Recalculate bounds after scaling
    (min_x, max_x), (min_y, max_y), (min_z, max_z) = get_scene_bounds(objects)
    
    # Compute the new center position
    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2
    bottom_z = min_z
    
    # Move the group so the bottom center is at (0,0,0)
    scene_anchor.location.x -= center_x
    scene_anchor.location.y -= center_y
    scene_anchor.location.z -= bottom_z
    bpy.ops.object.transform_apply(location=True)

    # Unparent objects if needed (optional)
    for obj in objects + lights:
        obj.parent = None

    # Delete the empty object
    bpy.data.objects.remove(scene_anchor)

    bpy.context.view_layer.update()

    print(f"Rescaled scene with factor: {scale_factor}, repositioned bottom center to (0,0,0), adjusted light intensities and radii.")

# Run the function
rescale_scene(1.0)
