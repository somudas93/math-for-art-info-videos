import {Node} from '@motion-canvas/2d';

export function applyStyle(node: Node, style: Record<string, any>): Node {
  if (style.opacity != null) node.opacity(style.opacity);
  if (style.scale != null) node.scale(style.scale);
  if (style.stroke_width != null && 'lineWidth' in node) {
    (node as any).lineWidth(style.stroke_width);
  }
  if (style.fill != null && 'fill' in node) {
    (node as any).fill(style.fill);
  }
  if (style.stroke != null && 'stroke' in node) {
    (node as any).stroke(style.stroke);
  }
  return node;
}
