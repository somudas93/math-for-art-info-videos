export type SceneObject = {
  id: string;
  kind: string;
  data: Record<string, any>;
};

export type AnimationSpec = {
  action: string;
  target: string;
  duration: number;
  delay: number;
  easing: string;
  data: Record<string, any>;
};

export type SceneIR = {
  name: string;
  duration: number;
  objects: SceneObject[];
  animation: {
    animations: AnimationSpec[];
    style: Record<string, any>;
  };
};
