import {Presenter} from './present/presentor'

const canvas = document.getElementById('canvas') as HTMLCanvasElement;
var p = new Presenter(canvas);

document.addEventListener('keydown', (event: KeyboardEvent) => {
    if (event.key == 'Backspace')
        event.preventDefault();
});

p.run();
