import {all, createEaseIn, createEaseInOut, createEaseOut, easeInOutCubic, easeOutCubic} from '@motion-canvas/core';
import {Node} from '@motion-canvas/2d';
import {AnimationSpec} from './types';

export function applyAnimation(
  spec: AnimationSpec,
  target: Node,
  objects: Record<string, Node>,
): any {
  const delay = spec.delay ? delayGenerator(spec.delay) : null;
  const easing = getEasing(spec.easing);

  let animation: any;

  switch (spec.action) {
    case 'create':
    case 'draw':
      animation = target.opacity(1, spec.duration, easing);
      break;
    case 'grow':
      animation = target.scale(1, spec.duration, easing);
      break;
    case 'fade_in':
      animation = target.opacity(1, spec.duration, easing);
      break;
    case 'fade_out':
      animation = target.opacity(0, spec.duration, easing);
      break;
    case 'highlight':
      animation = target.scale(1.08, spec.duration / 2, easing);
      break;
    case 'move':
      animation = target.position(
        spec.data.shift ?? [0, 0],
        spec.duration,
        easing,
      );
      break;
    case 'transform': {
      const destination = objects[spec.data.to];
      if (!destination) {
        throw new Error(`Missing transform destination: ${spec.data.to}`);
      }
      animation = target.opacity(0, spec.duration / 2, easing);
      break;
    }
    case 'wait':
      return waitGenerator(spec.duration);
    default:
      throw new Error(`Unsupported animation action: ${spec.action}`);
  }

  return delay ? all(delay, animation) : animation;
}

function delayGenerator(seconds: number): any {
  return async function* () {
    yield* new Promise<void>(resolve => setTimeout(resolve, seconds * 1000));
  };
}

function waitGenerator(seconds: number): any {
  return async function* () {
    yield* new Promise<void>(resolve => setTimeout(resolve, seconds * 1000));
  };
}

function getEasing(name: string): any {
  switch (name) {
    case 'ease_in':
      return createEaseIn(2);
    case 'ease_out':
      return createEaseOut(2);
    case 'ease_in_out':
      return createEaseInOut(2);
    case 'smooth':
      return easeInOutCubic;
    default:
      return undefined;
  }
}
