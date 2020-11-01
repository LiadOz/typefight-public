export interface IView {
    initView(): void;
    sendPayload(): void;
}

export class ViewFactory {
    public create(view_type: string, container: HTMLElement): IView {
        if (view_type == 'PIXI') {
            return new PixiView(container as HTMLCanvasElement);
        }
        throw new TypeError(`No view type ${view_type}`)
    }
}

import * as PIXI from 'pixi.js';
class PixiView implements IView {
    private renderer: PIXI.Renderer;
    private stage: PIXI.Container;
    private ticker: PIXI.Ticker;

    constructor(container: HTMLCanvasElement) {
        const app = new PIXI.Application({
            view: container,
            backgroundColor: 0xffffff,
        })
        this.renderer = app.renderer;
        this.stage = app.stage;
        this.ticker = app.ticker;
        this.ticker.start();
    }

    public initView(): void {
        var t = new PIXI.Text('welcome', {fontFamily: 'Arial', fontSize: 40})
        t.x = this.renderer.width / 2;
        t.y = this.renderer.height / 2;
        t.anchor.set(0.5);
        this.stage.addChild(t);
        
        var y_pos = 0;
        var initial_y = this.renderer.height / 2;
        function animate(){
            t.y = initial_y + Math.sin(y_pos) * 30;
            y_pos += 0.1;
        }

        this.ticker.add(animate);
    }

    public sendPayload(): void {
        
    }
}
