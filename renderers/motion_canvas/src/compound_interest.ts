import {makeScene2D} from '@motion-canvas/2d';
import {renderScene} from './renderer';
import scene from '../data/compound_interest.json';

export default makeScene2D(function* (view) {
  yield* renderScene(scene, view);
});
