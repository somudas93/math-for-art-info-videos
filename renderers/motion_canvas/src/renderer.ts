import {Node} from '@motion-canvas/2d';
import {SceneIR} from './types';
import {renderObject} from './primitives';
import {applyStyle} from './style';
import {applyAnimation} from './animation';

export function buildObjects(scene: SceneIR): Record<string, Node> {
  const objects: Record<string, Node> = {};

  for (const obj of scene.objects) {
    const rendered = renderObject(obj, objects);
    objects[obj.id] = applyStyle(rendered, scene.animation.style);
  }

  return objects;
}

export function* renderScene(scene: SceneIR, view: Node) {
  const objects = buildObjects(scene);

  for (const object of Object.values(objects)) {
    view.add(object);
  }

  for (const spec of scene.animation.animations) {
    const target = objects[spec.target];
    if (!target && spec.action !== 'wait') {
      throw new Error(`Animation target '${spec.target}' is not present`);
    }

    if (spec.action === 'wait') {
      yield* new Promise<void>(resolve =>
        setTimeout(resolve, spec.duration * 1000),
      );
      continue;
    }

    yield* applyAnimation(spec, target, objects);
  }
}
