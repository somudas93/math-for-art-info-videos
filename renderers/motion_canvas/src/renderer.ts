import {Node} from '@motion-canvas/2d';
import {SceneIR} from './types';
import {renderObject} from './primitives';
import {applyStyle} from './style';
import {runAnimation} from './animation';

export function buildObjects(scene: SceneIR): Record<string, Node> {
  const objects: Record<string, Node> = {};

  for (const obj of scene.objects) {
    const rendered = renderObject(obj, objects);
    objects[obj.id] = applyStyle(rendered, scene.animation.style);
  }

  // Establish renderer-neutral initial states before playback.
  for (const spec of scene.animation.animations) {
    const target = objects[spec.target];
    if (!target) continue;

    if (spec.action === 'create' || spec.action === 'draw' || spec.action === 'fade_in') {
      target.opacity(0);
    }
    if (spec.action === 'grow') {
      target.scale(0);
    }
  }

  return objects;
}

export function* renderScene(scene: SceneIR, view: Node) {
  const objects = buildObjects(scene);

  for (const object of Object.values(objects)) {
    view.add(object);
  }

  for (const spec of scene.animation.animations) {
    yield* runAnimation(spec, objects[spec.target], objects);
  }
}
