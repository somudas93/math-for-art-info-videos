import {
  Circle,
  Line,
  Rect,
  Txt,
  Node,
  Layout,
} from '@motion-canvas/2d';
import {SceneObject} from './types';

type Point = [number, number];

const point = (p: Point): [number, number] => [p[0], -p[1]];

export function renderTimeline(obj: SceneObject): Node {
  const d = obj.data;
  return new Layout({
    children: [
      new Line({
        points: [
          [0, 0],
          [900, 0],
        ],
        lineWidth: 3,
      }),
      new Line({
        points: [
          [0, 0],
          [0, -500],
        ],
        lineWidth: 3,
      }),
    ],
  });
}

export function renderCurve(obj: SceneObject): Node {
  const points = (obj.data.points ?? []).map(point);
  return new Line({
    points,
    lineWidth: 3,
  });
}

export function renderParticles(obj: SceneObject): Node {
  const values: number[] = obj.data.values ?? [];
  const children = values.map((value, i) =>
    new Circle({
      x: i * 30,
      y: -value * 0.2,
      width: 8,
      height: 8,
    }),
  );
  return new Layout({children});
}

export function renderLabel(obj: SceneObject): Node {
  return new Txt({
    text: obj.data.text ?? '',
    x: obj.data.position?.[0] ?? 0,
    y: obj.data.position?.[1] ?? 0,
  });
}

export function renderLine(obj: SceneObject): Node {
  return new Line({
    points: [point(obj.data.start), point(obj.data.end)],
    lineWidth: 3,
  });
}

export function renderCircle(obj: SceneObject): Node {
  return new Circle({
    width: (obj.data.radius ?? 1) * 2,
    height: (obj.data.radius ?? 1) * 2,
  });
}

export function renderRectangle(obj: SceneObject): Node {
  return new Rect({
    width: obj.data.width ?? 2,
    height: obj.data.height ?? 1,
  });
}

export function renderObject(obj: SceneObject, rendered: Record<string, Node>): Node {
  switch (obj.kind) {
    case 'timeline':
      return renderTimeline(obj);
    case 'curve':
      return renderCurve(obj);
    case 'particles':
      return renderParticles(obj);
    case 'label':
      return renderLabel(obj);
    case 'line':
      return renderLine(obj);
    case 'circle':
      return renderCircle(obj);
    case 'rectangle':
      return renderRectangle(obj);
    case 'group':
      return new Layout({
        children: (obj.data.children ?? []).map((id: string) => rendered[id]),
      });
    default:
      throw new Error(`Unsupported SceneObject kind: ${obj.kind}`);
  }
}
