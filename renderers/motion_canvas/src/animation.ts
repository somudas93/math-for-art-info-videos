import {chain, easeInOutCubic, easeOutCubic, waitFor} from '@motion-canvas/core';
import {Node} from '@motion-canvas/2d';
import {AnimationSpec} from './types';

export function applyAnimation(
  spec: AnimationSpec,
  target: Node,
  objects: Record<string, Node>,
): any {
  const easing = getEasing(spec.easing);

  switch (spec.action) {
    case 'create':
    case 'draw':
    case 'fade_in':
      return target.opacity(1, spec.duration, easing);

    case 'fade_out':
      return target.opacity(0, spec.duration, easing);

    case 'grow':
      return target.scale(1, spec.duration, easing);

    case 'highlight':
      return chain(
        target.scale(1.08, spec.duration / 2, easing),
        target.scale(1.0, spec.duration / 2, easing),
      );

    case 'move': {
      const shift = spec.data.shift ?? [0, 0];
      const current = target.position();
      return target.position(
        [current.x + shift[0], current.y + shift[1]],
        spec.duration,
        easing,
      );
    }

    case 'transform': {
      const destination = objects[spec.data.to];
      if (!destination) {
        throw new Error(`Missing transform destination: ${spec.data.to}`);
      }
      return chain(
        target.opacity(0, spec.duration / 2, easing),
        target.opacity(destination.opacity(), spec.duration / 2, easing),
      );
    }

    case 'wait':
      return waitFor(spec.duration);

    default:
      throw new Error(`Unsupported animation action: ${spec.action}`);
  }
}

export function* runAnimation(
  spec: AnimationSpec,
  target: Node | undefined,
  objects: Record<string, Node>,
) {
  if (spec.delay > 0) {
    yield* waitFor(spec.delay);
  }

  if (spec.action === 'wait') {
    yield* waitFor(spec.duration);
    return;
  }

  if (!target) {
    throw new Error(`Animation target '${spec.target}' is not present`);
  }

  yield* applyAnimation(spec, target, objects);
}

function getEasing(name: string): any {
  switch (name) {
    case 'smooth':
    case 'ease_in_out':
      return easeInOutCubic;
    case 'ease_out':
      return easeOutCubic;
    default:
      return undefined;
  }
}
